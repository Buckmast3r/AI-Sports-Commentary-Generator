"""
RSS Feed Handler for fetching sports headlines
"""
import feedparser
import logging
from typing import List, Dict, Optional


class RSSFeedHandler:
    """Handles fetching and parsing sports headlines from RSS feeds"""
    
    def __init__(self, feed_urls: List[str]):
        """
        Initialize RSS feed handler
        
        Args:
            feed_urls: List of RSS feed URLs to fetch from
        """
        self.feed_urls = feed_urls
        self.logger = logging.getLogger(__name__)
    
    def fetch_headlines(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        Fetch latest sports headlines from configured RSS feeds
        
        Args:
            limit: Maximum number of headlines to fetch
            
        Returns:
            List of headline dictionaries with 'title', 'link', 'summary'
        """
        headlines = []
        
        for feed_url in self.feed_urls:
            try:
                self.logger.info(f"Fetching from {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:limit]:
                    headline = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'summary': entry.get('summary', entry.get('description', ''))
                    }
                    headlines.append(headline)
                    
            except Exception as e:
                self.logger.error(f"Error fetching from {feed_url}: {e}")
                continue
        
        return headlines[:limit]
    
    def get_random_headline(self) -> Optional[Dict[str, str]]:
        """
        Get a single random headline from available feeds
        
        Returns:
            Dictionary with headline data or None if no headlines available
        """
        import random
        
        headlines = self.fetch_headlines(limit=5)
        if headlines:
            return random.choice(headlines)
        return None
