# EduNode — Step-by-Step Execution Plan

This is the authoritative build guide. Follow each step in order.
Each step has a clear **goal**, **files to create/edit**, and a **done check**.

---

## Pre-flight: What Already Exists

| File | Status | Notes |
|---|---|---|
| `asean_ai_tutor_project.py` | ✅ Done | Single-file prototype (Phases 0–8) |
| `requirements.txt` | ✅ Done | Needs `reportlab` added |
| `setup.sh` | ✅ Done | Pi one-shot installer |
| `.env.example` | ✅ Done | |
| `templates/index.html` | ✅ Done | Student chat UI |
| `templates/admin.html` | ✅ Done | Admin/teacher panel |
| `static/css/style.css` | ✅ Done | |
| `static/js/app.js` | ✅ Done | Voice + fetch logic |
| `README.md` | ✅ Done | |

The steps below build the **modular architecture** described in the README.
The monolithic prototype (`asean_ai_tutor_project.py`) remains as a reference.

---

## STEP 0 — Update requirements.txt

**Goal:** Add `reportlab` (PDF certificates) and `piper-tts` stub.

**Edit:** `requirements.txt`

Add to the end:
```
reportlab>=4.0
```

**Done check:** `pip install -r requirements.txt` completes with no errors.

---

## STEP 1 — Create `config.py`  ✅ Done

**Goal:** Single source of truth for all 13 hub deployments with two-tier language strategy.

All 13 hub configurations are defined in `config.py`. Uncomment the relevant
block for the target region; the active (uncommented) block becomes the hub identity.

**Two-tier language strategy:**
- `TIER_1_LANGS` — Full AI generation directly in these languages. The SLM has
  sufficient training data; `"respond in {language}"` in the system prompt works reliably.
- `TIER_2_LANGS` — Bridge mode. AI generates in English → key terms translated
  via HuggingFace glossary datasets. Output shown bilingually. Used for
  deep-minority languages (Iban, Cebuano, Sundanese, Isan, Hmong, Shan, Tetum, Kedayan).

**13 hub configurations defined:**

| # | Hub ID | Region | Tier-1 | Tier-2 |
|---|---|---|---|---|
| 1 | `singapore` | Singapore | English | — |
| 2 | `vietnam` | Vietnam | English, Vietnamese | Hmong |
| 3 | `sarawak` | Sarawak, Malaysia | English, Bahasa Melayu | Iban, Kedayan |
| 4 | `west_java` | West Java, Indonesia | English, Bahasa Indonesia | Sundanese |
| 5 | `visayas` | Visayas, Philippines | English, Filipino | Cebuano |
| 6 | `isan` | Northeast Thailand | English, Thai | Isan |
| 7 | `cambodia` | Rural Cambodia | English, Khmer | — |
| 8 | `laos` | Rural Laos | English, Lao | — |
| 9 | `shan` | Shan State, Myanmar | English | Shan |
| 10 | `timor_leste` | Timor-Leste | English | Tetum |
| 11 | `brunei` | Brunei Darussalam | English, Bahasa Melayu | Kedayan |
| 12 | `kalimantan` | Kalimantan, Indonesia | English, Bahasa Indonesia | Dayak |
| 13 | `peninsular_malaysia` | Peninsular Malaysia | English, Bahasa Melayu | — |

**Done check:** `python -c "from config import HUB_LANGUAGES, TIER_1_LANGS, TIER_2_LANGS; print(HUB_LANGUAGES, TIER_1_LANGS, TIER_2_LANGS)"`

---

## STEP 1A — Download Tier-2 Glossary Datasets

**Goal:** Download the HuggingFace datasets that power bridge-mode translation
for Tier-2 languages. Store as JSON files in `data/glossaries/`.

**Create:** `tools/download_glossaries.py`

```bash
python tools/download_glossaries.py
```

What it downloads:
- `filbench/cebuano-readability` → `data/glossaries/cebuano.json`
- `VynerCK/Iban-language-data` → `data/glossaries/iban.json`

Each file is normalised to: `[{"english": "...", "native": "..."}]`
so `core/llm_engine.py` can inject relevant terms into the bridge prompt.

Future datasets to add as community contributions arrive:
- Sundanese, Isan, Hmong, Shan, Tetum, Kedayan

**Done check:**
```bash
ls -lh data/glossaries/
# cebuano.json  iban.json
```

---

## STEP 1B — Kolibri + Khan Academy Integration

**Goal:** Run Kolibri (offline learning platform) alongside EduNode on the same Pi.
Students watch Khan Academy video lessons in Kolibri, then ask EduNode AI
follow-up questions — both grounded in the same curriculum content.

