"""
Unit tests for Voice Generator
"""
import pytest
from src.tts.voice_generator import VoiceGenerator


def test_voice_generator_initialization():
    """Test VoiceGenerator initialization"""
    gen = VoiceGenerator(
        piper_executable="piper",
        model="en_US-lessac-medium"
    )
    assert gen.piper_executable == "piper"
    assert gen.model == "en_US-lessac-medium"


def test_voice_generator_default_values():
    """Test VoiceGenerator with default values"""
    gen = VoiceGenerator()
    assert gen.piper_executable == "piper"
    assert gen.model == "en_US-lessac-medium"


# Note: Actual TTS tests would require Piper to be installed
# These are integration tests that should be run separately
