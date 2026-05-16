# =============================================================================
# config.py — Geo-Specific Edge Deployment Configuration
# Change this file per Hub deployment region.
# All other modules import from here — do NOT hard-code region values elsewhere.
#
# LANGUAGE TIERS:
#   Tier 1 — Full AI response generated directly in the language.
#             LLM has sufficient training data; "respond in {language}" works.
#   Tier 2 — Bridge mode. AI generates in English → key terms translated via
#             glossary datasets (HuggingFace). Output shown bilingually.
#             Used for deep-minority languages with <1 MB of training data.
#
# HUB IDENTIFIERS (used by tools/build_hub_image.py):
#   HUB_ID   — short snake_case name, becomes the WiFi SSID suffix and
#               the Pi image filename: edunode_<HUB_ID>.img
# =============================================================================

# =============================================================================
# TIER 1 HUBS — Full AI generation in all listed languages
# =============================================================================

# ── 1. SINGAPORE HUB ─────────────────────────────────────────────────────
HUB_ID        = "asean_hub"
HUB_REGION    = "Rural ASEAN"
HUB_LANGUAGES = [
    "English",
    "Bahasa Melayu",
    "Bahasa Indonesia",
    "Filipino",
    "Thai",
    "Vietnamese",
    "Khmer",
    "Lao",
    "Burmese",
    "Cebuano",
    "Iban",
]
TIER_1_LANGS  = ["English"]
TIER_2_LANGS  = []
SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
HUB_IP        = "192.168.1.1"
WIFI_SSID     = "EduNode_Hub"
KOLIBRI_CHANNEL = "en"

# ── 2. VIETNAM HUB ───────────────────────────────────────────────────────
# HUB_ID        = "vietnam"
# HUB_REGION    = "Vietnam"
# HUB_LANGUAGES = ["English", "Vietnamese", "Hmong"]
# TIER_1_LANGS  = ["English", "Vietnamese"]
# TIER_2_LANGS  = ["Hmong"]   # bridge mode — mountainous north VN minority
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Vietnam"
# KOLIBRI_CHANNEL = "vi"

# ── 3. MALAYSIA / BRUNEI — SARAWAK HUB ───────────────────────────────────
# HUB_ID        = "sarawak"
# HUB_REGION    = "Sarawak, Malaysia"
# HUB_LANGUAGES = ["English", "Bahasa Melayu", "Iban", "Kedayan"]
# TIER_1_LANGS  = ["English", "Bahasa Melayu"]
# TIER_2_LANGS  = ["Iban", "Kedayan"]  # bridge mode — Borneo indigenous
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Sarawak"
# KOLIBRI_CHANNEL = "en"

# ── 4. INDONESIA — WEST JAVA HUB ─────────────────────────────────────────
# HUB_ID        = "west_java"
# HUB_REGION    = "West Java, Indonesia"
# HUB_LANGUAGES = ["English", "Bahasa Indonesia", "Sundanese"]
# TIER_1_LANGS  = ["English", "Bahasa Indonesia"]
# TIER_2_LANGS  = ["Sundanese"]  # bridge mode — 40M speakers, underrepresented
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_WestJava"
# KOLIBRI_CHANNEL = "id"

# ── 5. PHILIPPINES — VISAYAS HUB ─────────────────────────────────────────
# HUB_ID        = "visayas"
# HUB_REGION    = "Visayas, Philippines"
# HUB_LANGUAGES = ["English", "Filipino", "Cebuano"]
# TIER_1_LANGS  = ["English", "Filipino"]
# TIER_2_LANGS  = ["Cebuano"]  # bridge mode + cebuano-readability dataset boost
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Visayas"
# KOLIBRI_CHANNEL = "en"

# ── 6. THAILAND — ISAN HUB ───────────────────────────────────────────────
# HUB_ID        = "isan"
# HUB_REGION    = "Isan, Northeast Thailand"
# HUB_LANGUAGES = ["English", "Thai", "Isan"]
# TIER_1_LANGS  = ["English", "Thai"]
# TIER_2_LANGS  = ["Isan"]  # bridge mode — Thai dialect, rural northeast
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Isan"
# KOLIBRI_CHANNEL = "th"