**Architecture:**
```
Pi port 5000 → EduNode (AI tutor, chat, quiz, voice)
Pi port 8080 → Kolibri (Khan Academy lessons, exercises, videos)

Student flow:
  1. Open http://192.168.1.1:8080 → watch Kolibri math video
  2. Tap "Ask EduNode" button (added to base.html navbar)
  3. Redirects to http://192.168.1.1:5000/chat?subject=Mathematics
  4. AI tutor answers from the same Khan Academy text content via RAG
```

**Setup steps (added to `setup.sh`):**
```bash
# Install Kolibri
pip install kolibri
python -m kolibri start --background

# Import Khan Academy channel (English, ~3 GB — run once)
python -m kolibri manage importchannel network 7765d6abe4f5413b9bb35a03b4bcea63
python -m kolibri manage importcontent network 7765d6abe4f5413b9bb35a03b4bcea63

# For localised channels, use the language-specific channel ID from:
# https://kolibri-studio.readthedocs.io/en/latest/working_with_content.html
```

**Kolibri channel IDs for EduNode hubs:**

| Language | Channel | ID |
|---|---|---|
| English | Khan Academy (en) | `7765d6abe4f5413b9bb35a03b4bcea63` |
| Vietnamese | Khan Academy (vi) | Look up on Kolibri Studio |
| Bahasa Indonesia | Khan Academy (id) | Look up on Kolibri Studio |
| Khmer | Khan Academy (km) | Look up on Kolibri Studio |

**Curriculum text extraction for RAG:**

Create `tools/kolibri_to_rag.py` — exports Kolibri article text to
`data/curriculum/kolibri_<subject>_<lang>.txt` so EduNode's RAG pipeline
can index it alongside official PDF textbooks.

**Done check:**
```bash
curl http://localhost:8080/api/public/v1/info/
# → {"installed": true, ...}
curl http://localhost:5000/api/status
# → {"kolibri": true, ...}  (add kolibri field to status endpoint)
```

---

## STEP 2 — Create `core/__init__.py`

**Goal:** Make `core/` a Python package.

**Create:** `core/__init__.py` (empty file)

**Done check:** `python -c "import core"` succeeds silently.

---

## STEP 3 — Create `core/rag_engine.py`

**Goal:** Offline RAG — ingest PDFs from `data/curriculum/` into ChromaDB,
expose `retrieve_context(query)` for use by all other modules.

**Create:** `core/rag_engine.py`

Key functions:
- `get_or_create_collection()` — connects to ChromaDB at `data/chroma/`
- `ingest_pdfs(curriculum_dir)` — reads every `.pdf` in the dir, chunks into
  ~300-word passages, upserts into ChromaDB (idempotent)
- `retrieve_context(query, n_results=3, subject=None)` — returns top-N passages
  as a single concatenated string ready to inject into a prompt

Implementation notes:
- Use `chromadb.PersistentClient(path="data/chroma")`
- Embedding function: `SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")`
- Collection metadata: `{"hnsw:space": "cosine"}`
- Chunk IDs: `sha1(filename + chunk_index + first_60_chars)[:16]` — makes
  re-ingestion idempotent
- Store metadata: `source`, `subject`, `grade` per chunk

**Done check:**
```bash
python -c "
from core.rag_engine import ingest_pdfs, retrieve_context
ingest_pdfs()
print(retrieve_context('what is photosynthesis'))
"
```

---

## STEP 4 — Create `core/llm_engine.py`

**Goal:** All Ollama (SLM) interactions in one place — chat, quiz generation,
podcast script generation, AND the Tier-2 bridge-mode translation layer.

**Create:** `core/llm_engine.py`

### Core functions:

- `query_tutor(user_message, language, rag_context)` → `str`
  - Checks `config.TIER_1_LANGS` vs `config.TIER_2_LANGS` to decide mode
  - **Tier-1 path:** system prompt includes `"You MUST respond in {language}"`
  - **Tier-2 path:** calls `_bridge_translate()` after English generation
  - Calls `POST /api/generate` on Ollama
- `generate_quiz(topic, language, rag_context)` → `list[dict]`
  - System prompt: output EXACTLY 3 MCQs as a JSON array
    `[{"question","options":["A…","B…","C…","D…"],"answer":"A"}]`
  - Temperature 0.3, parse JSON from response, return `[]` on parse failure
- `generate_podcast_script(topic, language)` → `str`
  - Two hosts: MAYA (curious) and NIKO (explains)
  - 6–8 exchanges, formatted `MAYA: …\nNIKO: …`
  - Temperature 0.8

