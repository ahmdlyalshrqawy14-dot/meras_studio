"""
Meras Studio - Master Production Script for Episode 01:
"Why Your Brain Loves Being Lied To" (Cognitive Dissonance & Self-Justification)
"""

import sys
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(STUDIO_ROOT))

from run_studio import run_production_pipeline

if __name__ == "__main__":
    run_production_pipeline(episode_num=1, is_verification=False, fps=30)
