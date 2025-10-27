# Quick Start Guide

Get up and running with AI Sports Commentary Generator in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- [x] Python 3.8+ installed
- [x] pip package manager
- [x] Internet connection

## Installation Steps

### 1. Clone the Repository (if not done)
```bash
git clone https://github.com/Buckmast3r/AI-Sports-Commentary-Generator.git
cd AI-Sports-Commentary-Generator
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- Install Python dependencies
- Create config.json
- Create output directories
- Check for required tools

### 3. Install External Tools

#### Install Ollama (Required)
```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the language model
ollama pull llama2

# Start the server
ollama serve
```

#### Install FFmpeg (Required)
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

#### Install Piper TTS (Required)
```bash
# Download Piper (Linux x64)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
tar -xzf piper_amd64.tar.gz
sudo mv piper/piper /usr/local/bin/

# Download a voice model
mkdir -p ~/.local/share/piper/models
cd ~/.local/share/piper/models
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# Test Piper
echo "Hello, this is a test." | piper --model en_US-lessac-medium --output_file test.wav
```

### 4. Configure the Application
```bash
# The setup script already created config.json from the template
# Edit it if needed
nano config.json
```

Key settings to check:
- `rss_feeds`: RSS feed URLs (defaults are fine)
- `ollama.host`: Ollama server URL (default: http://localhost:11434)
- `piper.executable`: Path to piper binary (default: "piper")
- `video.output_dir`: Where to save videos (default: "./output")

### 5. (Optional) Setup YouTube Upload

Only needed if you want to auto-upload to YouTube:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable YouTube Data API v3
4. Create OAuth credentials (Desktop app)
5. Download as `client_secrets.json`
6. Place in project root

## First Run

### Generate Your First Video (No Upload)
```bash
python main.py
```

This will:
1. ✅ Fetch a sports headline
2. ✅ Generate a script (80-110 words)
3. ✅ Create voice narration
4. ✅ Generate video with captions
5. ✅ Save to `output/` directory

Check the output:
```bash
ls -lh output/
# You should see:
# - commentary_TIMESTAMP.mp4
# - script_TIMESTAMP.txt
```

### View the Generated Video
```bash
# Find the latest video
VIDEO=$(ls -t output/commentary_*.mp4 | head -1)

# Play it (Linux)
vlc "$VIDEO"
# or
mpv "$VIDEO"

# macOS
open "$VIDEO"
```

### Generate and Upload to YouTube
```bash
python main.py --upload
```

First time will open browser for authentication.

## Troubleshooting

### "No module named 'ollama'"
```bash
pip install -r requirements.txt
```

### "Ollama connection error"
```bash
# Start Ollama in another terminal
ollama serve

# Or run in background
ollama serve > /dev/null 2>&1 &
```

### "Piper not found"
```bash
# Check if piper is in PATH
which piper

# If not found, update config.json with full path
# "piper_executable": "/usr/local/bin/piper"
```

### "FFmpeg not found"
```bash
# Install FFmpeg
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS

# Verify
ffmpeg -version
```

### Video generation fails
```bash
# Check logs
tail -f commentary_generator.log

# Try with verbose output
python main.py -v  # (if we add verbose flag)
```

## What's Next?

### Customize Your Setup
- ✏️ Edit script generation prompts in `src/llm/script_generator.py`
- 🎨 Add custom avatar image: `python main.py --avatar my_avatar.jpg`
- 📰 Add more RSS feeds in `config.json`

### Automate Daily Posts
```bash
# Create cron job for daily uploads at 9 AM
crontab -e

# Add:
0 9 * * * cd /path/to/AI-Sports-Commentary-Generator && python main.py --upload
```

### Explore Examples
```bash
# See EXAMPLES.md for detailed usage examples
cat EXAMPLES.md
```

## Directory Structure After Setup

```
AI-Sports-Commentary-Generator/
├── main.py                    # ← Run this
├── config.json               # ← Your settings
├── requirements.txt
├── output/                   # ← Generated videos here
│   ├── commentary_*.mp4
│   └── script_*.txt
├── temp/                     # ← Temporary files (auto-cleaned)
├── src/                      # ← Source code
└── commentary_generator.log  # ← Check for errors
```

## Quick Commands Reference

```bash
# Generate video (no upload)
python main.py

# Generate and upload to YouTube
python main.py --upload

# Use custom avatar
python main.py --avatar path/to/image.jpg

# Use custom config
python main.py --config my_config.json

# View logs
tail -f commentary_generator.log

# Run tests
python -m pytest tests/

# Clean up old videos
rm output/commentary_*.mp4
```

## Getting Help

- 📖 Read [README.md](README.md) for full documentation
- 💡 Check [EXAMPLES.md](EXAMPLES.md) for usage examples
- 🐛 Review `commentary_generator.log` for errors
- ❓ Open an issue on GitHub

## Success!

If you can run `python main.py` and see a video in `output/`, you're all set! 🎉

The video should be:
- 1080×1920 pixels (vertical/portrait)
- Include voice narration
- Have on-screen captions
- Be ready for YouTube Shorts

Happy creating! 🏀⚽🏈