### Bridge-mode translation layer (Tier-2 languages):

```python
def _load_glossary(language: str) -> dict:
    """
    Load the HuggingFace glossary JSON for a Tier-2 language.
    Returns {english_term: native_term} lookup dict.
    Falls back to {} if glossary file not found.
    """
    path = Path(f"data/glossaries/{language.lower()}.json")
    if not path.exists():
        return {}
    entries = json.loads(path.read_text())
    return {e["english"].lower(): e["native"] for e in entries if "english" in e and "native" in e}


def _bridge_translate(english_text: str, language: str) -> str:
    """
    Tier-2 bridge mode:
    1. Ask the SLM to translate the English answer into {language} using
       the provided glossary terms for accuracy.
    2. Return bilingual output:
       [English] {english_text}
       [{language}] {translated_text}
    Falls back to English-only if translation fails.
    """
    glossary = _load_glossary(language)
    glossary_hint = ", ".join(f"{k}={v}" for k, v in list(glossary.items())[:30])

    prompt = (
        f"Translate the following into {language}. "
        f"Use these key terms where applicable: {glossary_hint}\n\n"
        f"Text: {english_text}\n\nTranslation:"
    )
    translated = _ollama_generate(prompt, temperature=0.3, max_tokens=300)
    if not translated:
        return english_text
    return f"[English] {english_text}\n[{language}] {translated}"
```

**Two-tier dispatch in `query_tutor`:**
```python
def query_tutor(user_message, language, rag_context):
    from config import TIER_1_LANGS, TIER_2_LANGS
    if language in TIER_1_LANGS:
        # Direct generation in target language
        return _ollama_generate(_build_tutor_prompt(user_message, language, rag_context))
    elif language in TIER_2_LANGS:
        # Generate in English, then bridge-translate
        english_answer = _ollama_generate(_build_tutor_prompt(user_message, "English", rag_context))
        return _bridge_translate(english_answer, language)
    else:
        # Unknown language — fall back to English
        return _ollama_generate(_build_tutor_prompt(user_message, "English", rag_context))
```

Implementation notes:
- Base URL and model read from environment (`OLLAMA_BASE`, `OLLAMA_MODEL`)
- All requests wrapped in try/except; graceful fallback strings on error
- Use `/api/generate` for single-turn completions
- `_ollama_generate(prompt, temperature, max_tokens)` is a private helper
  called by all public functions to avoid duplication

**Done check:**
```bash
python -c "
from core.llm_engine import query_tutor, generate_quiz
print(query_tutor('What is the water cycle?', 'English', ''))
print(query_tutor('What is the water cycle?', 'Iban', ''))  # Tier-2 bridge
print(generate_quiz('water cycle', 'English', ''))
"
```

---

## STEP 5 — Create `core/voice_engine.py`

**Goal:** Speech-to-text via Whisper.cpp and text-to-speech via Piper TTS.

**Create:** `core/voice_engine.py`

Key functions:
- `speech_to_text(audio_bytes: bytes) -> str`
  - Saves bytes to a temp `.webm` file
  - Runs `ffmpeg -i input.webm -ar 16000 -ac 1 output.wav`
  - Runs `whisper.cpp/main -m models/whisper/ggml-base.en.bin -f output.wav`
  - Reads `.txt` output file; falls back to stdout
  - Returns empty string if binary missing (degrades gracefully)
- `text_to_speech(text: str) -> bytes`
  - Runs `models/piper/piper --model models/piper/en_US-lessac-medium.onnx
    --output_file /tmp/out.wav`, pipes text via stdin
  - Returns WAV bytes; returns `b""` if Piper missing
- `generate_podcast_audio(script: str) -> bytes`
  - Extracts dialogue lines after `:`, joins with ` ... `
  - Calls `text_to_speech` on combined text
  - Returns WAV bytes

Implementation notes:
- All subprocess calls use `timeout=` to prevent hangs
- Temp files use `uuid.uuid4()` names to prevent collisions
- Temp files cleaned up in `finally` blocks

**Done check:**
```bash
python -c "
from core.voice_engine import text_to_speech
wav = text_to_speech('Hello, I am EduNode.')
print('WAV bytes:', len(wav), '(0 = Piper not installed, OK for now)')
"
```

---

## STEP 6 — Create `core/quiz_engine.py`

**Goal:** Validate and score quiz JSON returned by the SLM.

**Create:** `core/quiz_engine.py`

