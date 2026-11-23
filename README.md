# Meras Studio | مِراس
### Automated Kurzgesagt-Style Vector Animation Production Engine

Automated, local motion graphics studio built for the YouTube channel **"Meras | مِراس"** (Behavioral Psychology, Cognitive Engineering, and Hidden Human Mechanics).

---

## 🏛️ Architecture Overview

```
meras_studio/
├── .env                         # Azure Speech credentials (AZURE_SPEECH_KEY, AZURE_SPEECH_REGION)
├── episodes_roadmap.json        # 30-episode viral roadmap (episodes 1 to 30)
├── run_studio.py                # Master CLI orchestrator
├── assets/
│   ├── sfx/                     # High-precision procedural audio kit
│   │   ├── pop.wav              # Tactile vector pop (frequency sweep + transient)
│   │   ├── blip.wav             # UI chime (harmonic bell tones)
│   │   ├── whoosh.wav           # Swept resonant bandpass noise with stereo pan
│   │   ├── sparkle.wav          # Insight ding (cascading chime arpeggio)
│   │   ├── deep_pulse.wav       # Sub-bass revelation pulse with analog saturation
│   │   └── meras_ambient.wav    # Warm, loopable cosmic ambient synth bed
│   ├── fonts/                   # Montserrat and Inter typography
│   ├── watermark.png            # Meras vector brand watermark badge
│   └── gsap.min.js              # Standalone GreenSock Animation Platform library
├── engine/
│   ├── __init__.py
│   ├── voice_engine.py          # Stage 1: Azure TTS (BrianMultilingualNeural) + Whisper alignment
│   ├── kurzgesagt_art_kit.py    # Stage 2: Flat 2.5D SVG/HTML5 procedural art kit & GSAP timeline
│   ├── motion_renderer.py       # Stage 3: Headless Chromium 60fps 1080p motion renderer
│   ├── compositor.py            # Stage 4: FFmpeg master transitions, audio mix, and export
│   ├── thumbnail_gen.py         # Stage 4: 1280x720 viral vector thumbnail generator
│   └── sfx_generator.py         # Procedural SFX synthesis engine (NumPy + SciPy)
└── output/
    └── episode_01/
        ├── final_video.mp4      # 1080p 60fps CRF 17 master cut
        └── thumbnail.png        # 1280x720 viral vector thumbnail
```

---

## 🎨 Brand & Visual Identity ("Meras | مِراس")

* **Visual Style:** Kurzgesagt-inspired Flat 2.5D vector illustration.
* **Outlines:** NO harsh black strokes. Shapes are sculpted exclusively via rich multi-stop gradients and color contrast.
* **Canvas:** Deep cosmic obsidian backgrounds (`#090D24` to `#161B40`) with parallax particle dust and glowing light beams.
* **Accents:** Electric Cyan (`#00E5FF`), Coral Magenta (`#FF3B6B`), Warm Amber (`#FFB800`), Royal Violet (`#6C2BD9`).
* **Mascot:** **The Meras Explorer** — a sleek, geometric, faceless minimalist character with an illuminated cyan/amber cape and specular gloss visor.
* **UI Elements:** Rounded pill-shaped badges with pointer triangles and witty micro-speech bubbles synced to spoken keywords.

---

## 🚀 Running the Studio

### 1. Configure Azure Speech
Edit `.env` and insert your Azure Cognitive Services Speech key and region:
```env
AZURE_SPEECH_KEY=your_actual_key_here
AZURE_SPEECH_REGION=eastus
```
*(If unconfigured, the engine automatically activates its high-fidelity local fallback synthesizer so development and rendering never halt.)*

### 2. Render Any Episode
To produce Episode 1:
```bash
python run_studio.py --episode 1
```

To run a verification test:
```bash
python run_studio.py --test
```

Custom framerate:
```bash
python run_studio.py --episode 1 --fps 60
```
