# Meras Studio | Secrets Manifest & Security Policy

This document defines all secrets, API keys, and environment variables recognized by **Meras Studio**.
It specifies where each secret is referenced, its required structure, and its fallback behavior when unconfigured.

---

## 1. Secrets Reference Table

| Variable Name | Service Provider | Used In Codebase | Required / Optional | Fallback Behavior When Missing |
| :--- | :--- | :--- | :--- | :--- |
| `AZURE_SPEECH_KEY` | Microsoft Azure Cognitive Services | `engine/voice_engine.py`<br/>`run_studio.py` | Optional | Automatically falls back to high-fidelity cloud Neural Edge TTS (`en-US-AndrewMultilingualNeural`). |
| `AZURE_SPEECH_REGION` | Microsoft Azure Cognitive Services | `engine/voice_engine.py`<br/>`run_studio.py` | Optional | Defaults to `eastus`. |
| `GEMINI_API_KEY` | Google AI Studio / Gemini API | `engine/episode_generator.py` | Optional | Falls back to local algorithmic script director and curated `episodes_roadmap.json`. |
| `YOUTUBE_API_KEY` | Google Cloud / YouTube Data API | `run_studio.py` | Optional | Generates formatted `youtube_metadata.txt` locally for manual copy-paste into YouTube Studio. |
| `YOUTUBE_CLIENT_SECRETS_FILE` | Google Cloud OAuth2 | `run_studio.py` | Optional | Skips direct upload API and preserves output MP4s in `output/EP_[N]/`. |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API | `run_studio.py` (Notifier) | Optional | Notifications are logged strictly to stdout/stderr. |
| `TELEGRAM_CHAT_ID` | Telegram Messenger | `run_studio.py` (Notifier) | Optional | Notifications are logged strictly to stdout/stderr. |

---

## 2. Security & Zero-Leakage Architecture

1. **Strict `.gitignore` Policy:**
   - `.env` and all `.env.*` variants (except `.env.example`) are permanently ignored by Git.
   - Private key files (`*.pem`, `*.key`, `*.pfx`, `*.p12`) and credential files (`*secret*`, `*credential*`, `token*.json`, `client_secret*.json`) are blocked at repository root and in subfolders.
2. **Environment Variable Injection:**
   - Real keys are injected strictly at runtime via `python-dotenv` (`load_dotenv()`) or OS environment variables.
   - Code never hardcodes default fallback keys or tokens.
3. **Local Media Exclusion:**
   - Output documentary renders (`output/`), temporary scene clips (`temp/`, `temp_scenes/`), and raw audio/video (`*.mp4`, `*.wav`, `*.mp3`) are excluded from Git to prevent large binary bloat.