# ── 7. CAMBODIA HUB ──────────────────────────────────────────────────────
# HUB_ID        = "cambodia"
# HUB_REGION    = "Rural Cambodia"
# HUB_LANGUAGES = ["English", "Khmer"]
# TIER_1_LANGS  = ["English", "Khmer"]
# TIER_2_LANGS  = []
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Cambodia"
# KOLIBRI_CHANNEL = "km"

# ── 8. LAO PDR HUB ───────────────────────────────────────────────────────
# HUB_ID        = "laos"
# HUB_REGION    = "Rural Laos"
# HUB_LANGUAGES = ["English", "Lao"]
# TIER_1_LANGS  = ["English", "Lao"]
# TIER_2_LANGS  = []
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Laos"
# KOLIBRI_CHANNEL = "lo"

# ── 9. MYANMAR — SHAN HUB ────────────────────────────────────────────────
# HUB_ID        = "shan"
# HUB_REGION    = "Shan State, Myanmar"
# HUB_LANGUAGES = ["English", "Shan"]
# TIER_1_LANGS  = ["English"]
# TIER_2_LANGS  = ["Shan"]  # bridge mode — border region, disrupted schooling
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Shan"
# KOLIBRI_CHANNEL = "en"

# ── 10. TIMOR-LESTE HUB ──────────────────────────────────────────────────
# HUB_ID        = "timor_leste"
# HUB_REGION    = "Timor-Leste"
# HUB_LANGUAGES = ["English", "Tetum"]
# TIER_1_LANGS  = ["English"]
# TIER_2_LANGS  = ["Tetum"]  # bridge mode — ASEAN newest member, ignored by big tech
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_TimorLeste"
# KOLIBRI_CHANNEL = "en"

# ── 11. BRUNEI — KEDAYAN HUB ─────────────────────────────────────────────
# HUB_ID        = "brunei"
# HUB_REGION    = "Brunei Darussalam"
# HUB_LANGUAGES = ["English", "Bahasa Melayu", "Kedayan"]
# TIER_1_LANGS  = ["English", "Bahasa Melayu"]
# TIER_2_LANGS  = ["Kedayan"]  # bridge mode — Borneo indigenous, cross-border
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Brunei"
# KOLIBRI_CHANNEL = "en"

# ── 12. INDONESIA — KALIMANTAN HUB ───────────────────────────────────────
# HUB_ID        = "kalimantan"
# HUB_REGION    = "Kalimantan, Indonesia"
# HUB_LANGUAGES = ["English", "Bahasa Indonesia", "Dayak"]
# TIER_1_LANGS  = ["English", "Bahasa Indonesia"]
# TIER_2_LANGS  = ["Dayak"]  # bridge mode — Borneo indigenous
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Kalimantan"
# KOLIBRI_CHANNEL = "id"

# ── 13. MALAYSIA — PENINSULAR HUB ────────────────────────────────────────
# HUB_ID        = "peninsular_malaysia"
# HUB_REGION    = "Peninsular Malaysia"
# HUB_LANGUAGES = ["English", "Bahasa Melayu"]
# TIER_1_LANGS  = ["English", "Bahasa Melayu"]
# TIER_2_LANGS  = []
# SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
# HUB_IP        = "192.168.1.1"
# WIFI_SSID     = "EduNode_Malaysia"
# KOLIBRI_CHANNEL = "ms"

# =============================================================================
# GLOSSARY DATASETS (HuggingFace) — used by Tier-2 bridge mode
# Downloaded once during setup and stored in data/glossaries/
# =============================================================================
GLOSSARY_DATASETS = {
    "Cebuano": "filbench/cebuano-readability",
    "Iban":    "VynerCK/Iban-language-data",
    # Add more as community datasets become available
}

# =============================================================================
# Kolibri + Khan Academy content channel
# KOLIBRI_CHANNEL maps to the language code used in Kolibri content packs.
# Set above per hub. "en" = English Khan Academy (default fallback).
# =============================================================================
KOLIBRI_PORT = 8080   # Kolibri runs alongside EduNode on a separate port

# =============================================================================
# Subjects available on this Hub
# =============================================================================
AVAILABLE_SUBJECTS = [
    "Mathematics",
    "Science",
    "English Language",
    "Environmental Studies",
    "Digital Literacy",
]
