"""
Video Composition with FFmpeg
"""
import subprocess
import logging
import os
from typing import Optional, List, Tuple
import json


class VideoComposer:
    """Composes final video with captions using FFmpeg"""
    
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        """
        Initialize video composer
        
        Args:
            width: Video width in pixels
            height: Video height in pixels
            fps: Frames per second
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.logger = logging.getLogger(__name__)
    
    def add_captions(self, input_video: str, script: str, output_path: str,
                    font: str = "Arial", fontsize: int = 48,
                    fontcolor: str = "white", bg_opacity: float = 0.5) -> bool:
        """
        Add captions/subtitles to video
        
        Args:
            input_video: Path to input video file
            script: Script text to display as captions
            output_path: Path to save output video
            font: Font family for captions
            fontsize: Font size for captions
            fontcolor: Font color for captions
            bg_opacity: Background opacity for caption text (0-1)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Adding captions to {input_video}")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create a temporary subtitle file in ASS format for better styling
            srt_path = output_path.replace('.mp4', '.srt')
            
            # Split script into chunks for better readability
            words = script.split()
            chunks = []
            chunk_size = 8  # words per caption
            
            for i in range(0, len(words), chunk_size):
                chunks.append(' '.join(words[i:i+chunk_size]))
            
            # Create SRT file
            with open(srt_path, 'w') as f:
                # Estimate duration per chunk based on reading speed
                # Average: 2.5 words per second
                words_per_second = 2.5
                
                current_time = 0.0
                for idx, chunk in enumerate(chunks):
                    word_count = len(chunk.split())
                    duration = word_count / words_per_second
                    
                    start = current_time
                    end = current_time + duration
                    
                    f.write(f"{idx + 1}\n")
                    f.write(f"{self._format_time(start)} --> {self._format_time(end)}\n")
                    f.write(f"{chunk}\n\n")
                    
                    current_time = end
            
            # Use ffmpeg to burn in subtitles with styling
            subtitle_filter = (
                f"subtitles={srt_path}:force_style='"
                f"FontName={font},"
                f"FontSize={fontsize},"
                f"PrimaryColour=&H{self._color_to_ass(fontcolor)},"
                f"Alignment=2,"  # Bottom center
                f"MarginV=50,"
                f"BorderStyle=3,"
                f"BackColour=&H{int(bg_opacity * 255):02X}000000,"
                f"Outline=2,"
                f"Shadow=1'"
            )
            
            cmd = [
                'ffmpeg', '-y',
                '-i', input_video,
                '-vf', subtitle_filter,
                '-c:a', 'copy',
                '-c:v', 'libx264',
                '-preset', 'medium',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up SRT file
            if os.path.exists(srt_path):
                os.remove(srt_path)
            
            if result.returncode == 0 and os.path.exists(output_path):
                self.logger.info(f"Successfully added captions to {output_path}")
                return True
            else:
                self.logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error adding captions: {e}")
            return False
    
    def resize_video(self, input_video: str, output_path: str) -> bool:
        """
        Resize and crop video to target dimensions (1080x1920 for Shorts)
        
        Args:
            input_video: Path to input video
            output_path: Path to save resized video
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Resizing video to {self.width}x{self.height}")
            
            # Use ffmpeg to resize and crop to 9:16 aspect ratio
            cmd = [
                'ffmpeg', '-y',
                '-i', input_video,
                '-vf', f'scale={self.width}:{self.height}:force_original_aspect_ratio=increase,crop={self.width}:{self.height}',
                '-c:a', 'copy',
                '-c:v', 'libx264',
                '-preset', 'medium',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                self.logger.info(f"Successfully resized video to {output_path}")
                return True
            else:
                self.logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error resizing video: {e}")
            return False
    
    def compose_final_video(self, avatar_video: str, script: str, 
                          output_path: str) -> bool:
        """
        Compose final video with all elements
        
        Args:
            avatar_video: Path to avatar animation video
            script: Script text for captions
            output_path: Path to save final composed video
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Composing final video")
            
            # First resize the avatar video
            temp_resized = output_path.replace('.mp4', '_resized.mp4')
            if not self.resize_video(avatar_video, temp_resized):
                return False
            
            # Then add captions
            if not self.add_captions(temp_resized, script, output_path):
                return False
            
            # Clean up temporary file
            if os.path.exists(temp_resized):
                os.remove(temp_resized)
            
            self.logger.info(f"Final video composed at {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error composing final video: {e}")
            return False
    
    def _format_time(self, seconds: float) -> str:
        """Format time for SRT file (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _color_to_ass(self, color: str) -> str:
        """Convert color name to ASS format (BGR)"""
        color_map = {
            'white': 'FFFFFF',
            'black': '000000',
            'red': '0000FF',
            'green': '00FF00',
            'blue': 'FF0000',
            'yellow': '00FFFF'
        }
        return color_map.get(color.lower(), 'FFFFFF')
