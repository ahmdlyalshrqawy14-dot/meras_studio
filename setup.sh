#!/usr/bin/env bash
# ==============================================================================
# MERAS STUDIO - AUTOMATED ENVIRONMENT SETUP SCRIPT
# Sets up Python virtual environment, dependencies, Playwright, and configuration.
# ==============================================================================

set -euo pipefail

echo "======================================================================"
echo "🚀 Initializing Meras Studio Production Environment"
echo "======================================================================"

# Determine project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Check Python version
if command -v python3 &>/dev/null; then
    PY_BIN="python3"
elif command -v python &>/dev/null; then
    PY_BIN="python"
else
    echo "❌ Error: Python 3 is required but neither python3 nor python was found."
    exit 1
fi

PY_VERSION=$($PY_BIN -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Found Python: $PY_BIN (version $PY_VERSION)"

# 2. Check FFmpeg installation
if command -v ffmpeg &>/dev/null; then
    echo "✓ Found FFmpeg: $(ffmpeg -version | head -n 1)"
else
    echo "⚠️ Warning: FFmpeg not detected in PATH. Required for rendering video clips."
    echo "  Please install FFmpeg (e.g., sudo apt-get install ffmpeg or winget install Gyan.FFmpeg)"
fi

# 3. Virtual environment setup
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment in ./venv..."
    $PY_BIN -m venv venv
else
    echo "✓ Existing virtual environment detected in ./venv"
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    # Linux / macOS
    # shellcheck disable=SC1091
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    # Git Bash on Windows
    # shellcheck disable=SC1091
    source venv/Scripts/activate
fi

# 4. Install dependencies
echo "📥 Upgrading pip and installing required Python packages..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Install Playwright Chromium headless shell
echo "🌐 Installing Playwright Chromium browser binary..."
python -m playwright install chromium

# 6. Initialize .env from template if missing
if [ ! -f ".env" ]; then
    echo "📄 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️ Reminder: Review and update .env with your personal credentials if needed."
else
    echo "✓ Existing .env file preserved."
fi

# 7. Create necessary asset and cache folders
mkdir -p assets/sfx output temp

echo ""
echo "======================================================================"
echo "✅ Meras Studio setup complete! Ready for documentary generation."
echo "   Run a verification test: python run_studio.py --verify"
echo "======================================================================"
