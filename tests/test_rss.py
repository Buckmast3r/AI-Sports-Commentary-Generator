"""
Unit tests for RSS Feed Handler
"""
import pytest
from src.rss.feed_handler import RSSFeedHandler


def test_rss_handler_initialization():
    """Test RSS handler can be initialized"""
    feeds = ["https://www.espn.com/espn/rss/news"]
    handler = RSSFeedHandler(feeds)
    assert handler.feed_urls == feeds


def test_fetch_headlines_returns_list():
    """Test that fetch_headlines returns a list"""
    handler = RSSFeedHandler(["https://www.espn.com/espn/rss/news"])
    headlines = handler.fetch_headlines(limit=1)
    assert isinstance(headlines, list)


def test_fetch_headlines_with_limit():
    """Test that limit parameter is respected"""
    handler = RSSFeedHandler(["https://www.espn.com/espn/rss/news"])
    headlines = handler.fetch_headlines(limit=3)
    # Should return at most 3 headlines
    assert len(headlines) <= 3


def test_headline_structure():
    """Test that headlines have expected structure"""
    handler = RSSFeedHandler(["https://www.espn.com/espn/rss/news"])
    headlines = handler.fetch_headlines(limit=1)
    
    if headlines:
        headline = headlines[0]
        assert 'title' in headline
        assert 'link' in headline
        assert 'summary' in headline
        assert isinstance(headline['title'], str)


def test_invalid_feed_url():
    """Test handling of invalid feed URL"""
    handler = RSSFeedHandler(["https://invalid-url-that-does-not-exist.com/rss"])
    headlines = handler.fetch_headlines(limit=1)
    # Should return empty list for invalid feeds
    assert isinstance(headlines, list)


def test_get_random_headline():
    """Test getting a random headline"""
    handler = RSSFeedHandler(["https://www.espn.com/espn/rss/news"])
    headline = handler.get_random_headline()
    
    # May return None if no headlines available
    if headline:
        assert isinstance(headline, dict)
        assert 'title' in headline
