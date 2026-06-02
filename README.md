# Edge — Offline AI Tutor for ASEAN Schools

> **Run a full AI-powered classroom on a $80 Raspberry Pi. No internet. No cloud. No fees.**

Edge is an off-grid, multilingual AI tutor that runs entirely on a Raspberry Pi 5
connected to a portable WiFi router. Students connect from any phone browser and get
curriculum-grounded answers, quizzes, voice interaction, and microcredentials —
even in areas with zero connectivity.

Built for the **AI for a Resilient ASEAN** track.

---

## Table of Contents

1. [Why Edge](#why-edunode)
2. [Hardware Bill of Materials](#hardware-bill-of-materials)
3. [System Architecture](#system-architecture)
4. [Project Structure](#project-structure)
5. [Quick Start (Laptop Dev)](#quick-start-laptop-dev)
6. [Raspberry Pi Deployment](#raspberry-pi-deployment)
7. [Configuration](#configuration)
8. [Feature Overview](#feature-overview)
9. [API Reference](#api-reference)
10. [Multilingual Support](#multilingual-support)
11. [Sneakernet USB Sync](#sneakernet-usb-sync)
12. [Microcredentials](#microcredentials)
13. [Contributing / Adding Curriculum](#contributing--adding-curriculum)
14. [Roadmap](#roadmap)

---

## Why Edge

| Problem | Edge Solution |
|---|---|
| 47 % of ASEAN rural schools have no internet | Runs 100 % offline on a $80 Pi |
| AI tools require cloud subscriptions | Local SLM (Llama 3 / Gemma 2, quantized Q4) |
| Students speak minority languages | Per-hub language config (Iban, Cebuano, Dayak…) |
| No power infrastructure | 50 W solar panel + 30 000 mAh battery powers Pi all day |
| No way to update content remotely | Sneakernet USB sync — teacher plugs in a drive monthly |
| No recognition for offline learning | PDF microcredentials aligned with UNESCO 2022 framework |

---

## Hardware Bill of Materials

| Component | Recommended | Est. Cost |
|---|---|---|
| Single-board computer | Raspberry Pi 5 (8 GB RAM) | $80 |
| Storage | 256 GB NVMe SSD (USB 3) | $25 |
| Router | TP-Link TL-WR902AC (portable) | $15 |
| Power | 30 000 mAh USB-C battery bank | $30 |
| Solar (optional) | 50 W foldable panel + MPPT | $45 |
| **Total** | | **~$195** |

> For development, any Linux laptop or macOS machine works. See [Quick Start](#quick-start-laptop-dev).

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       PHYSICAL LAYER (HARDWARE)                          │
│                                                                          │
│  [50W Solar] ──► [30 000 mAh Battery] ──► [Raspberry Pi 5 (8GB)]        │
│                                                    │                     │
│                                         [256GB SSD (NVMe USB)]           │
│                                                    │                     │
│                                         [TP-Link Router ($15)]           │
│                                                    │                     │
│                             ┌──────────────────────┘                     │
│                    [Phone A (Chrome)]  [Phone B (Chrome)]  …             │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                       SOFTWARE STACK (ON THE PI)                         │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  PRESENTATION LAYER  — Flask → http://192.168.1.1:5000             │  │
│  │  Mobile HTML/CSS/JS  |  PWA "Add to Home Screen"                   │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│  ┌────────────────────────────────▼───────────────────────────────────┐  │
│  │  APPLICATION LAYER  — Python / Flask                                │  │
│  │  Chat · Quiz · Podcast · Flashcard · Progress · P2P Share · Sync   │  │
│  └───────────────┬───────────────────────────────┬────────────────────┘  │
│                  │                               │                       │
│  ┌───────────────▼──────────┐   ┌───────────────▼────────────────────┐  │
│  │  VOICE LAYER             │   │  AI / RAG LAYER                     │  │
│  │  Whisper.cpp (STT)       │   │  Ollama — llama3.2:3b Q4            │  │
│  │  Piper TTS               │   │  ChromaDB — curriculum vectors      │  │
│  └──────────────────────────┘   └─────────────────────────────────────┘  │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  DATA LAYER                                                         │  │
│  │  SQLite (students · sessions · badges)  |  /data/curriculum/ PDFs  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
edunode/
├── app.py                          ← Flask entry point (main server)
├── config.py                       ← Per-hub locale config (region, languages)
├── asean_ai_tutor_project.py       ← Legacy single-file prototype (Phase 0)
├── requirements.txt
├── setup.sh                        ← One-shot Pi setup script
├── sneakernet_sync.py              ← USB teacher sync (import PDFs / export reports)
├── .env.example                    ← Copy to .env and configure
│
├── core/
│   ├── llm_engine.py               ← Ollama wrapper (chat, quiz, podcast prompts)
│   ├── rag_engine.py               ← ChromaDB PDF ingestion + semantic retrieval
│   ├── voice_engine.py             ← Whisper.cpp STT + Piper TTS
│   ├── quiz_engine.py              ← JSON quiz validator + score logic
│   ├── podcast_engine.py           ← MAYA/NIKO dialogue generator
│   ├── flashcard_engine.py         ← Flashcard + slide carousel builder
│   ├── progress_tracker.py         ← SQLite student CRUD + badge engine
│   ├── microcredential_engine.py   ← PDF certificate generator (ReportLab)
│   └── p2p_share.py                ← LAN QR share (no internet needed)
│
├── data/
│   ├── curriculum/                 ← Offline PDFs (one per subject/grade/language)
│   ├── media/                      ← Diagrams and images for flashcards
│   ├── dialect_logs/               ← Anonymised logs for research flywheel
│   ├── audio/                      ← Piper TTS output cache
│   ├── uploads/                    ← Admin-uploaded documents
│   └── chroma/                     ← ChromaDB persistent vector store
│
├── models/
│   ├── whisper/                    ← ggml-base.en.bin (~150 MB)
│   └── piper/                      ← en_US-lessac-medium.onnx (~60 MB)
│
├── db/
│   └── edunode.db                  ← SQLite (students, sessions, badges, quizzes)
│
├── static/
│   ├── css/main.css
│   ├── js/
│   │   ├── chat.js
│   │   ├── quiz.js
│   │   ├── flashcard.js
│   │   └── podcast.js
│   ├── icons/
│   │   └── manifest.json           ← PWA manifest
│   ├── certificates/               ← Generated PDF microcredentials
│   └── shared/                     ← P2P QR share content
│
└── templates/
    ├── base.html                   ← Shared layout (navbar, offline indicator)
    ├── home.html                   ← Dashboard: subject + language picker
    ├── chat.html                   ← Main tutor chat interface
    ├── quiz.html                   ← MCQ quiz UI
    ├── flashcard.html              ← Swipeable slide carousel
    ├── podcast.html                ← Podcast player UI
    ├── progress.html               ← Badge wall + quiz history
    ├── share_view.html             ← P2P shared content viewer
    └── admin.html                  ← Teacher dashboard
```

---

## Quick Start (Laptop Dev)

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- ffmpeg (`brew install ffmpeg` on macOS)

### Steps

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/Edge.git
cd Edge

# 2. Python environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Pull the SLM (one-time, ~2 GB)
ollama pull llama3.2:3b-instruct-q4_K_M

# 4. Configure
cp .env.example .env
# Edit .env → set ADMIN_TOKEN to something secret

# 5. Run
ollama serve &                        # keep running in background
python app.py                         # or: python asean_ai_tutor_project.py
```

Open `http://localhost:5000` in your browser. Scan the QR code printed in the
terminal to test from your phone on the same WiFi.

---

## Raspberry Pi Deployment

```bash
# On the Pi (Ubuntu 24.04 or Raspberry Pi OS Bookworm):
git clone https://github.com/YOUR_USERNAME/Edge.git
cd Edge
bash setup.sh          # installs Ollama, Whisper.cpp, Piper, Python deps

# Configure
cp .env.example .env
nano .env              # set ADMIN_TOKEN, SERVER_HOST=0.0.0.0

# Start (production)
ollama serve &
gunicorn -w 2 -b 0.0.0.0:5000 'app:app'
```

### Network Setup

| Setting | Value |
|---|---|
| Pi static IP | `192.168.1.1` |
| Router DHCP range | `192.168.1.2 – 192.168.1.254` |
| Student URL | `http://192.168.1.1` or `http://edunode.local` |
| Admin URL | `http://192.168.1.1/admin` |

### Auto-start on Boot

```bash
# /etc/systemd/system/edunode.service
[Unit]
Description=Edge AI Tutor
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Edge
ExecStartPre=/usr/local/bin/ollama serve
ExecStart=/home/pi/.venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable edunode && sudo systemctl start edunode
```

---

## Configuration

Copy `.env.example` to `.env` and edit:

```ini
OLLAMA_BASE=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b-instruct-q4_K_M
EMBED_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=400
CHUNK_OVERLAP=60
TOP_K=5
MAX_TOKENS=512
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
ADMIN_TOKEN=change-me-in-dot-env   # ← MUST change before deploying
MAX_UPLOAD_MB=32
```

For per-hub locale, edit `config.py`:

```python
# Sarawak Hub (default)
HUB_REGION    = "Sarawak, Malaysia"
HUB_LANGUAGES = ["English", "Bahasa Melayu", "Iban"]

# Visayas Hub — swap in for Philippines deployment
# HUB_REGION    = "Visayas, Philippines"
# HUB_LANGUAGES = ["English", "Filipino", "Cebuano"]
```

---

## Feature Overview

| Feature | How It Works | Status |
|---|---|---|
| **AI Chat Tutor** | Student types/speaks → RAG retrieves curriculum context → Ollama answers | ✅ Core |
| **Voice Input (STT)** | Browser records WebM → Whisper.cpp transcribes → sent to AI | ✅ Core |
| **Voice Output (TTS)** | AI answer → Piper TTS → WAV auto-plays on student phone | ✅ Core |
| **MCQ Quiz** | AI generates 3–5 JSON questions from topic + curriculum | ✅ Core |
| **Podcast Mode** | AI writes MAYA/NIKO dialogue → Piper narrates both roles | 🔶 Week 2 |
| **Flashcard Carousel** | AI generates slide + image from curriculum PDF | 🔶 Week 2 |
| **Progress Tracker** | SQLite stores sessions, quiz scores, streaks | 🔶 Week 3 |
| **Badge System** | Rule-based awards (First Step, Quiz Ace, Week Warrior…) | 🔶 Week 3 |
| **Microcredentials** | ReportLab PDF cert when quiz pass-rate threshold met | 🔶 Week 3 |
| **Sneakernet Sync** | Teacher plugs USB → new PDFs in, progress DB out | 🔶 Week 3 |
| **P2P QR Share** | Share quiz/AI answer via QR code to another phone on LAN | 🔶 Week 3 |
| **PWA** | "Add to Home Screen" on Android Chrome — works offline | 🔶 Week 4 |
| **Admin Dashboard** | Sync status, student list, document management | 🔶 Week 4 |

---

## API Reference

### Student Endpoints

| Method | Path | Body / Params | Response |
|---|---|---|---|
| `GET` | `/` | — | Home page |
| `GET` | `/chat` | — | Chat UI |
| `GET` | `/quiz` | — | Quiz UI |
| `GET` | `/podcast` | — | Podcast UI |
| `GET` | `/progress` | — | Progress / badge wall |
| `POST` | `/api/chat` | `{message, language, student_id}` | `{response}` |
| `POST` | `/api/voice/stt` | raw audio bytes (WebM) | `{text}` |
| `POST` | `/api/voice/tts` | `{text}` | WAV audio stream |
| `POST` | `/api/quiz/generate` | `{topic, language}` | `{questions: [...]}` |
| `POST` | `/api/quiz/submit` | `{student_id, topic, score, total}` | `{status, microcredentials_earned}` |
| `POST` | `/api/podcast/generate` | `{topic, language}` | `{script, audio_url}` |
| `GET` | `/api/progress/<id>` | — | `{badges, recent_quizzes}` |
| `POST` | `/api/share/create` | `{content, type}` | `{share_id, local_url, qr_image_path}` |
| `GET` | `/share/<id>` | — | Share viewer page |
| `GET` | `/api/status` | — | `{ollama, tts, stt, docs, model}` |

### Admin Endpoints (require `X-Admin-Token` header or `admin_token` form field)

| Method | Path | Body | Response |
|---|---|---|---|
| `GET` | `/admin` | — | Admin panel |
| `POST` | `/api/ingest` | multipart `file`, `subject`, `grade` | `{message, chunks}` |
| `GET` | `/api/sources` | — | `{sources: [...]}` |
| `GET` | `/qr` | — | PNG QR code for student URL |

---

## Multilingual Support

Language is selected by the student in the UI. It is passed to the SLM prompt:

```
You MUST respond in {language}.
```

**Supported out of the box:**

| Hub | Primary | Languages |
|---|---|---|
| Sarawak (default) | Bahasa Melayu | English, Bahasa Melayu, Iban |
| Visayas | Filipino | English, Filipino, Cebuano |
| Kalimantan | Bahasa Indonesia | English, Bahasa Indonesia, Dayak |

To add a new hub: edit `HUB_LANGUAGES` in `config.py`. No code changes required.

---

## Sneakernet USB Sync

Run by the teacher once a month when the USB drive is delivered from the district office:

```bash
python sneakernet_sync.py --usb /media/usb0
```

**What it does:**

1. Copies new curriculum PDFs from `USB/new_curriculum/` → `data/curriculum/`
2. Re-ingests all PDFs into ChromaDB (idempotent — skips existing chunks)
3. Applies a model update script if present on the USB
4. Exports the SQLite progress DB to `USB/exported_reports/`
5. Exports anonymised dialect logs as JSON for university research

---

## Microcredentials

When a student's average quiz score for a topic exceeds the threshold:

| Credential | Min Avg | Quizzes Required |
|---|---|---|
| Mathematics Foundations | 70 % | 3 |
| Science Literacy | 70 % | 3 |
| Digital Citizenship | 60 % | 2 |
| Environmental Sustainability | 65 % | 2 |

A PDF certificate is automatically generated and available to download.
Certificates are aligned with the **UNESCO 2022 Microcredential Framework**.

---

## Contributing / Adding Curriculum

1. Convert your curriculum document to PDF (any ASEAN language / subject)
2. Name it clearly: `math_grade7_cebuano.pdf`, `science_grade8_iban.pdf`
3. Either:
   - Drop it into `data/curriculum/` and restart the server, OR
   - Upload it via the Admin panel at `/admin`
4. Edge will automatically chunk and index it into ChromaDB

---

## Roadmap

- [ ] `core/flashcard_engine.py` — image + AI text carousel
- [ ] `templates/flashcard.html` — swipeable slide UI
- [ ] Multi-student login (PIN-based, no passwords)
- [ ] Offline-first PWA with Service Worker caching
- [ ] Cebuano and Iban Piper voice models
- [ ] Federated progress sync across multiple Pi hubs via USB
- [ ] Raspberry Pi CM5 carrier board for ruggedised enclosure
- [ ] ASEAN MoE curriculum alignment mapping

---

## License

MIT — free for schools, NGOs, and education projects.

---

*Edge — Because every child deserves a tutor, even 80 km from the nearest city.*

