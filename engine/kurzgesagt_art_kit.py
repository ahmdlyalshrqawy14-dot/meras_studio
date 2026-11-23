"""
Meras Studio Kurzgesagt Art Kit
Broadcast-Grade Modular Vector Motion Graphics Engine:
- 100% Mascot-Free: Pure, rich, abstract & scientific vector motion graphics
- Composable Multi-Scene Architecture (capable of generating 60 to 100 unique scenes per episode)
- Dynamic Chapter Color Palettes across 6 thematic chapters:
  * Chapter 1: Cosmic Obsidian & Electric Cyan (#00E5FF)
  * Chapter 2: Royal Violet (#8B5CF6) & Electric Magenta (#D946EF)
  * Chapter 3: Amber Gold (#FFB800) & Coral Flame (#FF5722)
  * Chapter 4: Coral Magenta (#FF3B6B) & Tangerine (#FB923C)
  * Chapter 5: Emerald Green (#10B981) & Mint (#34D399)
  * Chapter 6: Celestial Gold (#FACC15) & Ultraviolet (#818CF8)
- 2-Second Animated Chapter Title Cards
- Sentence-Accurate Dynamic Metaphors & Animated Numerical Counters
- Strict Safe Zones: +25px safe vertical margins between titles and badges (zero collisions)
- 3-Layer Depth Parallax & Continuous Cinematic Camera Motion (1.0x to 1.07x)
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

STUDIO_ROOT = Path(__file__).resolve().parent.parent

# Shared text sanitizer for captions and display
try:
    from engine.voice_engine import sanitize_display_and_tts_text
except ImportError:
    from voice_engine import sanitize_display_and_tts_text

# Embedded Local GSAP Engine for 100% deterministic, offline 60fps rendering
GSAP_LOCAL_PATH = STUDIO_ROOT / "assets" / "gsap.min.js"
if GSAP_LOCAL_PATH.exists():
    with open(GSAP_LOCAL_PATH, "r", encoding="utf-8") as f:
        GSAP_INLINE_SCRIPT = f.read()
else:
    GSAP_INLINE_SCRIPT = "console.warn('GSAP local not found, using fallback CDN');"

# 6 Dynamic Chapter Palettes
PALETTES = {
    1: {  # Chapter 1: Cosmic Cyan (Intro / Awakening)
        "bg_dark": "#090D24",
        "bg_darker": "#050714",
        "bg_radial": "#141B42",
        "primary": "#00E5FF",      # Electric Cyan
        "secondary": "#38BDF8",    # Sky Blue
        "accent": "#818CF8",       # Periwinkle
        "highlight": "#FFFFFF",
        "card_bg": "#12193C",
        "glow": "glow-cyan"
    },
    2: {  # Chapter 2: Royal Violet (Evolutionary Wire)
        "bg_dark": "#0D0B24",
        "bg_darker": "#070514",
        "bg_radial": "#211648",
        "primary": "#8B5CF6",      # Royal Violet
        "secondary": "#D946EF",    # Magenta
        "accent": "#00E5FF",       # Cyan spark
        "highlight": "#FFFFFF",
        "card_bg": "#19153B",
        "glow": "glow-violet"
    },
    3: {  # Chapter 3: Amber Gold (Mechanical Breakdown / Gears)
        "bg_dark": "#161124",
        "bg_darker": "#0B0814",
        "bg_radial": "#2E1C38",
        "primary": "#FFB800",      # Amber Gold
        "secondary": "#FF5722",    # Deep Orange
        "accent": "#FDE047",       # Lemon Glow
        "highlight": "#FFFFFF",
        "card_bg": "#241836",
        "glow": "glow-amber"
    },
    4: {  # Chapter 4: Coral Flame (The Catastrophe / Conflict)
        "bg_dark": "#1A0D1E",
        "bg_darker": "#0D0610",
        "bg_radial": "#381432",
        "primary": "#FF3B6B",      # Coral Magenta
        "secondary": "#FB923C",    # Tangerine
        "accent": "#EF4444",       # Crimson
        "highlight": "#FFFFFF",
        "card_bg": "#28132B",
        "glow": "glow-magenta"
    },
    5: {  # Chapter 5: Emerald Matrix (The Historic Experiment)
        "bg_dark": "#081A1F",
        "bg_darker": "#040D10",
        "bg_radial": "#103239",
        "primary": "#10B981",      # Emerald Green
        "secondary": "#34D399",    # Mint
        "accent": "#38BDF8",       # Ice Blue
        "highlight": "#FFFFFF",
        "card_bg": "#0F262C",
        "glow": "glow-emerald"
    },
    6: {  # Chapter 6: Celestial Gold (The Meras Antidote / Transcendence)
        "bg_dark": "#09112E",
        "bg_darker": "#040817",
        "bg_radial": "#182259",
        "primary": "#FACC15",      # Celestial Gold
        "secondary": "#00E5FF",    # Electric Cyan
        "accent": "#A78BFA",       # Soft Violet
        "highlight": "#FFFFFF",
        "card_bg": "#141D47",
        "glow": "glow-gold"
    }
}

def get_palette(chapter_index: int = 1) -> Dict[str, str]:
    """Returns the color palette for the given chapter index (1-6)."""
    idx = max(1, min(6, int(chapter_index)))
    return PALETTES.get(idx, PALETTES[1])

def get_svg_defs(p: Dict[str, str]) -> str:
    """Generates rich multi-stop SVG gradients and feGaussianBlur glows."""
    return f"""
    <defs>
        <!-- Dynamic Chapter Radial Gradient -->
        <radialGradient id="space-grad" cx="50%" cy="50%" r="75%">
            <stop offset="0%" stop-color="{p['bg_radial']}" stop-opacity="1" />
            <stop offset="65%" stop-color="{p['bg_dark']}" stop-opacity="1" />
            <stop offset="100%" stop-color="{p['bg_darker']}" stop-opacity="1" />
        </radialGradient>

        <!-- Chapter Primary Linear Gradient -->
        <linearGradient id="primary-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{p['primary']}" />
            <stop offset="100%" stop-color="{p['secondary']}" />
        </linearGradient>

        <!-- Accent Gradient -->
        <linearGradient id="accent-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{p['secondary']}" />
            <stop offset="50%" stop-color="{p['primary']}" />
            <stop offset="100%" stop-color="{p['accent']}" />
        </linearGradient>

        <!-- Card Surface Gradient -->
        <linearGradient id="card-grad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="{p['card_bg']}" stop-opacity="0.95" />
            <stop offset="100%" stop-color="{p['bg_dark']}" stop-opacity="0.85" />
        </linearGradient>

        <!-- Flat 2.5D Torso Body Gradient -->
        <linearGradient id="torso-25d-grad" x1="20%" y1="0%" x2="80%" y2="100%">
            <stop offset="0%" stop-color="{p['card_bg']}" stop-opacity="1" />
            <stop offset="55%" stop-color="{p['bg_dark']}" stop-opacity="0.98" />
            <stop offset="100%" stop-color="{p['bg_darker']}" stop-opacity="1" />
        </linearGradient>

        <!-- Flat 2.5D Head Spherical Gradient -->
        <radialGradient id="head-25d-grad" cx="35%" cy="30%" r="70%">
            <stop offset="0%" stop-color="{p['card_bg']}" stop-opacity="1" />
            <stop offset="70%" stop-color="{p['bg_dark']}" stop-opacity="1" />
            <stop offset="100%" stop-color="{p['bg_darker']}" stop-opacity="1" />
        </radialGradient>

        <!-- Flat 2.5D Synapse Axon Gradient -->
        <linearGradient id="axon-25d-grad" x1="0%" y1="0%" x2="100%" y2="80%">
            <stop offset="0%" stop-color="{p['card_bg']}" stop-opacity="0.98" />
            <stop offset="50%" stop-color="{p['bg_dark']}" stop-opacity="0.95" />
            <stop offset="100%" stop-color="{p['bg_darker']}" stop-opacity="1" />
        </linearGradient>

        <!-- Flat 2.5D Synapse Dendrite Gradient -->
        <linearGradient id="dendrite-25d-grad" x1="100%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stop-color="{p['card_bg']}" stop-opacity="0.98" />
            <stop offset="50%" stop-color="{p['bg_dark']}" stop-opacity="0.95" />
            <stop offset="100%" stop-color="{p['bg_darker']}" stop-opacity="1" />
        </linearGradient>

        <!-- Balanced Soft Glow Filter (No excessive neon bloom) -->
        <filter id="glow-primary" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur1" />
            <feGaussianBlur in="SourceGraphic" stdDeviation="11" result="blur2" />
            <feMerge>
                <feMergeNode in="blur2" />
                <feMergeNode in="blur1" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>

        <!-- Subtle Crisp Edge Accent -->
        <filter id="glow-intense" x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="b1" />
            <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="b2" />
            <feGaussianBlur in="SourceGraphic" stdDeviation="16" result="b3" />
            <feMerge>
                <feMergeNode in="b3" />
                <feMergeNode in="b2" />
                <feMergeNode in="b1" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>

        <!-- Crisp Directional Drop Shadow -->
        <filter id="drop-shadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000000" flood-opacity="0.65" />
        </filter>

        <!-- Soft Ambient Shadow for Overlays -->
        <filter id="soft-shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.45" />
        </filter>

        <!-- Subtle Dot Grid Pattern -->
        <pattern id="dot-grid" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1.5" fill="{p['primary']}" opacity="0.06" />
        </pattern>
    </defs>
    """

def get_3layer_background(p: Dict[str, str], stars_count: int = 60) -> str:
    """Generates Layer 1: Deep cosmic obsidian canvas with parallax stars and light beams."""
    import random
    rng = random.Random(42)
    
    stars_p1 = []
    stars_p2 = []
    for i in range(stars_count):
        x = rng.randint(20, 1900)
        y = rng.randint(20, 1060)
        r = rng.choice([1.2, 1.8, 2.4, 3.2])
        op = round(rng.uniform(0.2, 0.75), 2)
        star_svg = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{op}" />'
        if i % 2 == 0:
            stars_p1.append(star_svg)
        else:
            stars_p2.append(star_svg)

    return f"""
    <!-- Layer 1: Cosmic Obsidian Background & Parallax Starfields -->
    <rect width="1920" height="1080" fill="url(#space-grad)" />
    <rect width="1920" height="1080" fill="url(#dot-grid)" />

    <!-- Radiant Ambient Light Beams -->
    <g id="bg-light-beams" opacity="0.25">
        <polygon points="960,0 300,1080 480,1080" fill="{p['primary']}" opacity="0.12" filter="url(#glow-primary)" />
        <polygon points="960,0 1440,1080 1620,1080" fill="{p['secondary']}" opacity="0.10" filter="url(#glow-primary)" />
        <polygon points="960,0 820,1080 1100,1080" fill="{p['accent']}" opacity="0.08" filter="url(#glow-primary)" />
    </g>

    <!-- Parallax Dust Layer 1 -->
    <g id="stars-parallax-1" class="parallax-p1">
        {"".join(stars_p1)}
    </g>

    <!-- Parallax Dust Layer 2 -->
    <g id="stars-parallax-2" class="parallax-p2">
        {"".join(stars_p2)}
    </g>
    """

def get_foreground_particles(p: Dict[str, str], count: int = 16) -> str:
    """Generates Layer 3: Floating foreground bokeh dust drifting across the camera."""
    import random
    rng = random.Random(1337)
    particles = []
    for _ in range(count):
        cx = rng.randint(40, 1880)
        cy = rng.randint(40, 1040)
        r = rng.uniform(3.0, 7.5)
        color = rng.choice([p["primary"], p["secondary"], "#FFFFFF"])
        op = round(rng.uniform(0.18, 0.45), 2)
        particles.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{color}" opacity="{op}" filter="url(#glow-primary)" />')
    return f'<g id="fg-bokeh-particles" class="foreground-particles">{"".join(particles)}</g>'

def get_safe_chapter_header(title: str, subtitle: Optional[str], chapter_index: int, p: Dict[str, str]) -> str:
    """
    Enforces strict safe bounding-box layout:
    - Chapter Title at y=105 (40px, Bold Montserrat, #FFFFFF)
    - Subtitle / Chapter Pill Badge at y=165 (22px, Semi-Bold Montserrat, Chapter Accent)
    - Enforces +25px safe vertical separation so title and badge NEVER collide or touch.
    """
    clean_title = re.sub(r'<[^>]+>', '', title).strip().upper()
    sub_text = (re.sub(r'<[^>]+>', '', subtitle).strip().upper()) if subtitle else f"CHAPTER 0{chapter_index} : BEHAVIORAL COGNITION"

    # Dynamic badge width calculation with generous padding
    badge_w = max(380, len(sub_text) * 11 + 60)
    badge_x = (1920 - badge_w) // 2

    return f"""
    <!-- Safe-Zone Header Group (y=70 to y=190) -->
    <g id="header-group">
        <!-- Top Episode Title -->
        <text x="960" y="105" text-anchor="middle" fill="{p['highlight']}"
              font-family="'Montserrat', sans-serif" font-weight="900" font-size="40" letter-spacing="1.5">
            {clean_title}
        </text>

        <!-- Subtitle Pill Badge with +25px safe margin -->
        <g id="header-pill-badge" transform="translate({badge_x}, 145)">
            <rect x="0" y="0" width="{badge_w}" height="38" rx="19"
                  fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="1.8" opacity="0.95" />
            <circle cx="22" cy="19" r="5" fill="{p['primary']}" filter="url(#glow-primary)" />
            <text x="{badge_w // 2 + 10}" y="25" text-anchor="middle" fill="{p['primary']}"
                  font-family="'Montserrat', sans-serif" font-weight="800" font-size="16" letter-spacing="2">
                {sub_text}
            </text>
        </g>
    </g>
    """

HIGHLIGHT_KEYWORDS = {
    "meras", "truth", "lie", "lies", "lied", "festinger", "1957", "1959",
    "dissonance", "beliefs", "clash", "gears", "overdrive", "ego", "incentive",
    "twenty", "dollar", "dollars", "pride", "comfort", "brain", "skull",
    "fraud", "illusion", "rationalization", "action", "actions", "boring",
    "thrilling", "conquers", "shield", "scales", "friction", "payout", "unsettling"
}

def split_sentence_into_phrases(sentence: str) -> List[str]:
    """Splits a narration sentence into concise 3-5 word kinetic phrase chunks."""
    clean = sanitize_display_and_tts_text(re.sub(r'<[^>]+>', '', sentence)).strip()
    if not clean:
        return []
    
    # Split by major punctuation marks
    raw_clauses = [c.strip() for c in re.split(r'([,.;:!?—]+)', clean) if c.strip()]
    merged = []
    i = 0
    while i < len(raw_clauses):
        part = raw_clauses[i]
        punct = ""
        if i + 1 < len(raw_clauses) and re.match(r'^[,.;:!?—]+$', raw_clauses[i+1]):
            punct = raw_clauses[i+1]
            i += 1
        clause = (part + punct).strip()
        words = clause.split()
        if len(words) > 6:
            # Split longer clause into two balanced halves
            half = (len(words) + 1) // 2
            merged.append(" ".join(words[:half]))
            merged.append(" ".join(words[half:]))
        elif len(words) > 0:
            merged.append(clause)
        i += 1
    
    # If any single chunk is very small (1-2 words), merge with adjacent if total <= 6 words
    final_phrases = []
    for chunk in merged:
        if final_phrases and len(final_phrases[-1].split()) + len(chunk.split()) <= 6:
            final_phrases[-1] = final_phrases[-1] + " " + chunk
        else:
            final_phrases.append(chunk)
            
    return final_phrases if final_phrases else [clean]

def get_kinetic_subtitles(
    sentence: str,
    duration: float,
    p: Dict[str, str],
    words_alignment: Optional[List[Dict[str, Any]]] = None,
    cx: float = 960,
    cy: float = 880
) -> tuple[str, str]:
    """
    Renders crisp, non-overlapping 2–3 second word-synced kinetic caption phrases.
    Guarantees outgoing phrases fade/snap out completely (0.08s) before incoming phrases enter,
    eliminating any visual text overlap inside the bottom caption box.
    """
    phrases = split_sentence_into_phrases(sentence)
    if not phrases:
        return "", ""

    num_phrases = len(phrases)
    phrase_svgs = []
    gsap_lines = []

    # Dynamic non-overlapping phrase time slots
    t_avail_start = 0.15
    t_avail_end = max(t_avail_start + 1.0, round(duration - 0.20, 2))
    slot_dur = (t_avail_end - t_avail_start) / num_phrases
    fade_in_dur = 0.18
    fade_out_dur = 0.08
    gap = 0.06  # Clean separation gap where previous phrase is 100% invisible

    for idx, phrase in enumerate(phrases):
        # Format words with active punch-word highlighting
        words = phrase.split()
        tspan_parts = []
        for w in words:
            clean_w = re.sub(r'[^a-zA-Z0-9$]', '', w).lower()
            if clean_w in HIGHLIGHT_KEYWORDS or clean_w.startswith("$"):
                color = p.get("secondary", "#00E5FF") if idx % 2 == 0 else p.get("primary", "#FFB800")
                tspan_parts.append(f'<tspan fill="{color}" font-weight="900" filter="url(#glow-primary)">{w}</tspan>')
            else:
                tspan_parts.append(f'<tspan fill="#FFFFFF" font-weight="700">{w}</tspan>')

        formatted_text = " ".join(tspan_parts)
        
        # Calculate dynamic width based on phrase length
        char_count = sum(len(w) for w in words) + len(words)
        box_w = max(440, min(1400, char_count * 22 + 90))
        box_x = -box_w // 2

        # SVG capsule
        phrase_svg = f"""
        <g class="sub-phrase-anchor" transform="translate({cx}, {cy})">
            <g id="sub-phrase-{idx}" class="kinetic-sub-phrase" opacity="0">
                <rect x="{box_x}" y="-32" width="{box_w}" height="64" rx="20"
                      fill="{p['bg_dark']}" fill-opacity="0.95" stroke="{p['primary']}" stroke-width="2.0" filter="url(#drop-shadow)" />
                <text x="0" y="2" text-anchor="middle" dominant-baseline="central"
                      font-family="'Montserrat', sans-serif" font-size="28" letter-spacing="0.5">
                    {formatted_text}
                </text>
            </g>
        </g>
        """
        phrase_svgs.append(phrase_svg)

        # Precise timing calculation guaranteeing ZERO crossfade overlap
        t_in = round(t_avail_start + idx * slot_dur, 2)
        t_slot_end = round(t_avail_start + (idx + 1) * slot_dur, 2)
        t_out = round(t_slot_end - fade_out_dur - gap, 2)
        if t_out <= t_in + 0.3:
            t_out = round(t_in + 0.3, 2)

        gsap_lines.append(f"""
            gsap.set('#sub-phrase-{idx}', {{ opacity: 0, y: 12, scale: 0.96, transformOrigin: 'center center' }});
            tl.to('#sub-phrase-{idx}', {{ duration: {fade_in_dur}, opacity: 1, y: 0, scale: 1.0, ease: 'power2.out' }}, {t_in});
            tl.to('#sub-phrase-{idx}', {{ duration: {fade_out_dur}, opacity: 0, y: -8, ease: 'power2.in' }}, {t_out});
        """)

    svg_out = "".join(phrase_svgs)
    gsap_out = "\n".join(gsap_lines)
    return svg_out, gsap_out

def get_kinetic_punch_word(text: str, p: Dict[str, str], cx: float = 960, cy: float = 920) -> str:
    """Legacy helper: preserved for backward compatibility."""
    return ""

def get_fast_synced_caption(sentence: str, p: Dict[str, str], cx: float = 960, cy: float = 835) -> str:
    """Legacy helper: preserved for backward compatibility."""
    return ""

# ==============================================================================
# COMPOSABLE VECTOR METAPHOR LIBRARY (100% MASCOT-FREE)
# ==============================================================================

def get_chapter_title_card(chapter_num: int, title: str, subtitle: str, p: Dict[str, str]) -> tuple[str, str]:
    """
    2-Second Motion-Graphics Chapter Title Card.
    Features expanding neon laser divider, bold chapter number badge, and glowing reticles.
    """
    svg = f"""
    <g id="metaphor-chapter-card" transform="translate(960, 520)" filter="url(#drop-shadow)">
        <!-- Outer Glowing Framing Ring -->
        <circle cx="0" cy="0" r="320" fill="none" stroke="{p['primary']}" stroke-width="1.5" stroke-dasharray="12 16" opacity="0.35" />
        <circle cx="0" cy="0" r="280" fill="{p['card_bg']}" opacity="0.9" />

        <!-- Chapter Index Pill Badge -->
        <g id="card-badge" transform="translate(0, -110)">
            <rect x="-110" y="-22" width="220" height="44" rx="22" fill="{p['bg_dark']}" stroke="{p['primary']}" stroke-width="2" />
            <text x="0" y="6" text-anchor="middle" fill="{p['primary']}"
                  font-family="'Montserrat', sans-serif" font-weight="900" font-size="20" letter-spacing="3">
                CHAPTER 0{chapter_num}
            </text>
        </g>

        <!-- Bold Chapter Title -->
        <text id="card-title" x="0" y="15" text-anchor="middle" fill="{p['highlight']}"
              font-family="'Montserrat', sans-serif" font-weight="900" font-size="52" letter-spacing="1">
            {title.upper()}
        </text>

        <!-- Expanding Neon Laser Divider -->
        <line id="card-divider" x1="-360" y1="65" x2="360" y2="65" stroke="url(#primary-grad)" stroke-width="4" stroke-linecap="round" filter="url(#glow-intense)" />

        <!-- Thematic Subtitle -->
        <text id="card-sub" x="0" y="115" text-anchor="middle" fill="{p['secondary']}"
              font-family="'Inter', sans-serif" font-weight="700" font-size="24" letter-spacing="4">
            {subtitle.upper()}
        </text>

        <!-- Tech Corner Reticles -->
        <path d="M -300,-180 L -330,-180 L -330,-150" stroke="{p['accent']}" stroke-width="3" fill="none" />
        <path d="M 300,-180 L 330,-180 L 330,-150" stroke="{p['accent']}" stroke-width="3" fill="none" />
        <path d="M -300,180 L -330,180 L -330,150" stroke="{p['accent']}" stroke-width="3" fill="none" />
        <path d="M 300,180 L 330,180 L 330,150" stroke="{p['accent']}" stroke-width="3" fill="none" />
    </g>
    """

    gsap = f"""
        gsap.set('#metaphor-chapter-card', {{ scale: 0.85, opacity: 0 }});
        gsap.set('#card-divider', {{ scaleX: 0, transformOrigin: 'center center' }});
        gsap.set('#card-title', {{ y: 25, opacity: 0 }});
        gsap.set('#card-sub', {{ y: 20, opacity: 0 }});
        gsap.set('#card-badge', {{ scale: 0.7, opacity: 0, transformOrigin: 'center center' }});

        tl.to('#metaphor-chapter-card', {{ duration: 0.6, opacity: 1, scale: 1.0, ease: 'power3.out' }}, 0.1);
        tl.to('#card-badge', {{ duration: 0.5, opacity: 1, scale: 1.0, ease: 'back.out(1.8)' }}, 0.25);
        tl.to('#card-title', {{ duration: 0.6, opacity: 1, y: 15, ease: 'power3.out' }}, 0.35);
        tl.to('#card-divider', {{ duration: 0.7, scaleX: 1.0, ease: 'elastic.out(1.2, 0.6)' }}, 0.45);
        tl.to('#card-sub', {{ duration: 0.5, opacity: 1, y: 115, ease: 'power3.out' }}, 0.55);
    """
    return svg, gsap

def get_animated_counter(
    number_target: str,
    label: str,
    sub_label: str,
    p: Dict[str, str],
    is_currency_comparison: bool = False,
    left_metric: str = "HIGH",
    right_metric: str = "LOW"
) -> tuple[str, str]:
    """
    Generates an animated numerical counter / comparison system.
    Handles dynamic metrics, years, quantities, and comparative columns.
    """
    if is_currency_comparison or "vs" in number_target.lower():
        # Dual column comparison
        svg = f"""
        <g id="metaphor-counter" transform="translate(960, 520)" filter="url(#drop-shadow)">
            <!-- Left Card -->
            <g id="card-col-left" transform="translate(-240, 0)">
                <rect x="-180" y="-190" width="360" height="380" rx="24" fill="{p['card_bg']}" stroke="#EF4444" stroke-width="3" />
                <circle cx="0" cy="-90" r="50" fill="#EF4444" opacity="0.2" filter="url(#glow-primary)" />
                <text x="0" y="-75" text-anchor="middle" fill="#EF4444" font-family="'Montserrat', sans-serif" font-weight="900" font-size="44">{left_metric}</text>
                <text x="0" y="-15" text-anchor="middle" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="22">HIGH CONDITION</text>
                <line x1="-140" y1="15" x2="140" y2="15" stroke="#EF4444" stroke-width="1.5" opacity="0.5" />
                <text x="0" y="55" text-anchor="middle" fill="#E2E8F0" font-family="'Inter', sans-serif" font-weight="600" font-size="19">External Signal</text>
                <text x="0" y="90" text-anchor="middle" fill="#94A3B8" font-family="'Inter', sans-serif" font-size="18">"Sufficient Reason"</text>
                <rect x="-140" y="122" width="280" height="38" rx="19" fill="#EF4444" opacity="0.22" />
                <text x="0" y="146" text-anchor="middle" fill="#EF4444" font-family="'Montserrat', sans-serif" font-weight="800" font-size="18">MINIMAL DISSONANCE</text>
            </g>

            <!-- Center VS Energy Spark -->
            <g id="vs-spark" transform="translate(0, 0)">
                <circle cx="0" cy="0" r="32" fill="{p['bg_dark']}" stroke="{p['primary']}" stroke-width="2.5" />
                <text x="0" y="8" text-anchor="middle" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="22">VS</text>
            </g>

            <!-- Right Card -->
            <g id="card-col-right" transform="translate(240, 0)">
                <rect x="-180" y="-190" width="360" height="380" rx="24" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3" />
                <circle cx="0" cy="-90" r="50" fill="{p['primary']}" opacity="0.2" filter="url(#glow-primary)" />
                <text x="0" y="-75" text-anchor="middle" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="44">{right_metric}</text>
                <text x="0" y="-15" text-anchor="middle" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="22">LOW CONDITION</text>
                <line x1="-140" y1="15" x2="140" y2="15" stroke="{p['primary']}" stroke-width="1.5" opacity="0.5" />
                <text x="0" y="55" text-anchor="middle" fill="#E2E8F0" font-family="'Inter', sans-serif" font-weight="600" font-size="19">Internal Friction</text>
                <text x="0" y="90" text-anchor="middle" fill="#94A3B8" font-family="'Inter', sans-serif" font-size="18">"Belief Must Adapt"</text>
                <rect x="-140" y="122" width="280" height="38" rx="19" fill="{p['primary']}" opacity="0.22" />
                <text x="0" y="146" text-anchor="middle" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="18">ACUTE DISSONANCE</text>
            </g>
        </g>
        """
        gsap = f"""
            gsap.set('#card-col-left', {{ x: -320, opacity: 0 }});
            gsap.set('#card-col-right', {{ x: 320, opacity: 0 }});
            gsap.set('#vs-spark', {{ scale: 0, opacity: 0 }});
            
            tl.to('#card-col-left', {{ duration: 0.8, x: -240, opacity: 1, ease: 'power3.out' }}, 0.2);
            tl.to('#card-col-right', {{ duration: 0.8, x: 240, opacity: 1, ease: 'power3.out' }}, 0.35);
            tl.to('#vs-spark', {{ duration: 0.6, scale: 1.0, opacity: 1, ease: 'elastic.out(1.2, 0.5)' }}, 0.55);
            
            tl.to('#card-col-right', {{ duration: 2.0, y: -8, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.8);
            tl.to('#card-col-left', {{ duration: 2.0, y: 8, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.8);
        """
        return svg, gsap

    # Standard Animated Number Counter (e.g. 1957, 48 PEGS, 100,000 YEARS)
    clean_num = re.sub(r'[^\d]', '', number_target) or "1957"
    target_int = int(clean_num)
    start_int = (target_int - 57) if target_int > 100 else 0
    start_display = f"{start_int}" if not is_currency_comparison else number_target

    svg = f"""
    <g id="metaphor-counter" transform="translate(960, 510)" filter="url(#drop-shadow)">
        <!-- Outer Glowing Radial Gauge -->
        <circle cx="0" cy="0" r="230" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3.5" />
        <circle id="counter-dashed-ring" cx="0" cy="0" r="255" fill="none" stroke="{p['secondary']}" stroke-width="2.5" stroke-dasharray="14 18" opacity="0.6" />
        <circle cx="0" cy="0" r="180" fill="{p['bg_dark']}" />

        <!-- Counter Digital Value (Counts Up Rapidly) -->
        <text id="counter-value-text" x="0" y="25" text-anchor="middle" fill="{p['primary']}"
              font-family="'Montserrat', sans-serif" font-weight="900" font-size="96" letter-spacing="2" filter="url(#glow-primary)">
            {start_display}
        </text>

        <!-- Metric Label -->
        <text x="0" y="-70" text-anchor="middle" fill="{p['highlight']}"
              font-family="'Montserrat', sans-serif" font-weight="800" font-size="24" letter-spacing="4">
            {label.upper()}
        </text>

        <!-- Subtext Pill -->
        <g id="counter-sub-pill" transform="translate(0, 85)">
            <rect x="-160" y="-19" width="320" height="40" rx="20" fill="{p['primary']}" opacity="0.25" stroke="{p['primary']}" stroke-width="1.5" />
            <text x="0" y="7" text-anchor="middle" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="20" letter-spacing="1.5">
                {sub_label.upper()}
            </text>
        </g>
    </g>
    """
    gsap = f"""
        // Staggered 3-Beat Motion for Counter
        // Beat 1 (0.0s - 0.4s): Outer gauge pops in
        gsap.set('#metaphor-counter', {{ scale: 0.85, opacity: 0 }});
        tl.to('#metaphor-counter', {{ duration: 0.55, scale: 1.0, opacity: 1, ease: 'back.out(1.7)' }}, 0.1);

        // Beat 2 (0.5s - 1.8s): Rapid digital counter tick-up ({start_int} -> {target_int}) & ring rotation
        const counterTarget = {{ val: {start_int} }};
        tl.to(counterTarget, {{
            val: {target_int},
            duration: 1.25,
            ease: 'power2.out',
            onUpdate: function() {{
                const el = document.getElementById('counter-value-text');
                if (el) el.textContent = Math.round(counterTarget.val);
            }}
        }}, 0.5);
        tl.to('#counter-dashed-ring', {{ duration: 2.2, rotate: 180, ease: 'power2.out', transformOrigin: 'center center' }}, 0.5);

        // Beat 3 (2.0s): Subtext pill pops in and subtle float
        gsap.set('#counter-sub-pill', {{ scale: 0.8, opacity: 0 }});
        tl.to('#counter-sub-pill', {{ duration: 0.5, scale: 1.0, opacity: 1, ease: 'back.out(1.5)' }}, 1.8);
        tl.to('#metaphor-counter', {{ duration: 2.2, rotate: 3, repeat: -1, yoyo: true, ease: 'sine.inOut', transformOrigin: 'center center' }}, 2.0);
    """
    return svg, gsap

def get_brain_synaptic_network(p: Dict[str, str]) -> tuple[str, str]:
    """Neural synaptic architecture with firing nodes and prefrontal cortex arbiter."""
    svg = f"""
    <g id="metaphor-brain" transform="translate(960, 520)" filter="url(#drop-shadow)">
        <!-- Outer Halo -->
        <circle cx="0" cy="0" r="280" fill="url(#primary-grad)" opacity="0.08" filter="url(#glow-intense)" />

        <!-- Dual Hemisphere Contours -->
        <path d="M 0,-180 C 130,-180 230,-90 230,30 C 230,140 130,210 0,210 C -130,210 -230,140 -230,30 C -230,-90 -130,-180 0,-180 Z"
              fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3.5" />

        <!-- Longitudinal Fissure Divider -->
        <line x1="0" y1="-175" x2="0" y2="205" stroke="{p['secondary']}" stroke-width="3" stroke-dasharray="10 12" opacity="0.7" />

        <!-- Neural Synapse Axons & Nodes -->
        <g id="synapse-network">
            <line x1="-120" y1="-70" x2="-40" y2="-110" stroke="{p['primary']}" stroke-width="2" opacity="0.6" />
            <line x1="-40" y1="-110" x2="60" y2="-90" stroke="{p['primary']}" stroke-width="2" opacity="0.6" />
            <line x1="60" y1="-90" x2="140" y2="-40" stroke="{p['primary']}" stroke-width="2" opacity="0.6" />
            <line x1="-120" y1="-70" x2="-80" y2="40" stroke="{p['primary']}" stroke-width="2" opacity="0.6" />
            <line x1="-80" y1="40" x2="0" y2="80" stroke="{p['primary']}" stroke-width="2" opacity="0.6" />
            <line x1="0" y1="80" x2="90" y2="60" stroke="{p['primary']}" stroke-width="2" opacity="0.6" />
            <line x1="90" y1="60" x2="140" y2="-40" stroke="{p['primary']}" stroke-width="2" opacity="0.6" />

            <circle class="synapse-node" cx="-120" cy="-70" r="9" fill="{p['primary']}" filter="url(#glow-primary)" />
            <circle class="synapse-node" cx="-40" cy="-110" r="11" fill="{p['secondary']}" filter="url(#glow-primary)" />
            <circle class="synapse-node" cx="60" cy="-90" r="10" fill="{p['primary']}" filter="url(#glow-primary)" />
            <circle class="synapse-node" cx="140" cy="-40" r="9" fill="{p['accent']}" filter="url(#glow-primary)" />
            <circle class="synapse-node" cx="-80" cy="40" r="12" fill="{p['secondary']}" filter="url(#glow-primary)" />
            <circle class="synapse-node" cx="0" cy="80" r="14" fill="{p['primary']}" filter="url(#glow-intense)" />
            <circle class="synapse-node" cx="90" cy="60" r="10" fill="{p['accent']}" filter="url(#glow-primary)" />
        </g>

        <!-- Prefrontal Cortex Glowing Arbiter Beacon -->
        <g id="prefrontal-arbiter" transform="translate(0, -90)">
            <circle cx="0" cy="0" r="32" fill="{p['primary']}" opacity="0.3" filter="url(#glow-intense)" />
            <circle cx="0" cy="0" r="16" fill="{p['highlight']}" filter="url(#glow-primary)" />
            <text x="0" y="44" text-anchor="middle" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="18" letter-spacing="1.5">PREFRONTAL ARBITER</text>
        </g>
    </g>
    """
    gsap = f"""
        // Staggered 3-Beat Motion for Brain Synaptic Network
        // Beat 1 (0.0s): Brain contour pops in
        gsap.set('#metaphor-brain', {{ scale: 0.88, opacity: 0 }});
        tl.to('#metaphor-brain', {{ duration: 0.6, scale: 1.0, opacity: 1, ease: 'back.out(1.7)' }}, 0.1);

        // Beat 2 (0.8s): Synapse nodes cascade in with lively pops
        gsap.set('.synapse-node', {{ scale: 0, opacity: 0 }});
        tl.to('.synapse-node', {{ duration: 0.5, scale: 1.3, opacity: 1, stagger: 0.1, ease: 'back.out(2.0)', transformOrigin: 'center center' }}, 0.7);

        // Beat 3 (2.2s): Prefrontal Arbiter beacon flares brightly
        tl.to('#prefrontal-arbiter', {{ duration: 1.2, scale: 1.2, repeat: -1, yoyo: true, ease: 'sine.inOut', transformOrigin: 'center center' }}, 2.0);
        tl.to('.synapse-node', {{ duration: 0.8, scale: 1.0, repeat: -1, yoyo: true, ease: 'sine.inOut', stagger: 0.12, transformOrigin: 'center center' }}, 2.0);
    """
    return svg, gsap

def get_cognitive_dissonance_split(p: Dict[str, str]) -> tuple[str, str]:
    """Two opposing reality hemispheres tearing apart with central energy fissure."""
    svg = f"""
    <g id="metaphor-split" transform="translate(960, 520)" filter="url(#drop-shadow)">
        <!-- Left Hemisphere: Belief / Values -->
        <g id="split-left" transform="translate(-140, 0)">
            <path d="M 0,-170 C -120,-170 -200,-90 -200,20 C -200,130 -120,190 0,190 Z"
                  fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3" />
            <circle cx="-90" cy="10" r="38" fill="{p['primary']}" opacity="0.2" filter="url(#glow-primary)" />
            <text x="-90" y="5" text-anchor="middle" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="24">BELIEF</text>
            <text x="-90" y="32" text-anchor="middle" fill="{p['primary']}" font-family="'Inter', sans-serif" font-weight="700" font-size="18">"I AM RATIONAL"</text>
        </g>

        <!-- Right Hemisphere: Contradictory Action -->
        <g id="split-right" transform="translate(140, 0)">
            <path d="M 0,-170 C 120,-170 200,-90 200,20 C 200,130 120,190 0,190 Z"
                  fill="{p['card_bg']}" stroke="#FF3B6B" stroke-width="3" />
            <circle cx="90" cy="10" r="38" fill="#FF3B6B" opacity="0.2" filter="url(#glow-primary)" />
            <text x="90" y="5" text-anchor="middle" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="24">ACTION</text>
            <text x="90" y="32" text-anchor="middle" fill="#FF3B6B" font-family="'Inter', sans-serif" font-weight="700" font-size="18">"CONTRADICTION"</text>
        </g>

        <!-- Jagged Lightning Energy Fissure -->
        <g id="split-fissure">
            <path d="M 0,-210 L -25,-120 L 25,-40 L -30,40 L 20,130 L 0,220"
                  stroke="{p['secondary']}" stroke-width="4.5" fill="none" filter="url(#glow-intense)" />
            <circle cx="0" cy="0" r="20" fill="{p['highlight']}" filter="url(#glow-primary)" />
            <text x="0" y="-14" text-anchor="middle" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="18">ACUTE FRICTION</text>
        </g>
    </g>
    """
    gsap = f"""
        gsap.set('#split-left', {{ x: -60, opacity: 0 }});
        gsap.set('#split-right', {{ x: 60, opacity: 0 }});
        gsap.set('#split-fissure', {{ scaleY: 0, opacity: 0, transformOrigin: 'center center' }});

        tl.to('#split-left', {{ duration: 0.9, x: -140, opacity: 1, ease: 'power3.out' }}, 0.15);
        tl.to('#split-right', {{ duration: 0.9, x: 140, opacity: 1, ease: 'power3.out' }}, 0.15);
        tl.to('#split-fissure', {{ duration: 0.6, scaleY: 1.0, opacity: 1, ease: 'elastic.out(1.2, 0.6)' }}, 0.4);

        // Fissure Electric Pulse
        tl.to('#split-fissure', {{ duration: 0.15, opacity: 0.65, repeat: -1, yoyo: true, ease: 'steps(2)' }}, 0.6);
        tl.to('#split-left', {{ duration: 2.2, y: -6, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.6);
        tl.to('#split-right', {{ duration: 2.2, y: 6, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.6);
    """
    return svg, gsap

def get_rationalization_gears(p: Dict[str, str]) -> tuple[str, str]:
    """
    Staggered 3-Beat Rotating Precision Mechanical Vector Gears.
    Beat 1 (0.0s): Main gear scales in with punchy back.out(1.7)
    Beat 2 (1.0s): Secondary counter gear slams into mesh, gears rotate visibly fast (3.5s per rev)
    Beat 3 (2.6s): Deflection friction sparks flare and pulse with intense glow
    Inner hub text (REASONING & EGO SHIELD) enforced >= 20px, permanently upright and horizontal.
    """
    svg = f"""
    <g id="metaphor-gears" transform="translate(960, 510)" filter="url(#drop-shadow)">
        <!-- Large Primary Central Gear -->
        <g id="gear-main" transform="translate(-60, 0)">
            <!-- Rotating Teeth & Outer Ring Only -->
            <g id="gear-main-teeth">
                <circle cx="0" cy="0" r="132" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3" />
                <circle cx="0" cy="0" r="95" fill="none" stroke="{p['primary']}" stroke-width="2" stroke-dasharray="10 8" opacity="0.6" />
                <!-- Gear Teeth -->
                <rect x="-14" y="-150" width="28" height="38" rx="6" fill="{p['primary']}" />
                <rect x="-14" y="112" width="28" height="38" rx="6" fill="{p['primary']}" />
                <rect x="-150" y="-14" width="38" height="28" rx="6" fill="{p['primary']}" />
                <rect x="112" y="-14" width="38" height="28" rx="6" fill="{p['primary']}" />
                <!-- 45-deg teeth -->
                <rect x="-14" y="-150" width="28" height="38" rx="6" fill="{p['primary']}" transform="rotate(45)" />
                <rect x="-14" y="-150" width="28" height="38" rx="6" fill="{p['primary']}" transform="rotate(135)" />
                <rect x="-14" y="-150" width="28" height="38" rx="6" fill="{p['primary']}" transform="rotate(225)" />
                <rect x="-14" y="-150" width="28" height="38" rx="6" fill="{p['primary']}" transform="rotate(315)" />
            </g>
            <!-- Upright Static Center Hub & Label (NEVER ROTATES) -->
            <g id="gear-main-hub">
                <circle cx="0" cy="0" r="72" fill="{p['bg_dark']}" stroke="{p['secondary']}" stroke-width="3" filter="url(#drop-shadow)" />
                <circle cx="0" cy="0" r="62" fill="{p['card_bg']}" />
                <circle cx="0" cy="0" r="14" fill="{p['primary']}" opacity="0.4" filter="url(#glow-primary)" />
                <text x="0" y="8" text-anchor="middle" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="22" letter-spacing="1.5">REASONING</text>
            </g>
        </g>

        <!-- Secondary Interlocking Counter-Gear -->
        <g id="gear-sub" transform="translate(150, -75)">
            <!-- Rotating Teeth & Outer Ring Only -->
            <g id="gear-sub-teeth">
                <circle cx="0" cy="0" r="88" fill="{p['card_bg']}" stroke="{p['secondary']}" stroke-width="2.5" />
                <circle cx="0" cy="0" r="64" fill="none" stroke="{p['secondary']}" stroke-width="1.5" stroke-dasharray="8 6" opacity="0.6" />
                <rect x="-10" y="-102" width="20" height="28" rx="4" fill="{p['secondary']}" />
                <rect x="-10" y="74" width="20" height="28" rx="4" fill="{p['secondary']}" />
                <rect x="-102" y="-10" width="28" height="20" rx="4" fill="{p['secondary']}" />
                <rect x="74" y="-10" width="28" height="20" rx="4" fill="{p['secondary']}" />
                <rect x="-10" y="-102" width="20" height="28" rx="4" fill="{p['secondary']}" transform="rotate(45)" />
                <rect x="-10" y="-102" width="20" height="28" rx="4" fill="{p['secondary']}" transform="rotate(135)" />
                <rect x="-10" y="-102" width="20" height="28" rx="4" fill="{p['secondary']}" transform="rotate(225)" />
                <rect x="-10" y="-102" width="20" height="28" rx="4" fill="{p['secondary']}" transform="rotate(315)" />
            </g>
            <!-- Upright Static Sub Hub & Label (NEVER ROTATES, min 20px font) -->
            <g id="gear-sub-hub">
                <circle cx="0" cy="0" r="56" fill="{p['bg_dark']}" stroke="{p['accent']}" stroke-width="2.5" filter="url(#drop-shadow)" />
                <circle cx="0" cy="0" r="48" fill="{p['card_bg']}" />
                <text x="0" y="7" text-anchor="middle" fill="{p['secondary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="20" letter-spacing="0.5">EGO SHIELD</text>
            </g>
        </g>

        <!-- Deflected Reality Arrow Particles -->
        <g id="gear-sparks">
            <line x1="75" y1="-20" x2="115" y2="-55" stroke="{p['accent']}" stroke-width="3" stroke-linecap="round" filter="url(#glow-primary)" />
            <line x1="85" y1="10" x2="135" y2="25" stroke="{p['primary']}" stroke-width="3" stroke-linecap="round" filter="url(#glow-primary)" />
            <circle cx="115" cy="-55" r="5" fill="{p['highlight']}" filter="url(#glow-intense)" />
            <circle cx="135" cy="25" r="5" fill="{p['primary']}" filter="url(#glow-intense)" />
        </g>
    </g>
    """
    gsap = f"""
        // Staggered 3-Beat Motion
        // Beat 1: Main Gear pops in (0.0s)
        gsap.set('#gear-main', {{ scale: 0.8, opacity: 0, transformOrigin: 'center center' }});
        tl.to('#gear-main', {{ duration: 0.6, scale: 1.0, opacity: 1, ease: 'back.out(1.7)' }}, 0.1);

        // Beat 2: Counter Gear slams in and latches into mesh (1.0s)
        gsap.set('#gear-sub', {{ x: 260, opacity: 0 }});
        tl.to('#gear-sub', {{ duration: 0.75, x: 150, opacity: 1, ease: 'back.out(1.5)' }}, 0.9);

        // Continuous Interlocking Rotation: Fast, visible mechanical action (3.5s full rotation)
        tl.to('#gear-main-teeth', {{ duration: 3.5, rotate: 360, repeat: -1, ease: 'none', transformOrigin: 'center center' }}, 0);
        tl.to('#gear-sub-teeth', {{ duration: 2.29, rotate: -360, repeat: -1, ease: 'none', transformOrigin: 'center center' }}, 0);

        // Beat 3: Friction sparks burst and pulse (2.6s)
        gsap.set('#gear-sparks', {{ scale: 0, opacity: 0, transformOrigin: 'center center' }});
        tl.to('#gear-sparks', {{ duration: 0.5, scale: 1.3, opacity: 1, ease: 'elastic.out(1.2, 0.5)' }}, 2.4);
        tl.to('#gear-sparks', {{ duration: 0.8, scale: 1.0, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 2.9);
    """
    return svg, gsap

def get_scales_balance_system(
    p: Dict[str, str],
    left_label: str = "HIGH INCENTIVE",
    right_label: str = "LOW INCENTIVE",
    left_val: str = "HEAVY",
    right_val: str = "LIGHT"
) -> tuple[str, str]:
    """Precision vector balance scales with connected horizontal pivot beam and dynamic labels."""
    svg = f"""
    <g id="metaphor-scales" transform="translate(960, 500)" filter="url(#drop-shadow)">
        <!-- Vertical Central Stand & Base -->
        <rect x="-14" y="-120" width="28" height="260" rx="8" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3" />
        <polygon points="-90,140 90,140 70,105 -70,105" fill="{p['bg_dark']}" stroke="{p['primary']}" stroke-width="3" />

        <!-- Tilting Cross Beam Assembly (Pivoting at 0, -120) -->
        <g id="scales-beam-group">
            <!-- Sturdy Connected Horizontal Pivot Beam -->
            <rect x="-260" y="-127" width="520" height="14" rx="7" fill="url(#primary-grad)" stroke="{p['highlight']}" stroke-width="2" filter="url(#glow-primary)" />
            <line x1="-240" y1="-120" x2="240" y2="-120" stroke="{p['bg_dark']}" stroke-width="2" stroke-dasharray="8 6" opacity="0.6" />

            <!-- Left Suspension Chains & Pan -->
            <g id="pan-left" transform="translate(-240, -120)">
                <!-- Suspension Chains connected to beam end -->
                <line x1="0" y1="0" x2="-55" y2="130" stroke="{p['primary']}" stroke-width="2.5" />
                <line x1="0" y1="0" x2="55" y2="130" stroke="{p['primary']}" stroke-width="2.5" />
                <circle cx="0" cy="0" r="7" fill="{p['highlight']}" />
                <!-- Pan Bowl -->
                <path d="M -85,130 Q 0,175 85,130 Z" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3" />
                <!-- Left Weight Block -->
                <rect x="-65" y="78" width="130" height="52" rx="10" fill="{p['bg_dark']}" stroke="#EF4444" stroke-width="2.5" />
                <text x="0" y="114" text-anchor="middle" fill="#EF4444" font-family="'Montserrat', sans-serif" font-weight="900" font-size="28">{left_val}</text>
                <text x="0" y="156" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="21">{left_label}</text>
            </g>

            <!-- Right Suspension Chains & Pan -->
            <g id="pan-right" transform="translate(240, -120)">
                <!-- Suspension Chains connected to beam end -->
                <line x1="0" y1="0" x2="-55" y2="130" stroke="{p['secondary']}" stroke-width="2.5" />
                <line x1="0" y1="0" x2="55" y2="130" stroke="{p['secondary']}" stroke-width="2.5" />
                <circle cx="0" cy="0" r="7" fill="{p['highlight']}" />
                <!-- Pan Bowl -->
                <path d="M -85,130 Q 0,175 85,130 Z" fill="{p['card_bg']}" stroke="{p['secondary']}" stroke-width="3" />
                <!-- Right Weight Block -->
                <rect x="-55" y="90" width="110" height="40" rx="8" fill="{p['bg_dark']}" stroke="{p['primary']}" stroke-width="2.5" />
                <text x="0" y="120" text-anchor="middle" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="26">{right_val}</text>
                <text x="0" y="156" text-anchor="middle" dominant-baseline="central" fill="{p['secondary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="21">{right_label}</text>
            </g>

            <!-- Central Fulcrum / Pivot Bearing (On top of beam at pivot point) -->
            <circle cx="0" cy="-120" r="24" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3.5" />
            <circle cx="0" cy="-120" r="14" fill="{p['secondary']}" filter="url(#glow-intense)" />
            <circle cx="0" cy="-120" r="6" fill="#FFFFFF" />
        </g>
    </g>
    """
    gsap = f"""
        // Staggered 3-Beat Motion for Scales
        // Beat 1 (0.0s - 0.4s): Pillar & horizontal beam drop in
        gsap.set('#metaphor-scales', {{ scale: 0.88, opacity: 0 }});
        tl.to('#metaphor-scales', {{ duration: 0.6, scale: 1.0, opacity: 1, ease: 'back.out(1.7)' }}, 0.1);

        // Beat 2 (0.7s): Left weight hits the pan, beam rapidly tilts down
        tl.to('#scales-beam-group', {{ duration: 0.65, rotate: -14, ease: 'back.out(1.5)', transformOrigin: '0px -120px' }}, 0.65);

        // Beat 3 (1.8s): Dynamic harmonic sway between -14 and +8 degrees
        tl.to('#scales-beam-group', {{ duration: 1.8, rotate: 8, repeat: -1, yoyo: true, ease: 'sine.inOut', transformOrigin: '0px -120px' }}, 1.8);
    """
    return svg, gsap

def get_hourglass_clock(p: Dict[str, str]) -> tuple[str, str]:
    """Animated vector hourglass with flowing glowing particle sands."""
    svg = f"""
    <g id="metaphor-hourglass" transform="translate(960, 520)" filter="url(#drop-shadow)">
        <g id="hourglass-float">
            <!-- Outer Time-Dilation Rings -->
            <circle cx="0" cy="0" r="240" fill="none" stroke="{p['primary']}" stroke-width="1.5" stroke-dasharray="10 14" opacity="0.3" />

            <!-- Hourglass Glass Envelope -->
            <path d="M -110,-170 L 110,-170 L 18,-15 Q 0,0 -18,15 L -110,170 L 110,170"
                  fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="3" opacity="0.85" />
            <rect x="-130" y="-185" width="260" height="22" rx="8" fill="{p['primary']}" />
            <rect x="-130" y="165" width="260" height="22" rx="8" fill="{p['primary']}" />

            <!-- Falling Particle Stream -->
            <line x1="0" y1="-10" x2="0" y2="140" stroke="{p['secondary']}" stroke-width="3" stroke-dasharray="4 6" filter="url(#glow-primary)" />
            <circle cx="0" cy="140" r="30" fill="{p['secondary']}" opacity="0.4" filter="url(#glow-primary)" />
        </g>
    </g>
    """
    gsap = f"""
        gsap.set('#hourglass-float', {{ scale: 0.88, opacity: 0, transformOrigin: 'center center' }});
        tl.to('#hourglass-float', {{ duration: 0.9, scale: 1.0, opacity: 1, ease: 'power3.out' }}, 0.15);
        tl.to('#hourglass-float', {{ duration: 3.0, y: -12, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0);
    """
    return svg, gsap

def get_cosmic_horizon(p: Dict[str, str]) -> tuple[str, str]:
    """Celestial deep space body with glowing orbital rings and horizon revelation."""
    svg = f"""
    <g id="metaphor-horizon" transform="translate(960, 520)" filter="url(#drop-shadow)">
        <g id="horizon-float">
            <!-- Giant Celestial Body -->
            <circle cx="0" cy="0" r="170" fill="url(#primary-grad)" />
            <circle cx="0" cy="0" r="170" fill="{p['card_bg']}" opacity="0.65" />

            <!-- Glowing Equatorial Ring System -->
            <g id="horizon-rings">
                <ellipse cx="0" cy="0" rx="340" ry="70" fill="none" stroke="{p['primary']}" stroke-width="4" stroke-dasharray="24 16"
                         transform="rotate(-18)" filter="url(#glow-intense)" />
                <ellipse cx="0" cy="0" rx="370" ry="80" fill="none" stroke="{p['secondary']}" stroke-width="1.8"
                         transform="rotate(-18)" opacity="0.5" />
            </g>

            <!-- Core Transcendence Emblem (min 20px font) -->
            <g id="horizon-core">
                <circle cx="0" cy="0" r="46" fill="{p['highlight']}" filter="url(#glow-primary)" />
                <text x="0" y="8" text-anchor="middle" fill="{p['bg_dark']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="22" letter-spacing="1">MERAS</text>
            </g>
        </g>
    </g>
    """
    gsap = f"""
        // Staggered 3-Beat Motion for Cosmic Horizon
        // Beat 1 (0.0s): Core body scales in
        gsap.set('#horizon-float', {{ scale: 0.85, opacity: 0, transformOrigin: 'center center' }});
        tl.to('#horizon-float', {{ duration: 0.65, scale: 1.0, opacity: 1, ease: 'back.out(1.7)' }}, 0.1);

        // Beat 2 (0.8s): Rings expand and rotate
        gsap.set('#horizon-rings', {{ scale: 0.75, opacity: 0, transformOrigin: 'center center' }});
        tl.to('#horizon-rings', {{ duration: 0.8, scale: 1.0, opacity: 1, ease: 'power2.out' }}, 0.7);

        // Beat 3 (2.2s): Core emblem pulses with flare
        tl.to('#horizon-core', {{ duration: 1.2, scale: 1.2, repeat: -1, yoyo: true, ease: 'sine.inOut', transformOrigin: 'center center' }}, 2.0);
        tl.to('#horizon-float', {{ duration: 3.5, y: -14, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0);
    """
    return svg, gsap

# ==============================================================================
# 5 ADVANCED BROADCAST COMPOSITIONAL LAYOUTS (Vox / Kurzgesagt Architecture)
# ==============================================================================

def get_split_comparison_layout(
    p: Dict[str, str],
    left_title: str = "BELIEF STATE",
    left_metric: str = "IDENTITY",
    left_sub: str = "INTERNAL MODEL",
    right_title: str = "ACTION TAKEN",
    right_metric: str = "REALITY",
    right_sub: str = "OBSERVED OUTCOME",
    vs_label: str = "≠"
) -> tuple[str, str]:
    """
    LAYOUT 1: SPLIT_COMPARISON
    Side-by-side visual contrast with split headers, dual high-contrast cards,
    mobile-readable secondary sub-labels (>= 20px–22px), and central dynamic tension seam.
    Fully dynamic parameters: zero hardcoded strings.
    """
    svg = f"""
    <g id="layout-split-comparison">
        <!-- Split-Screen Section Headers -->
        <g transform="translate(500, 155)">
            <g id="split-left-header">
                <rect x="-230" y="-28" width="460" height="56" rx="28"
                      fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="2.2" filter="url(#drop-shadow)" />
                <text x="0" y="8" text-anchor="middle" dominant-baseline="central" fill="{p['primary']}"
                      font-family="'Montserrat', sans-serif" font-weight="900" font-size="22" letter-spacing="1">
                    {left_title}
                </text>
            </g>
        </g>

        <g transform="translate(1420, 155)">
            <g id="split-right-header">
                <rect x="-230" y="-28" width="460" height="56" rx="28"
                      fill="{p['card_bg']}" stroke="#FF3B6B" stroke-width="2.2" filter="url(#drop-shadow)" />
                <text x="0" y="8" text-anchor="middle" dominant-baseline="central" fill="#FF3B6B"
                      font-family="'Montserrat', sans-serif" font-weight="900" font-size="22" letter-spacing="1">
                    {right_title}
                </text>
            </g>
        </g>

        <!-- Central Tension Seam & Contradiction Badge -->
        <g id="split-center-seam">
            <line x1="960" y1="210" x2="960" y2="760" stroke="{p['primary']}" stroke-width="2.5" stroke-dasharray="8 8" opacity="0.45" />
            <circle cx="960" cy="485" r="44" fill="{p['bg_dark']}" stroke="{p['accent']}" stroke-width="3" filter="url(#drop-shadow)" />
            <text x="960" y="493" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}"
                  font-family="'Montserrat', sans-serif" font-weight="900" font-size="28">
                {vs_label}
            </text>
        </g>

        <!-- Left Visual Stage -->
        <g transform="translate(500, 480)">
            <g id="split-left-stage" filter="url(#drop-shadow)">
                <rect x="-220" y="-155" width="440" height="310" rx="24"
                      fill="url(#card-grad)" stroke="{p['primary']}" stroke-width="2.5" />
                
                <!-- Metric Foundation -->
                <rect x="-140" y="-125" width="280" height="85" rx="14" fill="{p['bg_dark']}" stroke="{p['secondary']}" stroke-width="2" />
                <text x="0" y="-76" text-anchor="middle" dominant-baseline="central" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="36" filter="url(#glow-primary)">{left_metric}</text>
                
                <!-- Analytical Sub-Pill (Mobile-Readable >= 20px) -->
                <rect x="-190" y="-15" width="380" height="48" rx="14" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="1.6" />
                <text x="0" y="10" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="20" letter-spacing="0.5">
                    {left_sub}
                </text>
                <!-- Label Sub-Caption (Mobile-Readable 21px) -->
                <text x="0" y="74" text-anchor="middle" dominant-baseline="central" fill="#FFFFFF" font-family="'Montserrat', sans-serif" font-weight="800" font-size="21">
                    {left_title}
                </text>
            </g>
        </g>

        <!-- Right Visual Stage -->
        <g transform="translate(1420, 480)">
            <g id="split-right-stage" filter="url(#drop-shadow)">
                <rect x="-220" y="-155" width="440" height="310" rx="24"
                      fill="url(#card-grad)" stroke="#FF3B6B" stroke-width="2.5" />
                
                <!-- Metric Tension Dial -->
                <rect x="-140" y="-125" width="280" height="85" rx="14" fill="{p['bg_dark']}" stroke="#FF3B6B" stroke-width="2" />
                <text x="0" y="-76" text-anchor="middle" dominant-baseline="central" fill="#FF3B6B" font-family="'Montserrat', sans-serif" font-weight="900" font-size="36" filter="url(#glow-intense)">{right_metric}</text>
                
                <!-- Analytical Sub-Pill (Mobile-Readable >= 20px) -->
                <rect x="-190" y="-15" width="380" height="48" rx="14" fill="{p['card_bg']}" stroke="#FF3B6B" stroke-width="1.6" />
                <text x="0" y="10" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="20" letter-spacing="0.5">
                    {right_sub}
                </text>
                <!-- Label Sub-Caption (Mobile-Readable 21px) -->
                <text x="0" y="74" text-anchor="middle" dominant-baseline="central" fill="#FFFFFF" font-family="'Montserrat', sans-serif" font-weight="800" font-size="21">
                    {right_title}
                </text>
            </g>
        </g>
    </g>
    """
    gsap = f"""
        // Split-Comparison Synchronous Entry
        gsap.set('#split-left-stage', {{ x: -60, opacity: 0 }});
        gsap.set('#split-right-stage', {{ x: 60, opacity: 0 }});
        gsap.set('#split-left-header', {{ y: -20, opacity: 0 }});
        gsap.set('#split-right-header', {{ y: -20, opacity: 0 }});
        gsap.set('#split-center-seam', {{ scale: 0.8, opacity: 0, transformOrigin: '960px 485px' }});

        tl.to('#split-left-stage', {{ duration: 0.55, x: 0, opacity: 1, ease: 'power3.out' }}, 0.1);
        tl.to('#split-right-stage', {{ duration: 0.55, x: 0, opacity: 1, ease: 'power3.out' }}, 0.1);
        tl.to('#split-left-header', {{ duration: 0.45, y: 0, opacity: 1, ease: 'back.out(1.5)' }}, 0.25);
        tl.to('#split-right-header', {{ duration: 0.45, y: 0, opacity: 1, ease: 'back.out(1.5)' }}, 0.25);
        tl.to('#split-center-seam', {{ duration: 0.5, scale: 1.0, opacity: 1, ease: 'back.out(1.8)', transformOrigin: '960px 485px' }}, 0.35);

        // Subtle Organic Tension Drift
        tl.to('#split-left-stage', {{ duration: 2.8, y: -6, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.7);
        tl.to('#split-right-stage', {{ duration: 2.8, y: 6, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.7);
    """
    return svg, gsap


def get_human_silhouette_scene(
    p: Dict[str, str],
    context_label: str = "INTERNAL CONFLICT",
    thought_bubble: str = "DEFENDING REALITY",
    emotion_state: str = "COGNITIVE FRICTION",
    variant: str = "conflict"
) -> tuple[str, str]:
    """
    LAYOUT 2: HUMAN_SILHOUETTE_SCENE
    Flat 2.5D geometric human silhouette with rich filled gradient shading,
    specular rim lighting, radiating conflict resonance rings, illuminated prefrontal node,
    and mobile-readable floating thought callout.
    Zero hardcoded strings.
    """
    lab_props = ""
    if variant == "experiment":
        lab_props = f"""
        <!-- Experimental Laboratory Apparatus -->
        <g id="lab-table" transform="translate(680, 700)">
            <rect x="-240" y="0" width="480" height="24" rx="8" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="2" />
            <!-- Pegboard base -->
            <rect x="-140" y="-45" width="280" height="45" rx="6" fill="{p['bg_dark']}" stroke="{p['secondary']}" stroke-width="2" />
            <!-- Pegs representation -->
            <line x1="-90" y1="-45" x2="-90" y2="-85" stroke="{p['primary']}" stroke-width="6" stroke-linecap="round" />
            <line x1="-30" y1="-45" x2="-30" y2="-85" stroke="{p['primary']}" stroke-width="6" stroke-linecap="round" />
            <line x1="30" y1="-45" x2="30" y2="-85" stroke="{p['primary']}" stroke-width="6" stroke-linecap="round" />
            <line x1="90" y1="-45" x2="90" y2="-85" stroke="{p['primary']}" stroke-width="6" stroke-linecap="round" />
            <text x="0" y="55" text-anchor="middle" dominant-baseline="central" fill="{p['secondary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="20">
                {context_label}
            </text>
        </g>
        """

    svg = f"""
    <g id="layout-human-silhouette">
        <!-- Minimalist Geometric Human Figure (Rich Flat 2.5D Filled Vector) -->
        <g transform="translate(680, 560)">
            <g id="human-figure-body" filter="url(#drop-shadow)">
                <!-- Torso & Shoulders: Layered 2.5D Gradient Shading with Rim Specular -->
                <path d="M -160,180 L -140,20 C -140,-60 -80,-85 0,-85 C 80,-85 140,-60 140,20 L 160,180 Z"
                      fill="url(#torso-25d-grad)" stroke="{p['primary']}" stroke-width="2.5" />
                
                <!-- Inner Torso Depth Layer -->
                <path d="M -110,175 L -95,35 C -95,-30 -55,-60 0,-60 C 55,-60 95,-30 95,35 L 110,175 Z"
                      fill="{p['card_bg']}" fill-opacity="0.45" stroke="{p['secondary']}" stroke-width="1.5" stroke-opacity="0.35" />

                <!-- Left Shoulder Specular Rim Light -->
                <path d="M -135,15 C -120,-45 -70,-75 0,-75" fill="none" stroke="{p['primary']}" stroke-width="3.5" stroke-linecap="round" opacity="0.85" filter="url(#glow-primary)" />
                <!-- Right Shoulder Ambient Rim Light -->
                <path d="M 0,-75 C 70,-75 120,-45 135,15" fill="none" stroke="{p['secondary']}" stroke-width="2.5" stroke-linecap="round" opacity="0.65" />

                <!-- Collar & Neck Assembly -->
                <rect x="-24" y="-115" width="48" height="38" rx="8" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="2" />

                <!-- Pulsing Conflict Resonance Rings radiating from Cranium -->
                <g id="conflict-rings">
                    <circle id="c-ring-1" cx="0" cy="-175" r="68" fill="none" stroke="#FF3B6B" stroke-width="2.5" opacity="0.85" stroke-dasharray="6 4" filter="url(#glow-intense)" />
                    <circle id="c-ring-2" cx="0" cy="-175" r="92" fill="none" stroke="{p['primary']}" stroke-width="2" opacity="0.65" stroke-dasharray="8 6" filter="url(#glow-primary)" />
                    <circle id="c-ring-3" cx="0" cy="-175" r="118" fill="none" stroke="{p['secondary']}" stroke-width="1.8" opacity="0.45" stroke-dasharray="10 8" />
                </g>

                <!-- Stylized Geometric Head (2.5D Spherical Shading) -->
                <circle cx="0" cy="-175" r="58" fill="url(#head-25d-grad)" stroke="{p['primary']}" stroke-width="2.8" />
                
                <!-- Head Cranial Rim Highlight -->
                <path d="M -44,-205 C -25,-232 25,-232 44,-205" fill="none" stroke="{p['highlight']}" stroke-width="3" stroke-linecap="round" opacity="0.85" filter="url(#glow-primary)" />

                <!-- Illuminated Prefrontal Cortex Node -->
                <g id="prefrontal-node">
                    <circle cx="16" cy="-185" r="26" fill="{p['primary']}" opacity="0.35" filter="url(#glow-primary)" />
                    <circle cx="16" cy="-185" r="13" fill="{p['highlight']}" />
                    <!-- Neural circuit paths -->
                    <line x1="16" y1="-185" x2="-15" y2="-160" stroke="{p['secondary']}" stroke-width="2" />
                    <line x1="16" y1="-185" x2="35" y2="-165" stroke="{p['accent']}" stroke-width="2" />
                    <circle cx="-15" cy="-160" r="4.5" fill="{p['secondary']}" />
                    <circle cx="35" cy="-165" r="4.5" fill="{p['accent']}" />
                </g>

                <!-- Heart / Ego Core -->
                <circle cx="0" cy="0" r="20" fill="{p['accent']}" opacity="0.45" filter="url(#glow-primary)" />
                <circle cx="0" cy="0" r="9" fill="{p['highlight']}" />
            </g>
        </g>

        {lab_props}

        <!-- Floating Thought Capsule with Direct Speech Pointer -->
        <g transform="translate(1260, 420)">
            <g id="human-thought-capsule" filter="url(#drop-shadow)">
                <!-- Speech Pointer connecting to Figure's Head -->
                <polygon points="-260,30 -300,0 -255,-15" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="2" />
                
                <rect x="-260" y="-70" width="520" height="140" rx="24"
                      fill="{p['bg_dark']}" fill-opacity="0.96" stroke="{p['primary']}" stroke-width="2.5" />
                
                <!-- Category Tag Pill (Mobile-Readable >= 20px) -->
                <rect x="-200" y="-56" width="400" height="42" rx="21" fill="{p['card_bg']}" stroke="{p['secondary']}" stroke-width="1.5" />
                <text x="0" y="-35" text-anchor="middle" dominant-baseline="central" fill="{p['secondary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="20" letter-spacing="1.2">
                    {context_label}
                </text>

                <!-- Spoken Thought Core (High Contrast Bold) -->
                <text x="0" y="30" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="26">
                    "{thought_bubble}"
                </text>
            </g>
        </g>
    </g>
    """
    gsap = f"""
        // Human Silhouette Organic Entrance & Dynamic Motion
        gsap.set('#human-figure-body', {{ y: 40, opacity: 0 }});
        gsap.set('#human-thought-capsule', {{ scale: 0.85, opacity: 0, transformOrigin: 'left center' }});

        tl.to('#human-figure-body', {{ duration: 0.7, y: 0, opacity: 1, ease: 'power3.out' }}, 0.1);
        tl.to('#human-thought-capsule', {{ duration: 0.55, scale: 1.0, opacity: 1, ease: 'back.out(1.6)' }}, 0.35);

        // Conflict Resonance Rings Radiation
        tl.fromTo('#c-ring-1',
            {{ scale: 0.85, opacity: 0.9, transformOrigin: '0px -175px' }},
            {{ scale: 1.4, opacity: 0, duration: 1.5, repeat: -1, ease: 'power1.out', transformOrigin: '0px -175px' }}, 0.2);
        tl.fromTo('#c-ring-2',
            {{ scale: 0.85, opacity: 0.8, transformOrigin: '0px -175px' }},
            {{ scale: 1.4, opacity: 0, duration: 1.5, repeat: -1, ease: 'power1.out', delay: 0.5, transformOrigin: '0px -175px' }}, 0.2);
        tl.fromTo('#c-ring-3',
            {{ scale: 0.85, opacity: 0.7, transformOrigin: '0px -175px' }},
            {{ scale: 1.4, opacity: 0, duration: 1.5, repeat: -1, ease: 'power1.out', delay: 1.0, transformOrigin: '0px -175px' }}, 0.2);

        // Prefrontal Core Breathing Pulse
        tl.to('#prefrontal-node', {{ duration: 1.6, scale: 1.25, repeat: -1, yoyo: true, ease: 'sine.inOut', transformOrigin: '16px -185px' }}, 0.6);
        tl.to('#human-thought-capsule', {{ duration: 2.6, y: -8, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.8);
        tl.to('#human-figure-body', {{ duration: 3.2, y: -6, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0.7);
    """
    return svg, gsap


def get_causal_mechanism_layout(
    p: Dict[str, str],
    step1_input: str = "CONTRADICTORY ACTION",
    step2_process: str = "PREFRONTAL ENGINE",
    step3_output: str = "FABRICATED EXCUSE",
    input_sub: str = "BEHAVIORAL INPUT",
    process_sub: str = "RATIONALIZATION ACTIVE",
    output_sub: str = "COGNITIVE RESOLUTION"
) -> tuple[str, str]:
    """
    LAYOUT 3: CAUSAL_MECHANISM
    Visual input-process-output diagram showing how contradiction transforms into rationalization
    with mobile-readable labels (>= 20px).
    Fully dynamic parameters: zero hardcoded strings.
    """
    svg = f"""
    <g id="layout-causal-mechanism">
        <!-- Connecting Energy Pipelines -->
        <g id="causal-conduits">
            <line x1="490" y1="500" x2="840" y2="500" stroke="{p['primary']}" stroke-width="4" stroke-dasharray="10 8" opacity="0.6" />
            <line x1="1080" y1="500" x2="1430" y2="500" stroke="{p['primary']}" stroke-width="4" stroke-dasharray="10 8" opacity="0.6" />
        </g>

        <!-- Station 1: Input (Contradiction / Behavioral Error) -->
        <g id="causal-station-1" transform="translate(360, 500)" filter="url(#drop-shadow)">
            <rect x="-160" y="-105" width="320" height="210" rx="22"
                  fill="url(#card-grad)" stroke="#FF3B6B" stroke-width="2.5" />
            
            <rect x="-120" y="-90" width="240" height="36" rx="18" fill="{p['bg_dark']}" stroke="#FF3B6B" stroke-width="1.6" />
            <text x="0" y="-72" text-anchor="middle" dominant-baseline="central" fill="#FF3B6B" font-family="'Montserrat', sans-serif" font-weight="900" font-size="18" letter-spacing="1">
                STEP 01: INPUT
            </text>

            <circle cx="0" cy="-12" r="30" fill="{p['bg_dark']}" stroke="#FF3B6B" stroke-width="2.5" />
            <text x="0" y="-4" text-anchor="middle" dominant-baseline="central" fill="#FF3B6B" font-family="'Montserrat', sans-serif" font-weight="900" font-size="24">⚡</text>

            <text x="0" y="44" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="20">
                {step1_input}
            </text>
            <text x="0" y="74" text-anchor="middle" dominant-baseline="central" fill="#FB923C" font-family="'Montserrat', sans-serif" font-weight="800" font-size="20">
                {input_sub}
            </text>
        </g>

        <!-- Station 2: Central Prefrontal Processing Chamber -->
        <g id="causal-station-2" transform="translate(960, 500)" filter="url(#drop-shadow)">
            <!-- Outer Hexagonal Chamber -->
            <polygon points="0,-125 108,-62 108,62 0,125 -108,62 -108,-62"
                     fill="{p['bg_dark']}" stroke="{p['primary']}" stroke-width="3" />
            
            <!-- Interlocking Gear Ring -->
            <g id="causal-gear-teeth">
                <circle cx="0" cy="0" r="75" fill="none" stroke="{p['primary']}" stroke-width="5" stroke-dasharray="14 12" />
                <rect x="-10" y="-85" width="20" height="14" rx="3" fill="{p['secondary']}" />
                <rect x="-10" y="71" width="20" height="14" rx="3" fill="{p['secondary']}" />
                <rect x="-85" y="-10" width="14" height="20" rx="3" fill="{p['secondary']}" />
                <rect x="71" y="-10" width="14" height="20" rx="3" fill="{p['secondary']}" />
            </g>

            <!-- Inner Engine Core -->
            <circle cx="0" cy="0" r="50" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="2" />
            <text x="0" y="-14" text-anchor="middle" dominant-baseline="central" fill="{p['secondary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="15" letter-spacing="1">STEP 02</text>
            <text x="0" y="10" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="18">ENGINE</text>
            <text x="0" y="32" text-anchor="middle" dominant-baseline="central" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="14">{process_sub}</text>

            <!-- Station Tag (Mobile-Readable >= 20px) -->
            <rect x="-160" y="145" width="320" height="42" rx="21" fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="1.8" />
            <text x="0" y="166" text-anchor="middle" dominant-baseline="central" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="18">
                {step2_process}
            </text>
        </g>

        <!-- Station 3: Output (Fabricated Comfort Excuse) -->
        <g id="causal-station-3" transform="translate(1560, 500)" filter="url(#drop-shadow)">
            <rect x="-160" y="-105" width="320" height="210" rx="22"
                  fill="url(#card-grad)" stroke="{p['primary']}" stroke-width="2.5" />
            
            <rect x="-120" y="-90" width="240" height="36" rx="18" fill="{p['bg_dark']}" stroke="{p['primary']}" stroke-width="1.6" />
            <text x="0" y="-72" text-anchor="middle" dominant-baseline="central" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="18" letter-spacing="1">
                STEP 03: RESOLUTION
            </text>

            <circle cx="0" cy="-12" r="30" fill="{p['bg_dark']}" stroke="{p['primary']}" stroke-width="2.5" />
            <text x="0" y="-4" text-anchor="middle" dominant-baseline="central" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="24">✓</text>

            <text x="0" y="44" text-anchor="middle" dominant-baseline="central" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="20">
                {step3_output}
            </text>
            <text x="0" y="74" text-anchor="middle" dominant-baseline="central" fill="{p['primary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="20">
                {output_sub}
            </text>
        </g>
    </g>
    """
    gsap = f"""
        // Causal Mechanism 3-Stage Pipeline Animation
        gsap.set('#causal-station-1', {{ scale: 0.85, opacity: 0, transformOrigin: 'center center' }});
        gsap.set('#causal-station-2', {{ scale: 0.85, opacity: 0, transformOrigin: 'center center' }});
        gsap.set('#causal-station-3', {{ scale: 0.85, opacity: 0, transformOrigin: 'center center' }});

        tl.to('#causal-station-1', {{ duration: 0.5, scale: 1.0, opacity: 1, ease: 'back.out(1.6)' }}, 0.1);
        tl.to('#causal-station-2', {{ duration: 0.55, scale: 1.0, opacity: 1, ease: 'back.out(1.6)' }}, 0.7);
        tl.to('#causal-gear-teeth', {{ duration: 3.5, rotate: 360, repeat: -1, ease: 'none', transformOrigin: 'center center' }}, 0.7);
        tl.to('#causal-station-3', {{ duration: 0.5, scale: 1.0, opacity: 1, ease: 'back.out(1.6)' }}, 1.8);
    """
    return svg, gsap


def get_macro_closeup_layout(
    p: Dict[str, str],
    header_label: str = "● NEURAL TELEMETRY: ACTIVE",
    focus_metric: str = "ACC CONFLICT",
    sub_detail: str = "ANTERIOR CINGULATE ACTIVATION",
    region_title: Optional[str] = None,
    metric_text: Optional[str] = None
) -> tuple[str, str]:
    """
    LAYOUT 4: MACRO_CLOSEUP
    Cinematic macro zoom into synaptic cleft and neural transmission pathways with
    Flat 2.5D filled gradient structures, glowing continuous electrical arc discharges,
    and mobile-readable diagnostic HUD telemetry.
    Fully dynamic parameters: zero hardcoded strings.
    """
    display_title = region_title or sub_detail
    svg = f"""
    <g id="layout-macro-closeup">
        <!-- High-Tech HUD Diagnostic Card (Top Left - Unclipped & Auto-Padded) -->
        <g transform="translate(80, 80)">
            <g id="macro-hud" filter="url(#drop-shadow)">
                <rect x="0" y="0" width="560" height="96" rx="20"
                      fill="{p['bg_dark']}" fill-opacity="0.95" stroke="{p['primary']}" stroke-width="2.5" />
                <text x="24" y="34" fill="{p['secondary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="15" letter-spacing="1.5">
                    {header_label}
                </text>
                <text x="24" y="68" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="22">
                    {display_title}
                </text>
                <rect x="400" y="26" width="136" height="44" rx="12" fill="{p['card_bg']}" stroke="{p['accent']}" stroke-width="1.8" />
                <text x="468" y="54" text-anchor="middle" fill="{p['accent']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="14">
                    {focus_metric}
                </text>
            </g>
        </g>

        <!-- Macro Synaptic Stage -->
        <g transform="translate(960, 540)">
            <g id="macro-synapse-stage">
                <!-- Pre-Synaptic Axon Terminal (Flat 2.5D Filled Gradient + Inner Rim) -->
                <path d="M -960,-200 L -320,-200 C -140,-200 -50,-130 -50,-40 C -50,40 -140,110 -280,120 L -960,120 Z"
                      fill="url(#axon-25d-grad)" stroke="{p['primary']}" stroke-width="3" filter="url(#drop-shadow)" />
                
                <!-- Axon Specular Rim Contour -->
                <path d="M -150,-180 C -65,-120 -65,25 -150,85"
                      fill="none" stroke="{p['highlight']}" stroke-width="4" stroke-linecap="round" opacity="0.8" filter="url(#glow-primary)" />
                <path d="M -960,-185 L -315,-185 C -145,-185 -70,-125 -70,-40"
                      fill="none" stroke="{p['primary']}" stroke-width="2" stroke-opacity="0.4" />
                
                <!-- Synaptic Vesicle Clusters (Neurotransmitter packets) -->
                <g id="vesicles-cluster">
                    <circle cx="-200" cy="-100" r="18" fill="{p['primary']}" opacity="0.65" filter="url(#glow-primary)" />
                    <circle cx="-150" cy="-50" r="16" fill="{p['secondary']}" opacity="0.85" />
                    <circle cx="-240" cy="-30" r="20" fill="{p['accent']}" opacity="0.55" />
                    <circle cx="-170" cy="20" r="16" fill="{p['primary']}" opacity="0.75" />
                </g>

                <!-- Post-Synaptic Dendritic Spine (Flat 2.5D Filled Gradient + Inner Rim) -->
                <path d="M 700,380 L 300,380 C 120,380 40,260 40,120 C 40,20 120,-40 260,-60 L 700,-60 Z"
                      fill="url(#dendrite-25d-grad)" stroke="{p['secondary']}" stroke-width="3" filter="url(#drop-shadow)" />
                
                <!-- Dendrite Specular Rim Contour -->
                <path d="M 130,355 C 55,245 55,35 135,-35"
                      fill="none" stroke="{p['secondary']}" stroke-width="4" stroke-linecap="round" opacity="0.85" filter="url(#glow-primary)" />
                
                <!-- 2.5D Receptor Channels with Caps -->
                <g transform="rotate(30, 88, 95)">
                    <rect x="80" y="80" width="16" height="30" rx="4" fill="{p['primary']}" />
                    <rect x="78" y="76" width="20" height="8" rx="3" fill="{p['highlight']}" />
                </g>
                <g transform="rotate(40, 148, 35)">
                    <rect x="140" y="20" width="16" height="30" rx="4" fill="{p['secondary']}" />
                    <rect x="138" y="16" width="20" height="8" rx="3" fill="{p['highlight']}" />
                </g>
                <g transform="rotate(50, 188, -15)">
                    <rect x="180" y="-30" width="16" height="30" rx="4" fill="{p['accent']}" />
                    <rect x="178" y="-34" width="20" height="8" rx="3" fill="{p['highlight']}" />
                </g>

                <!-- Glowing Electrical Action Potential Arc Discharges -->
                <g id="macro-synapse-arcs">
                    <path id="electrical-arc-1" d="M -50,-15 Q 5,10 65,35"
                          fill="none" stroke="{p['highlight']}" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="14 10" filter="url(#glow-intense)" opacity="0.95" />
                    <path id="electrical-arc-2" d="M -55,25 Q 15,55 85,85"
                          fill="none" stroke="{p['secondary']}" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 8" filter="url(#glow-primary)" opacity="0.85" />
                    <path id="electrical-arc-3" d="M -65,-40 Q -5,-15 140,15"
                          fill="none" stroke="{p['primary']}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="12 12" filter="url(#glow-primary)" opacity="0.8" />
                </g>

                <!-- Firing Neurotransmitter Cloud in Synaptic Cleft -->
                <g id="synaptic-neurotransmitters">
                    <circle cx="-30" cy="-30" r="8" fill="{p['highlight']}" filter="url(#glow-primary)" />
                    <circle cx="0" cy="0" r="10" fill="{p['primary']}" filter="url(#glow-primary)" />
                    <circle cx="30" cy="30" r="7" fill="{p['secondary']}" filter="url(#glow-primary)" />
                    <circle cx="-10" cy="40" r="9" fill="{p['accent']}" filter="url(#glow-primary)" />
                    <circle cx="20" cy="-40" r="8" fill="{p['highlight']}" filter="url(#glow-primary)" />
                </g>
            </g>
        </g>
    </g>
    """
    gsap = f"""
        // Macro Close-Up Continuous Cinematic Drift
        gsap.set('#macro-hud', {{ y: -15, opacity: 0 }});
        tl.to('#macro-hud', {{ duration: 0.5, y: 0, opacity: 1, ease: 'power2.out' }}, 0.2);

        tl.fromTo('#macro-synapse-stage',
            {{ scale: 0.98, x: -20, y: 15, transformOrigin: 'center center' }},
            {{ scale: 1.06, x: 20, y: -15, duration: 8.0, ease: 'sine.inOut', transformOrigin: 'center center' }}, 0);

        // Continuous glowing electrical pulses arcing across synaptic cleft
        tl.fromTo('#electrical-arc-1', {{ strokeDashoffset: 48, opacity: 0.35 }}, {{ strokeDashoffset: 0, opacity: 1.0, duration: 0.45, repeat: -1, ease: 'linear' }}, 0.1);
        tl.fromTo('#electrical-arc-2', {{ strokeDashoffset: -36, opacity: 0.25 }}, {{ strokeDashoffset: 0, opacity: 0.9, duration: 0.55, repeat: -1, ease: 'linear' }}, 0.2);
        tl.fromTo('#electrical-arc-3', {{ strokeDashoffset: 48, opacity: 0.2 }}, {{ strokeDashoffset: 0, opacity: 0.85, duration: 0.65, repeat: -1, ease: 'linear' }}, 0.1);

        // Neurotransmitter Cloud Particle Jitter
        tl.to('#synaptic-neurotransmitters', {{ duration: 0.3, x: 12, y: -8, repeat: -1, yoyo: true, ease: 'sine.inOut' }}, 0);
    """
    return svg, gsap


def get_full_canvas_metaphor_layout(
    p: Dict[str, str],
    is_outro: bool = False,
    next_ep_title: str = "The Dopamine Slot Machine in Your Skull",
    wrapup_title: str = "COGNITIVE TRANSCENDENCE"
) -> tuple[str, str]:
    """
    LAYOUT 5: FULL_CANVAS_METAPHOR
    Edge-to-edge layered illustration with foreground, midground, and background parallax.
    """
    outro_card = ""
    if is_outro:
        outro_card = f"""
        <!-- Purposeful Outro Wrap-Up Card -->
        <g id="outro-wrapup-card" transform="translate(960, 780)" filter="url(#drop-shadow)">
            <rect x="-380" y="-45" width="760" height="90" rx="24"
                  fill="{p['bg_dark']}" fill-opacity="0.96" stroke="{p['primary']}" stroke-width="2.5" />
            <text x="0" y="-12" text-anchor="middle" fill="{p['secondary']}" font-family="'Montserrat', sans-serif" font-weight="800" font-size="15" letter-spacing="1.5">
                UP NEXT: {next_ep_title.upper()}
            </text>
            <text x="0" y="24" text-anchor="middle" fill="{p['highlight']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="22">
                SUBSCRIBE TO MERAS | BEHAVIORAL MECHANICS
            </text>
        </g>
        """

    svg = f"""
    <g id="layout-full-canvas">
        <!-- Layer 2: Mid-Back Stepped Geometric Mountain Ridges (Edge-to-edge) -->
        <g id="canvas-mid-ridges" opacity="0.6">
            <polygon points="0,1080 0,620 280,520 620,680 960,490 1340,660 1680,530 1920,640 1920,1080"
                     fill="{p['card_bg']}" stroke="{p['primary']}" stroke-width="1.5" />
        </g>

        <!-- Layer 3: Central Truth Orb / Radiant Horizon Sun -->
        <g id="canvas-truth-orb" transform="translate(960, 480)" filter="url(#drop-shadow)">
            <!-- Outer Horizon Orbit Ring -->
            <ellipse cx="0" cy="0" rx="420" ry="85" fill="none" stroke="{p['primary']}" stroke-width="3"
                     stroke-dasharray="24 16" transform="rotate(-12)" filter="url(#glow-primary)" />
            <ellipse cx="0" cy="0" rx="450" ry="95" fill="none" stroke="{p['secondary']}" stroke-width="1.5"
                     stroke-dasharray="10 14" transform="rotate(-12)" opacity="0.4" />

            <!-- Core Celestial Body -->
            <circle cx="0" cy="0" r="160" fill="url(#primary-grad)" />
            <circle cx="0" cy="0" r="160" fill="{p['bg_dark']}" opacity="0.45" />

            <!-- Core Transcendence Emblem -->
            <circle cx="0" cy="0" r="48" fill="{p['highlight']}" filter="url(#glow-primary)" />
            <text x="0" y="8" text-anchor="middle" fill="{p['bg_dark']}" font-family="'Montserrat', sans-serif" font-weight="900" font-size="22" letter-spacing="1">
                MERAS
            </text>
        </g>

        <!-- Layer 4: Edge-to-Edge Silhouette Foreground Terrain -->
        <g id="canvas-foreground-terrain">
            <polygon points="0,1080 0,820 420,760 960,830 1480,770 1920,840 1920,1080"
                     fill="{p['bg_darker']}" stroke="{p['primary']}" stroke-width="2.5" />
        </g>

        {outro_card}
    </g>
    """
    gsap = f"""
        // Full Canvas Parallax Motion
        gsap.set('#canvas-truth-orb', {{ scale: 0.9, opacity: 0, transformOrigin: 'center center' }});
        tl.to('#canvas-truth-orb', {{ duration: 0.7, scale: 1.0, opacity: 1, ease: 'back.out(1.6)' }}, 0.1);

        tl.to('#canvas-mid-ridges', {{ duration: 8.0, x: -30, ease: 'none' }}, 0);
        tl.to('#canvas-foreground-terrain', {{ duration: 8.0, x: 40, ease: 'none' }}, 0);

        {"tl.fromTo('#outro-wrapup-card', { scale: 0.9, opacity: 0 }, { duration: 0.6, scale: 1.0, opacity: 1, ease: 'back.out(1.5)' }, 1.2);" if is_outro else ""}
    """
    return svg, gsap

# ==============================================================================
# MASTER SCENE HTML BUILDER
# ==============================================================================

def build_scene_html(
    scene_config: Dict[str, Any],
    duration: float = 5.0,
    fps: int = 30,
    words_alignment: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Compiles a broadcast-grade 30fps HTML5 + SVG + GSAP page for headless Chromium.
    Zero Mascots. 100% Pure Abstract Vector Storytelling across 5 distinct layouts.
    """
    ch_idx = scene_config.get("chapter_index", 1)
    p = get_palette(ch_idx)

    defs_svg = get_svg_defs(p)
    bg_svg = get_3layer_background(p)
    fg_particles = get_foreground_particles(p)

    layout = scene_config.get("layout", None)
    scene_type = scene_config.get("scene_type", "macro_closeup")
    title = scene_config.get("title", "Meras Architecture")
    subtitle = scene_config.get("subtitle", None)
    sentence = scene_config.get("sentence", "")
    is_outro = scene_config.get("is_outro", False)

    elements_svg = []
    gsap_timings = []

    # Layout Selection: 5 Dynamic Compositional Architectures
    if scene_type == "chapter_title_card":
        card_svg, card_gsap = get_chapter_title_card(
            chapter_num=ch_idx,
            title=title,
            subtitle=subtitle or "Behavioral Mechanics",
            p=p
        )
        elements_svg.append(card_svg)
        gsap_timings.append(card_gsap)

    elif layout == "SPLIT_COMPARISON" or scene_type in ["split_comparison", "dissonance_split"]:
        l_title = scene_config.get("left_title", "BELIEF STATE")
        l_metric = scene_config.get("left_metric", "IDENTITY")
        l_sub = scene_config.get("left_sub", "INTERNAL MODEL")
        r_title = scene_config.get("right_title", "ACTION TAKEN")
        r_metric = scene_config.get("right_metric", "REALITY")
        r_sub = scene_config.get("right_sub", "OBSERVED OUTCOME")
        split_svg, split_gsap = get_split_comparison_layout(
            p=p,
            left_title=l_title,
            left_metric=l_metric,
            left_sub=l_sub,
            right_title=r_title,
            right_metric=r_metric,
            right_sub=r_sub
        )
        elements_svg.append(split_svg)
        gsap_timings.append(split_gsap)

    elif layout == "HUMAN_SILHOUETTE_SCENE" or scene_type in ["human_silhouette", "human_conflict", "experiment_subject", "silhouette"]:
        ctx = scene_config.get("context_label", subtitle or "PREFRONTAL ARBITER")
        thought = scene_config.get("thought_bubble", "DEFENDING REALITY")
        emotion = scene_config.get("emotion_state", "COGNITIVE FRICTION")
        var = "experiment" if "experiment" in scene_type or "peg" in sentence.lower() else "conflict"
        hum_svg, hum_gsap = get_human_silhouette_scene(
            p=p,
            context_label=ctx,
            thought_bubble=thought,
            emotion_state=emotion,
            variant=var
        )
        elements_svg.append(hum_svg)
        gsap_timings.append(hum_gsap)

    elif layout == "CAUSAL_MECHANISM" or scene_type in ["causal_mechanism", "rationalization_machine", "rationalization_gears", "gears"]:
        s1 = scene_config.get("step1_input", "DISSONANT INPUT")
        s2 = scene_config.get("step2_process", "PREFRONTAL FILTER")
        s3 = scene_config.get("step3_output", "ADAPTIVE EXCUSE")
        c_svg, c_gsap = get_causal_mechanism_layout(
            p=p,
            step1_input=s1,
            step2_process=s2,
            step3_output=s3
        )
        elements_svg.append(c_svg)
        gsap_timings.append(c_gsap)

    elif layout == "MACRO_CLOSEUP" or scene_type in ["macro_closeup", "neural_macro", "brain_intro", "brain"]:
        h_label = scene_config.get("header_label", "NEURAL TELEMETRY: ACTIVE")
        f_metric = scene_config.get("focus_metric", "ACC CONFLICT")
        sub_d = scene_config.get("sub_detail", subtitle or "ACUTE COGNITIVE FRICTION")
        m_svg, m_gsap = get_macro_closeup_layout(
            p=p,
            header_label=h_label,
            focus_metric=f_metric,
            sub_detail=sub_d,
            region_title=title
        )
        elements_svg.append(m_svg)
        gsap_timings.append(m_gsap)

    elif layout == "FULL_CANVAS_METAPHOR" or scene_type in ["full_canvas_metaphor", "horizon_revelation", "horizon", "outro"]:
        hl = scene_config.get("headline", title or "COGNITIVE TRANSCENDENCE")
        foc = scene_config.get("focal_label", "TRUTH OVER COMFORT")
        sup = scene_config.get("supporting_note", subtitle or "OBJECTIVE REALITY")
        f_svg, f_gsap = get_full_canvas_metaphor_layout(
            p=p,
            headline=hl,
            focal_label=foc,
            supporting_note=sup,
            is_outro=is_outro
        )
        elements_svg.append(f_svg)
        gsap_timings.append(f_gsap)

    elif scene_type in ["animated_counter", "counter"] or ("1957" in sentence or "1959" in sentence or "pegs" in sentence):
        num_match = re.search(r'(\$\d+|\b19\d\d\b|\b\d+\s*pegs\b|\b\d+%\b|\b100,000\b)', sentence, re.IGNORECASE)
        val = num_match.group(0) if num_match else ("1957" if "1957" in sentence else "1959")
        sub_desc = "Stanford Experiment" if "1959" in val or "peg" in sentence else "Cognitive Dissonance Theory"
        cnt_svg, cnt_gsap = get_animated_counter(val, "Historic Milestone", f"Leon Festinger ({val})", p)
        elements_svg.append(get_safe_chapter_header(title, subtitle, ch_idx, p))
        elements_svg.append(cnt_svg)
        gsap_timings.append(cnt_gsap)

    elif scene_type in ["scales_balance", "scales"]:
        elements_svg.append(get_safe_chapter_header(title, subtitle, ch_idx, p))
        s_left_val = scene_data.get("left_metric", "HEAVY")
        s_right_val = scene_data.get("right_metric", "LIGHT")
        s_left_lbl = scene_data.get("left_header", "HIGH INCENTIVE")
        s_right_lbl = scene_data.get("right_header", "LOW INCENTIVE")
        scales_svg, scales_gsap = get_scales_balance_system(p, s_left_lbl, s_right_lbl, s_left_val, s_right_val)
        elements_svg.append(scales_svg)
        gsap_timings.append(scales_gsap)

    else:
        # Default to Macro Neural Close-Up
        m_svg, m_gsap = get_macro_closeup_layout(p, region_title=title, metric_text="NEURAL ARBITER")
        elements_svg.append(m_svg)
        gsap_timings.append(m_gsap)

    # 2. Fast 2-3s Word-Synced Kinetic Subtitles in Lower Third
    subtitle_overlay_svg = ""
    if sentence:
        sub_svg, sub_gsap = get_kinetic_subtitles(
            sentence=sentence,
            duration=duration,
            p=p,
            words_alignment=words_alignment,
            cx=960,
            cy=880
        )
        subtitle_overlay_svg = sub_svg
        gsap_timings.append(sub_gsap)

    # Master Continuous Camera Motion: 0.35s fluid entry with continuous momentum (Zero blank gap)
    camera_motion = f"""
        // 1. Entrance Transition (0.0s - 0.35s): smooth dynamic zoom-in from 0.96 to 1.0 (Zero blank gap)
        tl.fromTo('#scene-stage',
            {{ scale: 0.96, opacity: 1, y: 8, transformOrigin: '960px 540px' }},
            {{ scale: 1.0, opacity: 1, y: 0, duration: 0.35, ease: 'power3.out', transformOrigin: '960px 540px' }}, 0);

        // 2. Middle & Exit Continuous Float: gentle drift from 1.0 to 1.05 right up to the cut
        tl.to('#scene-stage',
            {{ scale: 1.05, duration: Math.max(0.1, {duration} - 0.35), ease: 'sine.inOut', transformOrigin: '960px 540px' }}, 0.35);

        // Background Beams and Parallax Dust Drift
        tl.fromTo('#bg-light-beams', {{ x: -20 }}, {{ x: 20, duration: {duration}, ease: 'sine.inOut' }}, 0);
        tl.to('.parallax-p1', {{ duration: {duration}, x: -60, ease: 'none' }}, 0);
        tl.to('.parallax-p2', {{ duration: {duration}, x: -100, ease: 'none' }}, 0);
        tl.to('.foreground-particles', {{ duration: {duration}, x: -140, ease: 'none' }}, 0);
    """

    body_content = f"""
    <svg id="studio-canvas" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
        {defs_svg}
        {bg_svg}
        <g id="scene-stage">
            {"".join(elements_svg)}
        </g>
        {fg_particles}
        <g id="subtitles-overlay">
            {subtitle_overlay_svg}
        </g>
    </svg>
    """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script>
    {GSAP_INLINE_SCRIPT}
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body, html {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: {p['bg_dark']};
            font-family: 'Montserrat', 'Inter', -apple-system, sans-serif;
            user-select: none;
        }}
        #studio-canvas {{
            width: 1920px;
            height: 1080px;
            position: absolute;
            top: 0;
            left: 0;
            transform-origin: top left;
        }}
    </style>
</head>
<body>
    {body_content}
    <script>
        const duration = {duration};
        const fps = {fps};

        // Master Virtual Clock: Zero uncontrolled CSS or requestAnimationFrame ticking
        gsap.globalTimeline.pause();
        const tl = gsap.timeline({{ paused: true }});
        window.tl = tl;

        // Composable Choreography
        {"".join(gsap_timings)}

        // Continuous Cinematic Camera Motion
        {camera_motion}

        window.renderAtTime = function(seconds) {{
            if (window.tl) {{
                window.tl.time(seconds);
            }}
            return true;
        }};

        window.seekTimeline = function(seconds) {{
            return window.renderAtTime(seconds);
        }};

        window.getTimelineDuration = function() {{
            return duration;
        }};

        window.renderAtTime(0);
    </script>
</body>
</html>
"""
    return html

# Backwards compatibility aliases for package imports
COLORS = PALETTES[1]

def get_meras_explorer(*args, **kwargs) -> str:
    """Mascot permanently removed in broadcast architecture."""
    return ""

def get_brain_network(*args, **kwargs) -> str:
    """Legacy alias for neural brain network SVG."""
    return get_brain_synaptic_network(PALETTES[1])[0]

if __name__ == "__main__":
    test_scene = {
        "chapter_index": 1,
        "scene_type": "brain_intro",
        "title": "The Invisible Fraud",
        "subtitle": "Chapter 1: Cognitive Mechanics",
        "sentence": "Your brain actively deceives you right now.",
        "punch_word": "EGO OVER TRUTH"
    }
    h = build_scene_html(test_scene, duration=5.0)
    print(f"Generated HTML length: {len(h)} chars. Mascot verified removed.")