Key functions:
- `validate_questions(raw: list) -> list[dict]`
  - Filters to items that have `question` (str), `options` (list of 4), `answer`
    (one of A/B/C/D)
  - Returns cleaned list (max 5 items)
- `score_attempt(questions: list, answers: dict) -> dict`
  - `answers` is `{question_index: "A"|"B"|"C"|"D"}`
  - Returns `{"score": int, "total": int, "pct": float,
    "correct": [bool, ...], "feedback": [str, ...]}`

**Done check:**
```bash
python -c "
from core.quiz_engine import validate_questions, score_attempt
qs = [{'question':'What is 2+2?','options':['A. 3','B. 4','C. 5','D. 6'],'answer':'B'}]
print(score_attempt(qs, {0: 'B'}))
"
```

---

## STEP 7 — Create `core/progress_tracker.py`

**Goal:** SQLite-backed student progress, session logging, and badge rules engine.

**Create:** `core/progress_tracker.py`

Key functions:
- `init_db()` — creates all tables on first run:
  - `students (id, name, language, grade, created_at)`
  - `sessions (id, student_id, subject, message_count, started_at, ended_at)`
  - `quiz_results (id, student_id, topic, score, total, taken_at)`
  - `badges (id, student_id, badge_name, description, earned_at)`
  - `dialect_logs (id, language, raw_input, detected_dialect_variant, logged_at)`
- `get_or_create_student(name, language, grade) -> int` — returns `student_id`
- `log_quiz_result(student_id, topic, score, total)`
- `check_and_award_badges(student_id)` — evaluates badge rules, inserts new ones
- `get_progress(student_id) -> dict` — returns badges + recent quiz results

**Badge rules:**

| Badge | Rule |
|---|---|
| First Step | ≥ 1 session |
| Quiz Ace | Any quiz score = 100 % |
| Week Warrior | Active on ≥ 7 distinct calendar days |
| Dialect Pioneer | ≥ 10 non-English inputs logged |

**Done check:**
```bash
python -c "
from core.progress_tracker import init_db, get_or_create_student
init_db()
sid = get_or_create_student('Test Student', 'English', 7)
print('student_id:', sid)
"
```

---

## STEP 8 — Create `core/microcredential_engine.py`

**Goal:** Check if a student has earned a microcredential and generate a PDF
certificate using ReportLab.

**Create:** `core/microcredential_engine.py`

Key functions:
- `MICROCREDENTIALS` dict — topic → `{min_score_pct, quizzes_required}`
- `check_eligibility(student_id, topic) -> bool`
  - Queries `quiz_results` for matching topic
  - Returns True if count ≥ required AND average ≥ min_score_pct
- `generate_certificate_pdf(student_name, topic, student_id) -> str`
  - Creates A4 PDF in `static/certificates/`
  - Includes: title, student name, topic, date, UNESCO alignment note
  - Returns file path

**Done check:**
```bash
python -c "
from core.microcredential_engine import generate_certificate_pdf
path = generate_certificate_pdf('Alinta Watson', 'Science Literacy', 1)
print('PDF:', path)
"
```

---

## STEP 9 — Create `core/p2p_share.py`

**Goal:** Generate a local LAN share link + QR code for any piece of content
(quiz result, AI summary, etc.). Works entirely within the Pi's WiFi bubble.

**Create:** `core/p2p_share.py`

Key functions:
- `create_share(content: str, content_type: str) -> dict`
  - Saves content JSON to `static/shared/<uuid8>.json` with expiry timestamp
  - Generates QR code PNG at `static/shared/<uuid8>_qr.png`
  - Returns `{share_id, local_url, qr_image_path, expires_at}`
- `get_shared_content(share_id: str) -> dict | None`
  - Returns content dict; returns None and deletes file if expired

**Security notes:**
- `share_id` is 8 hex chars from `uuid4()` — unguessable on a local network
- Expiry default: 30 minutes (configurable)
- Content is stored server-side; QR just carries the URL

**Done check:**
```bash
python -c "
from core.p2p_share import create_share, get_shared_content
s = create_share('Test content', 'text')
print(s)
print(get_shared_content(s['share_id']))
"
```

---

## STEP 10 — Create `core/podcast_engine.py`

**Goal:** Thin wrapper that combines LLM script generation with TTS audio synthesis.

**Create:** `core/podcast_engine.py`

Key functions:
- `generate_podcast(topic: str, language: str) -> dict`
  - Calls `llm_engine.generate_podcast_script(topic, language)`
  - Calls `voice_engine.generate_podcast_audio(script)`
  - Saves WAV to `data/audio/<uuid>.wav`
  - Returns `{"script": str, "audio_path": str}`

