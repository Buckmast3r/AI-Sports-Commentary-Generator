#!/bin/bash
# Setup script for AI Sports Commentary Generator

set -e

echo "================================="
echo "AI Sports Commentary Generator"
echo "Setup Script"
echo "================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 is required but not installed. Aborting."; exit 1; }

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create config from example
if [ ! -f "config.json" ]; then
    echo ""
    echo "Creating config.json from template..."
    cp config.example.json config.json
    echo "✓ config.json created. Please edit it with your settings."
else
    echo ""
    echo "✓ config.json already exists."
fi

# Create output directories
echo ""
echo "Creating output directories..."
mkdir -p output
mkdir -p temp
echo "✓ Directories created."

# Check for Ollama
echo ""
echo "Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"
    echo "  Testing Ollama connection..."
    if ollama list &> /dev/null; then
        echo "  ✓ Ollama is running"
    else
        echo "  ⚠ Ollama may not be running. Start it with: ollama serve"
    fi
else
    echo "⚠ Ollama not found. Install from: https://ollama.ai/"
    echo "  After installing, run: ollama pull llama2"
fi

# Check for FFmpeg
echo ""
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg is installed"
else
    echo "⚠ FFmpeg not found. Install with:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
fi

# Check for Piper
echo ""
echo "Checking for Piper TTS..."
if command -v piper &> /dev/null; then
    echo "✓ Piper is installed"
else
    echo "⚠ Piper not found. Install from: https://github.com/rhasspy/piper"
fi

echo ""
echo "================================="
echo "Setup Complete!"
echo "================================="
echo ""
echo "Next steps:"
echo "1. Edit config.json with your settings"
echo "2. Set up YouTube API credentials (see README)"
echo "3. Run: python main.py"
echo ""
echo "For detailed instructions, see README.md"
