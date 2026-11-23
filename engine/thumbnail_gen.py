"""
Meras Studio Thumbnail Generator
Renders 1280x720 vector YouTube thumbnails in Kurzgesagt flat 2.5D style:
- 100% Mascot-Free: Clean, bold vector hero illustration (Glowing Cognitive Prism & Neural Synaptic Core)
- High-contrast, vibrant 3-word curiosity hook
- High-CTR typography and dark obsidian background
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

STUDIO_ROOT = Path(__file__).resolve().parent.parent

def build_thumbnail_html(
    hook_3_words: str,
    episode_num: int = 1,
    category: str = "BEHAVIORAL MECHANICS",
    primary_color: str = "#00E5FF",
    secondary_color: str = "#FF3B6B",
    amber_color: str = "#FFB800"
) -> str:
    """Builds HTML for 1280x720 vector thumbnail."""
    words = hook_3_words.strip().split()
    w1 = words[0].upper() if len(words) > 0 else "YOUR"
    w2 = words[1].upper() if len(words) > 1 else "MIND"
    w3 = words[2].upper() if len(words) > 2 else "LIES"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body, html {{
            width: 1280px;
            height: 720px;
            overflow: hidden;
            background-color: #090D24;
            font-family: 'Montserrat', sans-serif;
        }}
        svg {{ width: 1280px; height: 720px; position: absolute; top: 0; left: 0; }}
    </style>
</head>
<body>
    <svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="thumb-bg" cx="65%" cy="50%" r="80%">
                <stop offset="0%" stop-color="#192252" />
                <stop offset="50%" stop-color="#0E1433" />
                <stop offset="100%" stop-color="#050714" />
            </radialGradient>

            <linearGradient id="hook-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="{amber_color}" />
                <stop offset="100%" stop-color="{secondary_color}" />
            </linearGradient>

            <linearGradient id="cyan-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="{primary_color}" />
                <stop offset="100%" stop-color="#38BDF8" />
            </linearGradient>

            <filter id="thumb-glow" x="-30%" y="-30%" width="160%" height="160%">
                <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b1" />
                <feGaussianBlur in="SourceGraphic" stdDeviation="28" result="b2" />
                <feMerge>
                    <feMergeNode in="b2" />
                    <feMergeNode in="b1" />
                    <feMergeNode in="SourceGraphic" />
                </feMerge>
            </filter>

            <filter id="hero-shadow" x="-30%" y="-30%" width="160%" height="160%">
                <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#000000" flood-opacity="0.8" />
            </filter>
        </defs>

        <!-- Background -->
        <rect width="1280" height="720" fill="url(#thumb-bg)" />

        <!-- Ambient Light Rays -->
        <g opacity="0.3">
            <polygon points="860,0 600,720 740,720" fill="{primary_color}" opacity="0.15" filter="url(#thumb-glow)" />
            <polygon points="860,0 1020,720 1180,720" fill="{secondary_color}" opacity="0.12" filter="url(#thumb-glow)" />
        </g>

        <!-- Category & Episode Badge -->
        <g transform="translate(80, 85)">
            <rect x="0" y="0" width="280" height="42" rx="21" fill="#13193C" stroke="{primary_color}" stroke-width="2" />
            <circle cx="21" cy="21" r="5" fill="{primary_color}" filter="url(#thumb-glow)" />
            <text x="145" y="27" text-anchor="middle" fill="{primary_color}" font-weight="900" font-size="16" letter-spacing="2">
                EPISODE 0{episode_num} • {category}
            </text>
        </g>

        <!-- Bold High-CTR 3-Word Hook (Massive Typography) -->
        <g transform="translate(80, 240)">
            <text x="0" y="0" fill="#FFFFFF" font-weight="900" font-size="88" letter-spacing="-1">
                {w1}
            </text>
            <text x="0" y="90" fill="url(#cyan-grad)" font-weight="900" font-size="88" letter-spacing="-1" filter="url(#thumb-glow)">
                {w2}
            </text>
            <text x="0" y="180" fill="url(#hook-grad)" font-weight="900" font-size="88" letter-spacing="-1">
                {w3}
            </text>
        </g>

        <!-- Central Vector Hero: Glowing Cognitive Prism & Neural Core (100% Mascot-Free) -->
        <g id="thumb-hero" transform="translate(880, 360)" filter="url(#hero-shadow)">
            <!-- Outer Geometric Hexagonal Energy Field -->
            <polygon points="-160,-190 160,-190 220,160 -220,160" fill="#12183D" stroke="{primary_color}" stroke-width="3.5" opacity="0.95" />
            <polygon points="-160,-190 0,-215 160,-190 0,185" fill="{primary_color}" opacity="0.08" />

            <!-- Glowing Cerebral Synaptic Core -->
            <circle cx="0" cy="-15" r="95" fill="url(#cyan-grad)" opacity="0.25" filter="url(#thumb-glow)" />
            <circle cx="0" cy="-15" r="60" fill="{primary_color}" opacity="0.4" filter="url(#thumb-glow)" />
            <circle cx="0" cy="-15" r="28" fill="#FFFFFF" filter="url(#thumb-glow)" />

            <!-- Synaptic Axon Network Lines -->
            <line x1="-80" y1="-70" x2="-20" y2="-15" stroke="{primary_color}" stroke-width="3" />
            <line x1="80" y1="-70" x2="20" y2="-15" stroke="{primary_color}" stroke-width="3" />
            <line x1="-60" y1="50" x2="-15" y2="-5" stroke="{primary_color}" stroke-width="3" />
            <line x1="60" y1="50" x2="15" y2="-5" stroke="{primary_color}" stroke-width="3" />

            <!-- Warning Glitch Badge -->
            <g transform="translate(-85, 95)">
                <rect x="0" y="0" width="170" height="42" rx="21" fill="#090D24" stroke="{amber_color}" stroke-width="2.5" />
                <text x="85" y="27" text-anchor="middle" fill="{amber_color}" font-weight="900" font-size="16" letter-spacing="2">
                    ⚠ GLITCH
                </text>
            </g>
        </g>
    </svg>
</body>
</html>
"""
    return html

def generate_thumbnail(
    hook_3_words: str,
    output_path: str,
    episode_num: int = 1,
    category: str = "BEHAVIORAL MECHANICS",
    primary_color: str = "#00E5FF",
    secondary_color: str = "#FF3B6B",
    amber_color: str = "#FFB800"
) -> str:
    """Renders 1280x720 thumbnail PNG using Playwright Chromium."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    html_content = build_thumbnail_html(
        hook_3_words=hook_3_words,
        episode_num=episode_num,
        category=category,
        primary_color=primary_color,
        secondary_color=secondary_color,
        amber_color=amber_color
    )

    temp_html = os.path.join(os.path.dirname(output_path), "thumb_render.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--force-dark-mode"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto("file:///" + temp_html.replace("\\", "/"))
        page.wait_for_timeout(100)
        page.screenshot(path=output_path)
        browser.close()

    if os.path.exists(temp_html):
        os.remove(temp_html)

    print(f"[ThumbnailGen] Vector thumbnail rendered -> {output_path} ({os.path.getsize(output_path)} bytes)")
    return output_path

if __name__ == "__main__":
    test_out = str(STUDIO_ROOT / "temp" / "test_thumb.png")
    generate_thumbnail("YOUR MIND LIES", test_out, 1)
