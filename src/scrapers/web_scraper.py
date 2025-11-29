"""
Web Scraper for HTML pages
Handles scraping of news websites and government portals
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Scraper for HTML web pages"""
    
    def __init__(self, timeout: int = 30, delay: float = 1.0):
        self.timeout = timeout
        self.delay = delay  # Delay between requests to be respectful
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse HTML page
        
        Args:
            url: Web page URL
            
        Returns:
            BeautifulSoup object or None if error
        """
        try:
            logger.info(f"Fetching web page: {url}")
            time.sleep(self.delay)  # Be respectful to servers
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e:
            logger.error(f"Error fetching web page {url}: {str(e)}")
            return None
    
    def scrape_ada_derana(self, url: str) -> List[Dict]:
        """Scrape Ada Derana news page"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # Ada Derana specific selectors (may need adjustment based on actual HTML structure)
        news_items = soup.find_all('div', class_='news-item') or soup.find_all('article')
        
        for item in news_items:
            title_elem = item.find('h2') or item.find('h3') or item.find('a')
            link_elem = item.find('a')
            
            if title_elem and link_elem:
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': link_elem.get('href', ''),
                    'description': '',
                    'source': 'Ada Derana',
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                
                desc_elem = item.find('p') or item.find('div', class_='description')
                if desc_elem:
                    article['description'] = desc_elem.get_text(strip=True)
                
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} articles from Ada Derana")
        return articles
    
    def scrape_economynext(self, url: str) -> List[Dict]:
        """Scrape EconomyNext news page"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # EconomyNext specific selectors
        news_items = soup.find_all('article') or soup.find_all('div', class_='post')
        
        for item in news_items:
            title_elem = item.find('h2') or item.find('h3') or item.find('a', class_='title')
            link_elem = item.find('a')
            
            if title_elem and link_elem:
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': link_elem.get('href', ''),
                    'description': '',
                    'source': 'EconomyNext',
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                
                desc_elem = item.find('p') or item.find('div', class_='excerpt')
                if desc_elem:
                    article['description'] = desc_elem.get_text(strip=True)
                
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} articles from EconomyNext")
        return articles
    
    def scrape_met_department(self, url: str) -> List[Dict]:
        """Scrape Meteorological Department warnings and forecasts"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # Met Department specific selectors
        content = soup.find('div', class_='content') or soup.find('main') or soup
        
        warnings = content.find_all(['div', 'article', 'section'], class_=lambda x: x and ('warning' in x.lower() or 'alert' in x.lower() or 'forecast' in x.lower()))
        
        for warning in warnings:
            title_elem = warning.find('h2') or warning.find('h3') or warning.find('strong')
            
            if title_elem:
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': url,
                    'description': warning.get_text(strip=True)[:500],
                    'source': 'Meteorological Department',
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} items from Met Department")
        return articles
    
    def scrape_central_bank(self, url: str) -> List[Dict]:
        """Scrape Central Bank news and publications"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # Central Bank specific selectors
        news_items = soup.find_all('div', class_='news-item') or soup.find_all('article') or soup.find_all('li')
        
        for item in news_items:
            title_elem = item.find('a') or item.find('h3') or item.find('h4')
            
            if title_elem:
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                if link and not link.startswith('http'):
                    link = f"https://www.cbsl.gov.lk{link}"
                
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': link or url,
                    'description': item.get_text(strip=True)[:300],
                    'source': 'Central Bank of Sri Lanka',
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} items from Central Bank")
        return articles
    
    def scrape_parliament(self, url: str) -> List[Dict]:
        """Scrape Parliament news and decisions"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # Parliament specific selectors
        news_items = soup.find_all('div', class_='news-item') or soup.find_all('article') or soup.find_all('li')
        
        for item in news_items:
            title_elem = item.find('a') or item.find('h3')
            
            if title_elem:
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                if link and not link.startswith('http'):
                    link = f"https://www.parliament.lk{link}"
                
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': link or url,
                    'description': item.get_text(strip=True)[:300],
                    'source': 'Parliament of Sri Lanka',
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} items from Parliament")
        return articles
    
    def scrape_ceb(self, url: str) -> List[Dict]:
        """Scrape CEB outage notices and load shedding"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # CEB specific selectors
        notices = soup.find_all('div', class_='notice') or soup.find_all('article') or soup.find_all('div', class_='outage')
        
        for notice in notices:
            title_elem = notice.find('h2') or notice.find('h3') or notice.find('strong')
            
            if title_elem:
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': url,
                    'description': notice.get_text(strip=True)[:500],
                    'source': 'Ceylon Electricity Board',
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} items from CEB")
        return articles
    
    def scrape_nwsdb(self, url: str) -> List[Dict]:
        """Scrape NWSDB announcements and water interruptions"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # NWSDB specific selectors
        announcements = soup.find_all('div', class_='announcement') or soup.find_all('article') or soup.find_all('tr')
        
        for ann in announcements:
            title_elem = ann.find('td') or ann.find('h3') or ann.find('strong')
            
            if title_elem:
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': url,
                    'description': ann.get_text(strip=True)[:300],
                    'source': 'National Water Supply and Drainage Board',
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} items from NWSDB")
        return articles
    
    def scrape_generic(self, url: str, source_name: str = "Unknown") -> List[Dict]:
        """Generic scraper for any website"""
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        articles = []
        # Try common article patterns
        news_items = (soup.find_all('article') or 
                     soup.find_all('div', class_=lambda x: x and ('article' in x.lower() or 'news' in x.lower())) or
                     soup.find_all('li'))
        
        for item in news_items[:20]:  # Limit to 20 items
            title_elem = item.find('a') or item.find('h2') or item.find('h3')
            
            if title_elem:
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                if link and not link.startswith('http'):
                    # Try to construct absolute URL
                    base_url = '/'.join(url.split('/')[:3])
                    link = f"{base_url}{link}"
                
                article = {
                    'title': title_elem.get_text(strip=True),
                    'link': link or url,
                    'description': item.get_text(strip=True)[:300],
                    'source': source_name,
                    'source_url': url,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} items from {source_name}")
        return articles