**Done check:**
```bash
python -c "
from core.podcast_engine import generate_podcast
result = generate_podcast('photosynthesis', 'English')
print('Script lines:', result['script'].count('MAYA:') + result['script'].count('NIKO:'))
"
```

---

## STEP 11 — Create `core/flashcard_engine.py`

**Goal:** Generate structured flashcard data (title, body text, optional image
filename) from a topic and curriculum context.

**Create:** `core/flashcard_engine.py`

Key functions:
- `generate_flashcards(topic: str, language: str, rag_context: str) -> list[dict]`
  - Prompts the SLM to return 5 flashcards as JSON:
    `[{"title": "...", "body": "...", "image": "water_cycle.png or null"}]`
  - Falls back to `[]` on parse error

**Done check:**
```bash
python -c "
from core.flashcard_engine import generate_flashcards
cards = generate_flashcards('water cycle', 'English', '')
print(f'{len(cards)} cards generated')
"
```

---

## STEP 12 — Create `app.py`

**Goal:** The main Flask server. Replaces `asean_ai_tutor_project.py` as the
production entry point.

**Create:** `app.py`

Routes to implement:

```
GET  /                        → home.html
GET  /chat                    → chat.html
GET  /quiz                    → quiz.html
GET  /flashcard               → flashcard.html
GET  /podcast                 → podcast.html
GET  /progress                → progress.html
GET  /admin                   → admin.html  (admin token required)
GET  /qr                      → PNG QR code
GET  /api/status              → {ollama, tts, stt, docs, model}

POST /api/chat                → {response}
POST /api/voice/stt           → {text}
POST /api/voice/tts           → WAV audio stream
POST /api/quiz/generate       → {questions: [...]}
POST /api/quiz/submit         → {status, microcredentials_earned}
POST /api/podcast/generate    → {script, audio_url}
GET  /api/podcast/audio       → WAV audio stream
POST /api/share/create        → {share_id, local_url, qr_image_path}
GET  /share/<share_id>        → share_view.html
GET  /api/progress/<id>       → {badges, recent_quizzes}
POST /api/ingest              → {message, chunks}   [admin]
GET  /api/sources             → {sources}           [admin]
GET  /api/audio/<filename>    → WAV audio stream
```

On startup:
```python
with app.app_context():
    init_db()
    ingest_pdfs("data/curriculum")
```

**Done check:**
```bash
ollama serve &
python app.py
# curl http://localhost:5000/api/status
# → {"ollama": true, "tts": false, "stt": false, "docs": 0, "model": "..."}
```

---

## STEP 13 — Create `templates/base.html`

**Goal:** Shared layout for all pages — navbar, offline indicator, PWA meta tags.

**Create:** `templates/base.html`

Must include:
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- `<link rel="manifest" href="/static/icons/manifest.json">`
- Navigation bar with links to Chat, Quiz, Podcast, Progress
- `{% block content %}{% endblock %}`
- Offline banner (hidden by default; shown via JS when `navigator.onLine` is false)

---

## STEP 14 — Create `templates/home.html`

**Goal:** Landing page — subject and language picker, links to features.

**Create:** `templates/home.html` (extends `base.html`)

Must include:
- Welcome message with hub region name (`{{ region }}`)
- Language selector (populated from `{{ languages }}`)
- Subject grid (Math, Science, English, etc.) as large tap-friendly cards
- Each card links to `/chat?subject=Mathematics` etc.

---

## STEP 15 — Update `templates/chat.html`

**Goal:** Replace the existing `index.html`-style single page with a proper
chat page that extends `base.html`, includes language selector, and integrates
with `/api/chat`, `/api/voice/stt`, `/api/voice/tts`.

**Edit:** `templates/chat.html` (already has a good implementation from the
architecture plan — port it to extend `base.html` and wire up the correct routes)

Key JS behaviour:
- Send button → `POST /api/chat` → display AI answer bubble
- Voice button (hold) → `MediaRecorder` → `POST /api/voice/stt` → auto-send transcript
- AI answer → `POST /api/voice/tts` → `new Audio(...).play()` auto-plays
- Language selector saved to `localStorage` so it persists across page loads

---

## STEP 16 — Create `templates/quiz.html`

**Goal:** MCQ quiz UI — topic input, generate button, clickable answer options,
score display.

**Create:** `templates/quiz.html` (extends `base.html`)

