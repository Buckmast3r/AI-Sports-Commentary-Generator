# AI Sports Commentary Generator

An automated pipeline for creating AI-generated sports commentary videos for YouTube Shorts. This tool pulls fresh sports headlines, generates engaging scripts, creates voice narration, animates an AI avatar, and produces ready-to-upload vertical videos with captions.

## Features

- 📰 **RSS Sports Headlines**: Automatically fetches the latest sports news from configurable RSS feeds
- 🤖 **AI Script Generation**: Uses Ollama (local LLM) to generate punchy 80-110 word commentary scripts
- 🎙️ **Voice Synthesis**: Converts scripts to natural speech using Piper TTS
- 👤 **Avatar Animation**: Animates AI avatars with SadTalker (or uses static fallback)
- 🎬 **Video Composition**: Creates 1080×1920 vertical videos with FFmpeg and on-screen captions
- 📤 **YouTube Upload**: Automatically uploads to YouTube Shorts via OAuth

## Architecture

```
┌─────────────┐
│ RSS Feeds   │ → Fetch Sports Headlines
└──────┬──────┘
       ↓
┌─────────────┐
│ Ollama LLM  │ → Generate 80-110 Word Script
└──────┬──────┘
       ↓
┌─────────────┐
│ Piper TTS   │ → Convert to Voice Audio
└──────┬──────┘
       ↓
┌─────────────┐
│ SadTalker   │ → Animate Avatar
└──────┬──────┘
       ↓
┌─────────────┐
│ FFmpeg      │ → Compose Video + Captions
└──────┬──────┘
       ↓
┌─────────────┐
│ YouTube API │ → Upload as Short
└─────────────┘
```

## Prerequisites

### Required Software

1. **Python 3.8+**
2. **Ollama** - Local LLM server
   - Install from: https://ollama.ai/
   - Pull a model: `ollama pull llama2`
3. **Piper TTS** - Fast neural text-to-speech
   - Install from: https://github.com/rhasspy/piper
4. **FFmpeg** - Video processing
   - Install: `sudo apt install ffmpeg` (Linux) or `brew install ffmpeg` (Mac)
5. **SadTalker** (Optional) - Avatar animation
   - Install from: https://github.com/OpenTalker/SadTalker
   - If not available, the system uses a static image fallback

### Python Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Buckmast3r/AI-Sports-Commentary-Generator.git
cd AI-Sports-Commentary-Generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure the Application

Copy the example configuration:
```bash
cp config.example.json config.json
```

Edit `config.json` to customize:
- RSS feed URLs
- Ollama model and host
- Piper TTS settings
- Video dimensions and output directory
- YouTube API settings

### 4. Setup YouTube API (for uploads)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file as `client_secrets.json`
6. Place it in the project root directory

On first upload, you'll be prompted to authenticate via browser.

### 5. Setup Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a language model
ollama pull llama2

# Start Ollama server (if not running)
ollama serve
```

### 6. Setup Piper TTS

```bash
# Download Piper
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
tar -xzf piper_amd64.tar.gz

# Download a voice model
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# Update config.json with path to piper executable
```

## Usage

### Basic Usage

Generate a sports commentary video:
```bash
python main.py
```

### Advanced Options

```bash
# Use custom configuration file
python main.py --config my_config.json

# Use custom avatar image
python main.py --avatar path/to/avatar.jpg

# Generate and upload to YouTube
python main.py --upload

# Generate without uploading (default)
python main.py --no-upload
```

### Command Line Options

- `--config PATH`: Path to configuration file (default: config.json)
- `--avatar PATH`: Path to custom avatar image
- `--upload`: Upload to YouTube after generation
- `--no-upload`: Skip YouTube upload (default)

## Output

The generator creates:
- **Video**: `output/commentary_TIMESTAMP.mp4` (1080×1920, vertical format)
- **Script**: `output/script_TIMESTAMP.txt` (saved for reference)
- **Logs**: `commentary_generator.log`

## Configuration Options

### RSS Feeds
```json
"rss_feeds": [
  "https://www.espn.com/espn/rss/news",
  "https://sports.yahoo.com/rss/"
]
```

### Ollama Settings
```json
"ollama": {
  "model": "llama2",
  "host": "http://localhost:11434"
}
```

### Script Generation
```json
"script": {
  "min_words": 80,
  "max_words": 110
}
```

### Video Settings
```json
"video": {
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "output_dir": "./output"
}
```

### YouTube Settings
```json
"youtube": {
  "title_template": "Sports Commentary - {headline}",
  "category": "17",
  "privacy_status": "public"
}
```

## Project Structure

```
AI-Sports-Commentary-Generator/
├── main.py                 # Main orchestration script
├── requirements.txt        # Python dependencies
├── config.example.json     # Example configuration
├── config.json            # Your configuration (gitignored)
├── src/
│   ├── rss/              # RSS feed handling
│   ├── llm/              # Script generation with LLM
│   ├── tts/              # Text-to-speech with Piper
│   ├── avatar/           # Avatar animation
│   ├── video/            # Video composition
│   └── youtube/          # YouTube upload
├── output/               # Generated videos
└── temp/                 # Temporary files
```

## Troubleshooting

### Ollama Connection Error
```bash
# Ensure Ollama is running
ollama serve

# Test with
ollama run llama2
```

### Piper TTS Not Found
- Verify piper executable path in config.json
- Check that voice model files are downloaded
- Test with: `echo "test" | piper --model en_US-lessac-medium --output_file test.wav`

### YouTube Upload Fails
- Ensure `client_secrets.json` is in project root
- Check that YouTube Data API v3 is enabled
- Verify OAuth consent screen is configured
- Delete `token.pickle` and re-authenticate if needed

### FFmpeg Not Found
```bash
# Install FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

## Future Enhancements

- [ ] Instagram Reels integration
- [ ] TikTok Business API integration
- [ ] Multiple avatar options
- [ ] Custom background music
- [ ] Batch processing of multiple headlines
- [ ] Scheduling and automation
- [ ] Analytics tracking

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM infrastructure
- [Piper](https://github.com/rhasspy/piper) - Fast neural TTS
- [SadTalker](https://github.com/OpenTalker/SadTalker) - Avatar animation
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [Google YouTube API](https://developers.google.com/youtube) - Video uploads

## Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review logs in `commentary_generator.log`