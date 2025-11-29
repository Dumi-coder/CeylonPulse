"""
RSS Feed Scraper
Handles RSS feed parsing and extraction
"""

import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSScraper:
    """Scraper for RSS feeds"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_rss(self, url: str) -> Optional[feedparser.FeedParserDict]:
        """
        Fetch and parse RSS feed
        
        Args:
            url: RSS feed URL
            
        Returns:
            Parsed feed object or None if error
        """
        try:
            logger.info(f"Fetching RSS feed: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            return feed
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {str(e)}")
            return None
    
    def extract_articles(self, feed: feedparser.FeedParserDict) -> List[Dict]:
        """
        Extract articles from parsed RSS feed
        
        Args:
            feed: Parsed feed object
            
        Returns:
            List of article dictionaries
        """
        articles = []
        
        if not feed or not hasattr(feed, 'entries'):
            return articles
        
        for entry in feed.entries:
            article = {
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'description': entry.get('description', ''),
                'published': entry.get('published', ''),
                'published_parsed': entry.get('published_parsed'),
                'source': feed.feed.get('title', 'Unknown'),
                'source_url': feed.feed.get('link', ''),
                'author': entry.get('author', ''),
                'tags': [tag.get('term', '') for tag in entry.get('tags', [])],
                'scraped_at': datetime.utcnow().isoformat()
            }
            articles.append(article)
        
        logger.info(f"Extracted {len(articles)} articles from RSS feed")
        return articles
    
    def scrape(self, url: str) -> List[Dict]:
        """
        Main method to scrape RSS feed
        
        Args:
            url: RSS feed URL
            
        Returns:
            List of article dictionaries
        """
        feed = self.fetch_rss(url)
        if feed:
            return self.extract_articles(feed)
        return []

