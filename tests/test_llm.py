"""
Unit tests for Script Generator
"""
import pytest
from src.llm.script_generator import ScriptGenerator


def test_script_generator_initialization():
    """Test ScriptGenerator initialization"""
    gen = ScriptGenerator(
        model="llama2",
        host="http://localhost:11434",
        min_words=80,
        max_words=110
    )
    assert gen.model == "llama2"
    assert gen.host == "http://localhost:11434"
    assert gen.min_words == 80
    assert gen.max_words == 110


def test_script_generator_default_values():
    """Test ScriptGenerator with default values"""
    gen = ScriptGenerator()
    assert gen.model == "llama2"
    assert gen.min_words == 80
    assert gen.max_words == 110


# Note: Actual script generation tests would require Ollama to be running
# These are integration tests that should be run separately
