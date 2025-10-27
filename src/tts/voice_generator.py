"""
Piper TTS Integration for voice generation
"""
import subprocess
import logging
import os
from typing import Optional


class VoiceGenerator:
    """Generates voice audio from text using Piper TTS"""
    
    def __init__(self, piper_executable: str = "piper", model: str = "en_US-lessac-medium"):
        """
        Initialize voice generator with Piper TTS
        
        Args:
            piper_executable: Path to piper executable
            model: Piper voice model to use
        """
        self.piper_executable = piper_executable
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    def generate_speech(self, text: str, output_path: str) -> bool:
        """
        Generate speech audio from text
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the output WAV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Generating speech to {output_path}")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Run piper TTS
            # Note: Piper reads from stdin and outputs to stdout
            process = subprocess.Popen(
                [self.piper_executable, '--model', self.model, '--output_file', output_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode == 0 and os.path.exists(output_path):
                self.logger.info(f"Successfully generated speech at {output_path}")
                return True
            else:
                self.logger.error(f"Piper TTS failed: {stderr}")
                return False
                
        except FileNotFoundError:
            self.logger.error(f"Piper executable not found: {self.piper_executable}")
            self.logger.info("Please install Piper TTS: https://github.com/rhasspy/piper")
            return False
        except Exception as e:
            self.logger.error(f"Error generating speech: {e}")
            return False
    
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """
        Get duration of audio file in seconds
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds or None if unable to determine
        """
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', audio_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return float(result.stdout.strip())
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting audio duration: {e}")
            return None
