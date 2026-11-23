# Meras Studio | مِراس
### Automated Kurzgesagt-Style Vector Animation Production Engine

Automated, broadcast-grade motion graphics studio built for the YouTube channel **"Meras | مِراس"** (Behavioral Psychology, Cognitive Engineering, and Hidden Human Mechanics).

---

## 🏛️ Architecture Overview

```
meras_studio/
├── .env                         # API credentials (AZURE_SPEECH_KEY, GEMINI_API_KEY)
├── episodes_roadmap.json        # 30-episode viral roadmap (episodes 1 to 30)
├── run_studio.py                # Master CLI orchestrator & preflight verification
├── produce_episode_01.py        # Dedicated 1-click launcher for Episode 01
├── requirements.txt             # Python dependencies (google-genai, faster-whisper, etc.)
├── assets/
│   ├── sfx/                     # High-precision procedural audio kit (48kHz stereo)
│   │   ├── ambient_bed.wav      # Dynamic ambient synth bed (-24dB to -20dB)
│   │   ├── air_whoosh.wav       # Smooth scene transition sweep
│   │   ├── gentle_chime.wav     # Chapter transition & insight chime
│   │   ├── soft_pop.wav         # Tactile metric & vector pop
│   │   └── sub_drop.wav         # Dramatic revelation sub-bass impact
│   ├── fonts/                   # Montserrat-Bold.ttf & Inter-Regular.woff2 (base64 embedded)
│   ├── watermark.png            # Meras vector brand watermark badge
│   └── gsap.min.js              # Standalone GreenSock Animation Platform library (v3.12.5)
├── engine/
│   ├── __init__.py
│   ├── dynamic_producer.py      # Dynamic Gemini 2.5 Flash & Algorithmic Director
│   ├── episode_generator.py     # Script planning, chapter structuring & word-binding
│   ├── voice_engine.py          # Andrew voice synthesis & faster-whisper alignment
│   ├── kurzgesagt_art_kit.py    # Flat 2.5D SVG/HTML5 procedural art kit & GSAP timeline
│   ├── motion_renderer.py       # Deterministic 30fps headless Chromium renderer (JPEG pipe)
│   ├── compositor.py            # 48kHz audio mix, xfade stitching & loudnorm mastering
│   ├── thumbnail_gen.py         # 1280x720 viral vector thumbnail generator
│   └── sfx_generator.py         # Procedural SFX synthesis engine (NumPy + SciPy)
└── output/
    └── EP_1/                    # Final Episode 01 production exports
        ├── final_video.mp4      # 1080p 30fps master cut (-14 LUFS stereo)
        ├── short_video.mp4      # 60s 9:16 vertical YouTube Short with branded typography
        ├── thumbnail.png        # 1280x720 viral vector thumbnail
        └── youtube_metadata.txt # 3 High-CTR titles, SEO description, chapter timestamps & tags
```

---

## 🎨 Production & Engineering Standards

* **Framerate & Rendering:** Deterministic **30fps** master clock (true Kurzgesagt/Vox broadcast standard). Renders via fast in-memory JPEG piping into FFmpeg (`-framerate 30 -f image2pipe`), cutting render times by 50% with zero stutter.
* **Visual Style:** Kurzgesagt-inspired **Flat 2.5D filled gradient vector art** with soft inner shading and layered depth. No hollow stroked wireframes.
* **Embedded Typography:** Fonts (`Montserrat-Bold.ttf` and `Inter-Regular.woff2`) are base64-encoded directly into every HTML/SVG document, guaranteeing zero font popping across all environments.
* **Camera Dynamics:** Deterministic camera motion presets (`push_in`, `pull_out`, `pan_right`, `pan_left`) provide subtle mid-scene kinetic energy without jarring transitions.
* **Audio Engineering:**
  * **Voice:** Signature youthful `en-US-AndrewMultilingualNeural` (rate `+2%`, pitch `0%`) with `<sub alias="Miras">Meras</sub>` SSML pronunciation lock.
  * **Alignment:** Word-level timestamp extraction via `faster-whisper` (`base.en` model).
  * **Mastering:** 48kHz float32 internal mixing, seamless 1.5s crossfade looping, and YouTube broadcast loudness normalization (`loudnorm=I=-14:TP=-1:LRA=11`).
* **Zero-Drift Timeline Math:** Contiguous timeline derivation with hard per-scene caps ($\le 14.0\text{s}$) and exact `ffprobe` stream validation, eliminating audio-visual desync permanently.
* **Safe Server Priority:** Adaptive 2-worker concurrency running at `BELOW_NORMAL_PRIORITY_CLASS` / `nice -n 10` with FFmpeg `-threads 2`, keeping other server services completely responsive.

---

## 🚀 Running the Studio

### 1. Environment Configuration (`.env`)
Create or edit `.env` in the root directory:
```env
# Optional: Azure Speech Service (Neural Andrew voice)
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=eastus

# Optional: Google Gemini API (Dynamic script & metadata generation)
GEMINI_API_KEY=your_gemini_api_key_here
```
*(If unconfigured, the engine automatically falls back to cross-platform edge-tts for voice and the offline algorithmic documentary director for scripts.)*

### 2. Produce Episode 1
To produce the full broadcast master for Episode 1:
```bash
python produce_episode_01.py
```
Or via the master CLI:
```bash
python run_studio.py --episode 1
```

### 3. Verification Test
To run a fast multi-scene verification test:
```bash
python run_studio.py --verify
```
