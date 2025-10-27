"""
Unit tests for Video Composer
"""
import pytest
import os
from src.video.composer import VideoComposer


def test_video_composer_initialization():
    """Test VideoComposer initialization"""
    composer = VideoComposer(width=1080, height=1920, fps=30)
    assert composer.width == 1080
    assert composer.height == 1920
    assert composer.fps == 30


def test_video_composer_default_values():
    """Test VideoComposer with default values"""
    composer = VideoComposer()
    assert composer.width == 1080  # Default for Shorts
    assert composer.height == 1920
    assert composer.fps == 30


def test_format_time():
    """Test SRT time formatting"""
    composer = VideoComposer()
    
    # Test various time values
    assert composer._format_time(0) == "00:00:00,000"
    assert composer._format_time(1.5) == "00:00:01,500"
    assert composer._format_time(61.250) == "00:01:01,250"
    # Note: floating point precision may cause slight variations
    result = composer._format_time(3661.999)
    assert result.startswith("01:01:01,99")  # Accept 998 or 999 due to float precision


def test_color_to_ass():
    """Test color conversion to ASS format"""
    composer = VideoComposer()
    
    assert composer._color_to_ass('white') == 'FFFFFF'
    assert composer._color_to_ass('black') == '000000'
    assert composer._color_to_ass('red') == '0000FF'
    assert composer._color_to_ass('unknown') == 'FFFFFF'  # Default to white


def test_resize_video_nonexistent_file():
    """Test resize with nonexistent input file"""
    composer = VideoComposer()
    result = composer.resize_video(
        '/nonexistent/video.mp4',
        '/tmp/output.mp4'
    )
    assert result == False


def test_add_captions_nonexistent_file():
    """Test add_captions with nonexistent input file"""
    composer = VideoComposer()
    result = composer.add_captions(
        '/nonexistent/video.mp4',
        'Test script here',
        '/tmp/output.mp4'
    )
    assert result == False