JS flow:
1. User types topic → clicks "Generate Quiz"
2. `POST /api/quiz/generate` → receive `{questions: [...]}`
3. Render each question with 4 option buttons
4. On submit → `POST /api/quiz/submit` → show score + any earned microcredentials
5. If certificate earned → show download link

---

## STEP 17 — Create `templates/podcast.html`

**Goal:** Topic input → generate MAYA/NIKO script → auto-play audio.

**Create:** `templates/podcast.html` (extends `base.html`)

JS flow:
1. User types topic + selects language
2. `POST /api/podcast/generate` → `{script, audio_url}`
3. Display formatted script (MAYA: in blue, NIKO: in green)
4. `<audio>` element auto-plays the returned URL

---

## STEP 18 — Create `templates/progress.html`

**Goal:** Student badge wall and recent quiz history.

**Create:** `templates/progress.html` (extends `base.html`)

JS flow:
1. `GET /api/progress/<student_id>` on page load
2. Render badge cards (earned badges lit up; locked badges greyed out)
3. Render quiz history table with topic, score, date
4. If any certificate PDF exists → show download button

---

## STEP 19 — Create `templates/share_view.html`

**Goal:** Display shared content when a student scans a QR code.

**Create:** `templates/share_view.html` (extends `base.html`)

Displays:
- Shared content (text, quiz result, or AI summary)
- "Open in Tutor" button to continue the conversation
- Expiry countdown

---

## STEP 20 — Create `templates/flashcard.html`

**Goal:** Swipeable slide carousel of AI-generated flashcards.

**Create:** `templates/flashcard.html` (extends `base.html`)

JS flow:
1. Topic input → `POST /api/flashcard/generate`
2. Render cards as a CSS `overflow-x: scroll` snap carousel
3. Swipe left/right (touch events) or arrow buttons

---

## STEP 21 — Create `static/js/` module files

**Goal:** Split `static/js/app.js` into focused modules consumed by each page.

**Create each file with the behaviour described:**

### `static/js/chat.js`
- `sendMessage(text)` → fetch + render bubble
- `startRecording()` / `stopRecording()` using `MediaRecorder`
- Auto-play TTS audio after AI response
- Persist language choice in `localStorage`

### `static/js/quiz.js`
- `generateQuiz(topic, language)` → render question cards
- `submitQuiz()` → POST scores → show result + cert link

### `static/js/flashcard.js`
- `generateFlashcards(topic)` → render carousel
- Touch/swipe event listeners + keyboard arrow support

### `static/js/podcast.js`
- `generatePodcast(topic, language)` → render script + `<audio>`
- Speaker colour-coding (MAYA / NIKO)

---

## STEP 22 — Create `static/icons/manifest.json`

**Goal:** PWA manifest so students can "Add to Home Screen" on Android.

**Create:** `static/icons/manifest.json`

