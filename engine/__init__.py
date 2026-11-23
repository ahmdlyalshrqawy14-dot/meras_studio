"""
Meras Studio Engine Package
Automated Kurzgesagt-Inspired Vector Animation Production Pipeline
"""

from .voice_engine import generate_voice, build_ssml, extract_word_timestamps
from .kurzgesagt_art_kit import build_scene_html, COLORS, get_svg_defs, get_meras_explorer, get_brain_network
from .motion_renderer import render_scene_plan, render_scene_clip
from .compositor import composite_video
from .thumbnail_gen import generate_thumbnail
from .sfx_generator import build_all_sfx

__all__ = [
    "generate_voice",
    "build_ssml",
    "extract_word_timestamps",
    "build_scene_html",
    "COLORS",
    "get_svg_defs",
    "get_meras_explorer",
    "get_brain_network",
    "render_scene_plan",
    "render_scene_clip",
    "composite_video",
    "generate_thumbnail",
    "build_all_sfx"
]
