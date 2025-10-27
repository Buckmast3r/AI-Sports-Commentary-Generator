"""
Ollama LLM Integration for script generation
"""
import logging
import ollama
from typing import Optional


class ScriptGenerator:
    """Generates sports commentary scripts using Ollama LLM"""
    
    def __init__(self, model: str = "llama2", host: str = "http://localhost:11434", 
                 min_words: int = 80, max_words: int = 110):
        """
        Initialize script generator with Ollama
        
        Args:
            model: Ollama model name to use
            host: Ollama server host URL
            min_words: Minimum words in generated script
            max_words: Maximum words in generated script
        """
        self.model = model
        self.host = host
        self.min_words = min_words
        self.max_words = max_words
        self.logger = logging.getLogger(__name__)
        
        # Configure ollama client
        self.client = ollama.Client(host=host)
    
    def generate_script(self, headline: str, summary: str = "") -> Optional[str]:
        """
        Generate a punchy sports commentary script from headline
        
        Args:
            headline: Sports headline to base the script on
            summary: Optional summary/description for more context
            
        Returns:
            Generated script text or None if generation fails
        """
        prompt = f"""You are a professional sports commentator creating exciting short-form content for YouTube Shorts.

Based on this sports headline: "{headline}"
{f'Context: {summary}' if summary else ''}

Create a punchy, energetic sports commentary script that:
- Is exactly {self.min_words}-{self.max_words} words long
- Has an exciting, engaging tone suitable for short-form video
- Opens with a strong hook
- Delivers key facts and commentary
- Ends with a compelling statement
- Uses natural, conversational language perfect for voice narration

Write ONLY the script, no additional commentary or labels."""

        try:
            self.logger.info(f"Generating script for: {headline}")
            response = self.client.generate(
                model=self.model,
                prompt=prompt
            )
            
            script = response['response'].strip()
            
            # Validate word count
            word_count = len(script.split())
            self.logger.info(f"Generated script with {word_count} words")
            
            if word_count < self.min_words * 0.8 or word_count > self.max_words * 1.2:
                self.logger.warning(f"Script length {word_count} outside target range")
            
            return script
            
        except Exception as e:
            self.logger.error(f"Error generating script: {e}")
            return None
