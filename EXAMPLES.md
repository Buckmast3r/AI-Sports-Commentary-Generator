# Example Usage Guide

This guide provides step-by-step examples for using the AI Sports Commentary Generator.

## Quick Start Example

The simplest way to generate a sports commentary video:

```bash
# 1. Make sure Ollama is running
ollama serve &

# 2. Run the generator
python main.py
```

This will:
1. Fetch a random sports headline from RSS feeds
2. Generate a 80-110 word script
3. Create voice narration
4. Generate a video with captions
5. Save it to `output/commentary_TIMESTAMP.mp4`

## Example with Custom Avatar

```bash
# Use your own avatar image
python main.py --avatar /path/to/my_avatar.jpg
```

The avatar image should be:
- At least 512x512 pixels
- Clear headshot/portrait
- JPG or PNG format

## Example with YouTube Upload

```bash
# Generate and automatically upload to YouTube Shorts
python main.py --upload
```

First-time upload will require browser authentication.

## Example with Custom Configuration

Create a custom config file:

```bash
cp config.example.json my_config.json
# Edit my_config.json with your preferences
python main.py --config my_config.json
```

## Workflow Example

Here's a complete workflow for daily content creation:

```bash
#!/bin/bash
# daily_commentary.sh - Generate daily sports commentary

# 1. Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    ollama serve &
    sleep 5
fi

# 2. Generate commentary
python main.py --upload

# 3. Check output
ls -lh output/
```

## Testing Individual Components

### Test RSS Feed Fetching
```python
from src.rss import RSSFeedHandler

handler = RSSFeedHandler([
    "https://www.espn.com/espn/rss/news"
])
headlines = handler.fetch_headlines(limit=5)
for h in headlines:
    print(h['title'])
```

### Test Script Generation
```python
from src.llm import ScriptGenerator

generator = ScriptGenerator(model="llama2")
script = generator.generate_script(
    headline="Lakers Win Championship in Overtime Thriller",
    summary="The Lakers defeated the Celtics 112-109..."
)
print(script)
```

### Test Voice Generation
```python
from src.tts import VoiceGenerator

voice_gen = VoiceGenerator()
success = voice_gen.generate_speech(
    text="Welcome to sports commentary!",
    output_path="./temp/test_audio.wav"
)
print(f"Success: {success}")
```

## Batch Processing Example

Generate multiple videos from different headlines:

```python
#!/usr/bin/env python3
from main import SportsCommentaryGenerator

generator = SportsCommentaryGenerator()

# Generate 5 videos
for i in range(5):
    try:
        video_path = generator.generate_commentary(upload=False)
        print(f"Generated: {video_path}")
    except Exception as e:
        print(f"Error on video {i}: {e}")
```

## Scheduled Automation Example

Using cron to generate daily at 9 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 9 * * * cd /path/to/AI-Sports-Commentary-Generator && python main.py --upload >> cron.log 2>&1
```

## Customizing Script Style

Edit the prompt in `src/llm/script_generator.py` to change the commentary style:

```python
# For more energetic style:
prompt = f"""Create a HIGH-ENERGY, EXPLOSIVE sports commentary...

# For analytical style:
prompt = f"""Create a professional, analytical sports commentary...

# For humorous style:
prompt = f"""Create a fun, slightly humorous sports commentary...
```

## Output Examples

Generated files structure:
```
output/
├── commentary_20251027_092415.mp4  # Final video (1080x1920)
├── commentary_20251027_093122.mp4
├── script_20251027_092415.txt      # Saved scripts
└── script_20251027_093122.txt

temp/  # (cleaned up automatically)
├── audio_20251027_092415.wav
└── avatar_20251027_092415.mp4
```

## Troubleshooting Examples

### If Ollama connection fails:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running:
ollama serve

# Test with a prompt
ollama run llama2 "Say hello"
```

### If Piper TTS fails:
```bash
# Test Piper directly
echo "Test speech" | piper \
  --model en_US-lessac-medium \
  --output_file test.wav

# Check if model files exist
ls -lh *.onnx*
```

### If YouTube upload fails:
```bash
# Delete old token and re-authenticate
rm token.pickle
python main.py --upload
```

## Advanced: Custom RSS Feeds

Add your favorite sports news sources:

```json
{
  "rss_feeds": [
    "https://www.espn.com/espn/rss/news",
    "https://sports.yahoo.com/rss/",
    "https://www.cbssports.com/rss/headlines",
    "https://www.si.com/rss/si_topstories.rss",
    "https://bleacherreport.com/articles/feed"
  ]
}
```

## Advanced: Multiple Language Support

Change Piper model for different languages:

```json
{
  "piper": {
    "model": "de_DE-thorsten-medium"  // German
    "model": "es_ES-davefx-medium"    // Spanish
    "model": "fr_FR-siwis-medium"     // French
  }
}
```

## Performance Optimization

For faster generation:

1. **Use smaller LLM**: Switch to `ollama pull llama2:7b-chat` or `tinyllama`
2. **Reduce video quality**: Lower fps in config.json (30 → 24)
3. **Skip SadTalker**: Use static avatar fallback (automatic)
4. **Batch processing**: Generate multiple videos in one session

## Integration Examples

### Slack Notification
```python
import requests

def notify_slack(video_url):
    webhook_url = "YOUR_SLACK_WEBHOOK"
    requests.post(webhook_url, json={
        "text": f"New sports commentary uploaded: {video_url}"
    })
```

### Discord Webhook
```python
import requests

def notify_discord(video_path):
    webhook_url = "YOUR_DISCORD_WEBHOOK"
    with open(video_path, 'rb') as f:
        requests.post(webhook_url, files={'file': f})
```

## Production Deployment

For production use:

1. **Use Docker** (create Dockerfile)
2. **Set up monitoring** (track generation success rate)
3. **Implement retry logic** (for failed API calls)
4. **Add error notifications** (email/Slack on failures)
5. **Schedule with proper logging** (centralized logs)

## Tips and Best Practices

- **Test during off-peak hours** for faster RSS fetching
- **Monitor YouTube quotas** (10,000 units per day)
- **Keep scripts between 80-110 words** for optimal Shorts length
- **Use high-quality avatar images** (512x512 minimum)
- **Review generated scripts** before uploading
- **Start with manual uploads** before automating
- **Respect API rate limits** for all services
