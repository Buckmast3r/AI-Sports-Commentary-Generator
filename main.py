#!/usr/bin/env python3
"""
AI Sports Commentary Generator
Main orchestration script that coordinates all components
"""
import os
import sys
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rss import RSSFeedHandler
from llm import ScriptGenerator
from tts import VoiceGenerator
from avatar import AvatarAnimator
from video import VideoComposer
from youtube import YouTubeUploader


class SportsCommentaryGenerator:
    """Main class orchestrating the sports commentary generation pipeline"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the generator with configuration
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config = self._load_config(config_path)
        self.setup_logging()
        
        # Initialize components
        self.rss_handler = RSSFeedHandler(self.config['rss_feeds'])
        self.script_gen = ScriptGenerator(
            model=self.config['ollama']['model'],
            host=self.config['ollama']['host'],
            min_words=self.config['script']['min_words'],
            max_words=self.config['script']['max_words']
        )
        self.voice_gen = VoiceGenerator(
            piper_executable=self.config['piper']['executable'],
            model=self.config['piper']['model']
        )
        self.avatar_animator = AvatarAnimator(
            checkpoint_dir=self.config['sadtalker']['checkpoint_dir'],
            config_path=self.config['sadtalker']['config_path']
        )
        self.video_composer = VideoComposer(
            width=self.config['video']['width'],
            height=self.config['video']['height'],
            fps=self.config['video']['fps']
        )
        self.youtube_uploader = YouTubeUploader(
            client_secrets_file=self.config['youtube']['client_secrets_file']
        )
        
        # Create output directories
        self.output_dir = Path(self.config['video']['output_dir'])
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("./temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        if not os.path.exists(config_path):
            # Try example config
            example_config = "config.example.json"
            if os.path.exists(example_config):
                print(f"Config not found at {config_path}, using {example_config}")
                print(f"Please copy {example_config} to {config_path} and customize it")
                config_path = example_config
            else:
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('commentary_generator.log'),
                logging.StreamHandler()
            ]
        )
    
    def generate_commentary(self, avatar_image: str = None, 
                          upload: bool = False) -> str:
        """
        Generate a complete sports commentary video
        
        Args:
            avatar_image: Path to avatar image (optional, uses default if None)
            upload: Whether to upload to YouTube after generation
            
        Returns:
            Path to generated video file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Step 1: Fetch sports headline
            self.logger.info("Step 1: Fetching sports headline from RSS feeds")
            headline_data = self.rss_handler.get_random_headline()
            
            if not headline_data:
                raise Exception("Failed to fetch sports headline")
            
            headline = headline_data['title']
            summary = headline_data.get('summary', '')
            self.logger.info(f"Headline: {headline}")
            
            # Step 2: Generate script with LLM
            self.logger.info("Step 2: Generating script with Ollama LLM")
            script = self.script_gen.generate_script(headline, summary)
            
            if not script:
                raise Exception("Failed to generate script")
            
            self.logger.info(f"Generated script ({len(script.split())} words):\n{script}")
            
            # Save script for reference
            script_path = self.output_dir / f"script_{timestamp}.txt"
            with open(script_path, 'w') as f:
                f.write(f"Headline: {headline}\n\n")
                f.write(f"Script:\n{script}\n")
            
            # Step 3: Generate voice with Piper TTS
            self.logger.info("Step 3: Generating voice with Piper TTS")
            audio_path = self.temp_dir / f"audio_{timestamp}.wav"
            
            if not self.voice_gen.generate_speech(script, str(audio_path)):
                raise Exception("Failed to generate voice audio")
            
            # Step 4: Animate avatar with SadTalker (or use static fallback)
            self.logger.info("Step 4: Animating avatar")
            
            # Use default avatar if none provided
            if avatar_image is None:
                # Create a simple default avatar placeholder
                avatar_image = self._create_default_avatar()
            
            avatar_video_path = self.temp_dir / f"avatar_{timestamp}.mp4"
            
            # Try SadTalker first, fallback to static video
            success = self.avatar_animator.animate_avatar(
                avatar_image, str(audio_path), str(avatar_video_path)
            )
            
            if not success:
                self.logger.warning("SadTalker failed, using static avatar fallback")
                success = self.avatar_animator.create_static_avatar_video(
                    avatar_image, str(audio_path), str(avatar_video_path)
                )
                
                if not success:
                    raise Exception("Failed to create avatar video")
            
            # Step 5: Compose final video with captions
            self.logger.info("Step 5: Composing final video with captions")
            final_video_path = self.output_dir / f"commentary_{timestamp}.mp4"
            
            if not self.video_composer.compose_final_video(
                str(avatar_video_path), script, str(final_video_path)
            ):
                raise Exception("Failed to compose final video")
            
            self.logger.info(f"Video generated successfully: {final_video_path}")
            
            # Step 6: Upload to YouTube (optional)
            if upload:
                self.logger.info("Step 6: Uploading to YouTube Shorts")
                
                title = self.config['youtube']['title_template'].format(
                    headline=headline[:80]  # Limit headline length
                )
                description = self.config['youtube']['description']
                
                video_id = self.youtube_uploader.upload_video(
                    str(final_video_path),
                    title=title,
                    description=f"{description}\n\nHeadline: {headline}",
                    category=self.config['youtube']['category'],
                    privacy_status=self.config['youtube']['privacy_status']
                )
                
                if video_id:
                    self.logger.info(f"Successfully uploaded to YouTube! Video ID: {video_id}")
                else:
                    self.logger.warning("YouTube upload failed")
            
            # Cleanup temp files
            self._cleanup_temp_files(audio_path, avatar_video_path)
            
            return str(final_video_path)
            
        except Exception as e:
            self.logger.error(f"Error generating commentary: {e}")
            raise
    
    def _create_default_avatar(self) -> str:
        """Create a simple default avatar image"""
        from PIL import Image, ImageDraw, ImageFont
        
        avatar_path = self.temp_dir / "default_avatar.png"
        
        if avatar_path.exists():
            return str(avatar_path)
        
        # Create a simple avatar with PIL
        img = Image.new('RGB', (512, 512), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple face
        # Circle for head
        draw.ellipse([100, 80, 412, 392], fill='#eee8d5', outline='#586e75', width=3)
        
        # Eyes
        draw.ellipse([180, 180, 220, 220], fill='#073642')
        draw.ellipse([292, 180, 332, 220], fill='#073642')
        
        # Smile
        draw.arc([150, 200, 362, 380], start=0, end=180, fill='#586e75', width=5)
        
        img.save(avatar_path)
        self.logger.info(f"Created default avatar at {avatar_path}")
        
        return str(avatar_path)
    
    def _cleanup_temp_files(self, *files):
        """Clean up temporary files"""
        for file in files:
            if file and os.path.exists(file):
                try:
                    os.remove(file)
                    self.logger.info(f"Cleaned up: {file}")
                except Exception as e:
                    self.logger.warning(f"Failed to cleanup {file}: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Sports Commentary Generator for YouTube Shorts'
    )
    parser.add_argument(
        '--config', 
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--avatar',
        help='Path to custom avatar image'
    )
    parser.add_argument(
        '--upload',
        action='store_true',
        help='Upload to YouTube after generation'
    )
    parser.add_argument(
        '--no-upload',
        action='store_true',
        help='Skip YouTube upload (default)'
    )
    
    args = parser.parse_args()
    
    # Create generator
    generator = SportsCommentaryGenerator(config_path=args.config)
    
    # Generate commentary
    upload = args.upload and not args.no_upload
    video_path = generator.generate_commentary(
        avatar_image=args.avatar,
        upload=upload
    )
    
    print(f"\n{'='*60}")
    print(f"Video generated successfully!")
    print(f"Output: {video_path}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
