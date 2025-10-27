"""
Unit tests for YouTube Uploader
"""
import pytest
from src.youtube.uploader import YouTubeUploader


def test_youtube_uploader_initialization():
    """Test YouTubeUploader initialization"""
    uploader = YouTubeUploader(
        client_secrets_file="client_secrets.json",
        token_file="token.pickle"
    )
    assert uploader.client_secrets_file == "client_secrets.json"
    assert uploader.token_file == "token.pickle"
    assert uploader.youtube is None  # Not authenticated yet


def test_youtube_uploader_default_values():
    """Test YouTubeUploader with default values"""
    uploader = YouTubeUploader()
    assert uploader.client_secrets_file == "client_secrets.json"
    assert uploader.token_file == "token.pickle"


# Note: Actual upload tests would require valid OAuth credentials
# These are integration tests that should be run separately