```json
{
  "name": "EduNode",
  "short_name": "EduNode",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#f0f4f8",
  "theme_color": "#1a6b3c",
  "icons": [
    { "src": "/static/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

Also create `icon-192.png` and `icon-512.png` (simple green leaf icon).
Can use any free icon generator; exact design not critical for PoC.

**Done check:** Open Chrome DevTools → Application → Manifest → no errors.

---

## STEP 23B — Create `tools/build_hub_image.py`

**Goal:** Generate a per-region configuration package (a ready-to-flash Pi
image config bundle) so teachers receive a single USB drive per hub — plug in,
flash, done. Zero configuration required on-site.

**Create:** `tools/build_hub_image.py`

```bash
python tools/build_hub_image.py --hub sarawak
# → builds/edunode_sarawak/
#     config.py          (sarawak block uncommented, all others removed)
#     wifi_setup.sh      (sets SSID to "EduNode_Sarawak", IP to 192.168.1.1)
#     kolibri_setup.sh   (imports the correct Kolibri channel for this hub)
#     data/glossaries/   (only the glossaries needed for this hub's Tier-2 langs)
#     DEPLOY.md          (one-page deploy instructions in the hub's Tier-1 language)
```

**What the script does:**

1. Reads `HUB_CONFIGS` dict — all 13 hubs defined inline
2. For the target `--hub` flag:
   - Generates a `config.py` with only that hub's block active
   - Generates `wifi_setup.sh`:
     ```bash
     nmcli dev wifi hotspot ifname wlan0 ssid "EduNode_Sarawak" password "edunode2026"
     nmcli connection modify "EduNode_Sarawak" ipv4.addresses 192.168.1.1/24
     ```
   - Generates `kolibri_setup.sh` with the correct channel import command
   - Copies only the relevant glossary JSON files for Tier-2 languages
   - Writes `DEPLOY.md` in the hub's primary Tier-1 language
3. Creates `builds/edunode_<hub_id>.tar.gz` — the teacher USB payload

**HUB_CONFIGS structure in the script:**
```python
HUB_CONFIGS = {
    "singapore":           {"region": "Singapore",            "tier1": ["English"],                        "tier2": [],                  "ssid": "EduNode_Singapore",    "kolibri_lang": "en"},
    "vietnam":             {"region": "Vietnam",              "tier1": ["English", "Vietnamese"],           "tier2": ["Hmong"],           "ssid": "EduNode_Vietnam",      "kolibri_lang": "vi"},
    "sarawak":             {"region": "Sarawak, Malaysia",    "tier1": ["English", "Bahasa Melayu"],        "tier2": ["Iban", "Kedayan"], "ssid": "EduNode_Sarawak",      "kolibri_lang": "en"},
    "west_java":           {"region": "West Java, Indonesia", "tier1": ["English", "Bahasa Indonesia"],    "tier2": ["Sundanese"],       "ssid": "EduNode_WestJava",     "kolibri_lang": "id"},
    "visayas":             {"region": "Visayas, Philippines", "tier1": ["English", "Filipino"],            "tier2": ["Cebuano"],         "ssid": "EduNode_Visayas",      "kolibri_lang": "en"},
    "isan":                {"region": "Isan, Thailand",       "tier1": ["English", "Thai"],                "tier2": ["Isan"],            "ssid": "EduNode_Isan",         "kolibri_lang": "th"},
    "cambodia":            {"region": "Rural Cambodia",       "tier1": ["English", "Khmer"],               "tier2": [],                  "ssid": "EduNode_Cambodia",     "kolibri_lang": "km"},
    "laos":                {"region": "Rural Laos",           "tier1": ["English", "Lao"],                 "tier2": [],                  "ssid": "EduNode_Laos",         "kolibri_lang": "lo"},
    "shan":                {"region": "Shan State, Myanmar",  "tier1": ["English"],                        "tier2": ["Shan"],            "ssid": "EduNode_Shan",         "kolibri_lang": "en"},
    "timor_leste":         {"region": "Timor-Leste",          "tier1": ["English"],                        "tier2": ["Tetum"],           "ssid": "EduNode_TimorLeste",   "kolibri_lang": "en"},
    "brunei":              {"region": "Brunei Darussalam",    "tier1": ["English", "Bahasa Melayu"],        "tier2": ["Kedayan"],         "ssid": "EduNode_Brunei",       "kolibri_lang": "en"},
    "kalimantan":          {"region": "Kalimantan, Indonesia","tier1": ["English", "Bahasa Indonesia"],    "tier2": ["Dayak"],           "ssid": "EduNode_Kalimantan",   "kolibri_lang": "id"},
    "peninsular_malaysia": {"region": "Peninsular Malaysia",  "tier1": ["English", "Bahasa Melayu"],        "tier2": [],                  "ssid": "EduNode_Malaysia",     "kolibri_lang": "ms"},
}
```

**Done check:**
```bash
python tools/build_hub_image.py --hub sarawak
ls builds/edunode_sarawak/
# config.py  wifi_setup.sh  kolibri_setup.sh  data/  DEPLOY.md
python tools/build_hub_image.py --list
# Lists all 13 available hub IDs
```

---

## STEP 23B — Create `sneakernet_sync.py`

**Goal:** Run by the teacher when plugging in the monthly USB drive.

**Create:** `sneakernet_sync.py`

```
python sneakernet_sync.py --usb /media/usb0
```

Steps the script performs:
1. Copy `USB/new_curriculum/*.pdf` → `data/curriculum/`
2. Call `ingest_pdfs()` to re-index (idempotent)
3. Run `USB/model_update.sh` if present
4. Copy `db/edunode.db` → `USB/exported_reports/progress_YYYYMMDD.db`
5. Export `dialect_logs` table as JSON → `USB/exported_reports/dialect_logs_YYYYMMDD.json`
6. Print summary report

---

## STEP 24 — Update `requirements.txt`

**Final state of `requirements.txt`:**

```
flask>=3.0
chromadb>=0.5
sentence-transformers>=3.0
pypdf>=4.0
qrcode[pil]>=7.4
pillow>=10.0
requests>=2.31
python-dotenv>=1.0
gunicorn>=22.0
reportlab>=4.0
```

---

## STEP 25 — End-to-End Integration Test

Run this sequence to validate everything works together:

```bash
# Terminal 1
ollama serve

# Terminal 2
cp .env.example .env   # if not done already
python app.py

# Terminal 3 — run the smoke tests
curl http://localhost:5000/api/status
# Expected: {"ollama": true, ...}

curl -s -X POST http://localhost:5000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "water cycle", "language": "English"}' | python -m json.tool
# Expected: {"questions": [{...}, {...}, {...}]}

curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is photosynthesis?", "language": "English", "student_id": 1}' \
  | python -m json.tool
# Expected: {"response": "..."}
```

---

## STEP 26 — Raspberry Pi Hardware Deploy

1. Flash Raspberry Pi OS Bookworm (64-bit) to SSD
2. `ssh pi@raspberrypi.local`
3. `git clone https://github.com/YOUR_USERNAME/EduNode.git && cd EduNode`
4. `bash setup.sh`
5. Configure router: Pi static IP = `192.168.1.1`
6. `cp .env.example .env && nano .env` — set `ADMIN_TOKEN`
7. Start:
   ```bash
   ollama serve &
   gunicorn -w 2 -b 0.0.0.0:5000 'app:app'
   ```
8. From an Android phone on the Pi's WiFi: open `http://192.168.1.1` in Chrome
9. Tap the ⋮ menu → "Add to Home Screen"

---

## Sprint Summary

| Week | Steps | Deliverable |
|---|---|---|
| **Week 1** | 0–12 | Core brain: chat + quiz + Tier-2 bridge mode working on laptop |
| **Week 2** | 13–21 | Voice + full UI: speak a question, hear the answer |
| **Week 3** | 1A, 1B, 22–23B | Kolibri+Khan Academy, glossaries, USB sync, P2P share |
| **Week 4** | 23C, 24–26 | Hub image builder, Pi hardware deploy, demo-ready |

---

## Demo Script for Judges (2 minutes)

```
1. Show Pi + solar panel + router — "no internet, no power grid needed"
2. Connect Android phone to "EduNode_Sarawak" WiFi
3. Open Chrome → http://192.168.1.1 → EduNode home loads instantly
4. Pick "Cebuano" language, select "Mathematics"
5. HOLD voice button → speak in Cebuano → AI answers from curriculum PDF
6. Tap "Generate Quiz" → 3 MCQ questions → answer → score + badge
7. Tap "Podcast" → MAYA/NIKO audio plays on topic
8. Tap "Share" → QR code → second phone scans → sees same quiz
9. Teacher plugs USB → sync script runs → progress exported
10. Show microcredential PDF certificate
```

---

## File Creation Checklist

```
[x] STEP 0    requirements.txt              (reportlab added)
[x] STEP 1    config.py                     (all 13 hubs, two-tier)
[x] STEP 1A   tools/download_glossaries.py  (HuggingFace Cebuano + Iban datasets)
[x] STEP 1B   tools/kolibri_to_rag.py       (Kolibri article text → RAG PDFs)
              setup.sh update               (Kolibri install + Khan Academy channel)
[x] STEP 2    core/__init__.py
[x] STEP 3    core/rag_engine.py
[x] STEP 4    core/llm_engine.py            (+ Tier-2 bridge-mode translate layer)
[x] STEP 5    core/voice_engine.py
[x] STEP 6    core/quiz_engine.py
[x] STEP 7    core/progress_tracker.py
[x] STEP 8    core/microcredential_engine.py
[x] STEP 9    core/p2p_share.py
[x] STEP 10   core/podcast_engine.py
[x] STEP 11   core/flashcard_engine.py
[x] STEP 12   app.py                        (+ /api/status kolibri field)
[x] STEP 13   templates/base.html           (+ "Open in Kolibri" nav link)
[x] STEP 14   templates/home.html
[x] STEP 15   templates/chat.html           (update)
[x] STEP 16   templates/quiz.html
[x] STEP 17   templates/podcast.html
[x] STEP 18   templates/progress.html
[x] STEP 19   templates/share_view.html
[x] STEP 20   templates/flashcard.html
[x] STEP 21   static/js/chat.js
[x] STEP 21   static/js/quiz.js
[x] STEP 21   static/js/flashcard.js
[x] STEP 21   static/js/podcast.js
[x] STEP 22   static/icons/manifest.json
[x] STEP 22   static/icons/icon-192.png
[x] STEP 22   static/icons/icon-512.png
[x] STEP 23   tools/build_hub_image.py      (13 hub image builder)
[x] STEP 23B  sneakernet_sync.py
[x] STEP 24   requirements.txt              (final check — already complete)
[x] STEP 25   Integration test
[ ] STEP 26   Pi hardware deploy
```
