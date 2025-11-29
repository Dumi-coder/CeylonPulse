"""
Main Data Collection Orchestrator
Coordinates scraping, API calls, and LLM extraction
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.sources import SCRAPING_SOURCES, API_SOURCES
from src.scrapers.rss_scraper import RSSScraper
from src.scrapers.web_scraper import WebScraper
from src.api.twitter_api import TwitterAPI
from src.api.google_trends_api import GoogleTrendsAPI
from src.llm_extraction.llm_extractor import LLMExtractor
from src.database.storage import DataStorage
from src.signal_detection.signal_detector import SignalDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCollector:
    """Main orchestrator for data collection"""
    
    def __init__(self, 
                 use_llm: bool = True,
                 llm_provider: str = 'openai',
                 db_type: str = 'json',
                 db_connection: Optional[str] = None):
        """
        Initialize data collector
        
        Args:
            use_llm: Whether to use LLM for extraction
            llm_provider: LLM provider ('openai' or 'anthropic')
            db_type: Database type ('postgres', 'mongodb', or 'json')
            db_connection: Database connection string
        """
        # Initialize components
        self.rss_scraper = RSSScraper()
        self.web_scraper = WebScraper()
        self.twitter_api = TwitterAPI()
        self.google_trends_api = GoogleTrendsAPI()
        self.llm_extractor = LLMExtractor(provider='mistral', use_api=True) if use_llm else None
        self.signal_detector = SignalDetector()  # Keyword-based signal detection
        self.storage = DataStorage(db_type=db_type, connection_string=db_connection)
        
        logger.info("Data Collector initialized")
    
    def collect_rss_feeds(self) -> List[Dict]:
        """Collect data from RSS feeds"""
        all_articles = []
        
        # Ada Derana RSS
        ada_rss = SCRAPING_SOURCES['ada_derana'].get('rss_feed')
        if ada_rss:
            articles = self.rss_scraper.scrape(ada_rss)
            all_articles.extend(articles)
        
        # EconomyNext RSS
        econ_rss = SCRAPING_SOURCES['economynext'].get('rss_feed')
        if econ_rss:
            articles = self.rss_scraper.scrape(econ_rss)
            all_articles.extend(articles)
        
        logger.info(f"Collected {len(all_articles)} articles from RSS feeds")
        return all_articles
    
    def collect_web_scraping(self) -> List[Dict]:
        """Collect data via web scraping"""
        all_articles = []
        
        # Ada Derana
        ada_urls = SCRAPING_SOURCES['ada_derana']
        for key, url in ada_urls.items():
            if key != 'rss_feed':
                articles = self.web_scraper.scrape_ada_derana(url)
                all_articles.extend(articles)
        
        # EconomyNext
        econ_urls = SCRAPING_SOURCES['economynext']
        for key, url in econ_urls.items():
            if key != 'rss_feed':
                articles = self.web_scraper.scrape_economynext(url)
                all_articles.extend(articles)
        
        # Met Department
        met_urls = SCRAPING_SOURCES['met_department']
        for key, url in met_urls.items():
            articles = self.web_scraper.scrape_met_department(url)
            all_articles.extend(articles)
        
        # Central Bank
        cbsl_urls = SCRAPING_SOURCES['central_bank']
        for key, url in cbsl_urls.items():
            articles = self.web_scraper.scrape_central_bank(url)
            all_articles.extend(articles)
        
        # Parliament
        parl_urls = SCRAPING_SOURCES['parliament']
        for key, url in parl_urls.items():
            articles = self.web_scraper.scrape_parliament(url)
            all_articles.extend(articles)
        
        # CEB
        ceb_urls = SCRAPING_SOURCES['ceb']
        for key, url in ceb_urls.items():
            if key not in ['facebook', 'twitter']:
                articles = self.web_scraper.scrape_ceb(url)
                all_articles.extend(articles)
        
        # NWSDB
        nwsdb_urls = SCRAPING_SOURCES['nwsdb']
        for key, url in nwsdb_urls.items():
            articles = self.web_scraper.scrape_nwsdb(url)
            all_articles.extend(articles)
        
        logger.info(f"Collected {len(all_articles)} articles via web scraping")
        return all_articles
    
    def collect_api_data(self) -> List[Dict]:
        """Collect data via API calls"""
        all_data = []
        
        # Twitter
        twitter_sources = API_SOURCES['twitter']
        accounts = twitter_sources.get('key_accounts', [])
        for account_url in accounts:
            username = account_url.split('/')[-1]
            tweets = self.twitter_api.get_account_tweets(username, max_results=10)
            all_data.extend(tweets)
        
        # Google Trends
        trends = self.google_trends_api.get_trending_searches(geo='LK')
        all_data.extend(trends)
        
        # Get interest for Sri Lanka keywords
        sri_lanka_keywords = ['Sri Lanka', 'Colombo', 'inflation', 'fuel', 'tourism']
        interest_data = self.google_trends_api.get_interest_over_time(
            keywords=sri_lanka_keywords[:3],  # Limit to 3 to avoid rate limits
            geo='LK',
            timeframe='today 3-m'
        )
        all_data.extend(interest_data)
        
        logger.info(f"Collected {len(all_data)} items via API")
        return all_data
    
    def collect_all(self, use_scraping: bool = True, 
                   use_api: bool = True,
                   use_llm_extraction: bool = True) -> Dict:
        """
        Collect data from all sources
        
        Args:
            use_scraping: Whether to use web scraping
            use_api: Whether to use API calls
            use_llm_extraction: Whether to use LLM for extraction
            
        Returns:
            Dictionary with collected data summary
        """
        logger.info("Starting data collection...")
        
        all_raw_data = []
        
        # Method 1: Scraping
        if use_scraping:
            logger.info("Method 1: Scraping data...")
            rss_articles = self.collect_rss_feeds()
            web_articles = self.collect_web_scraping()
            all_raw_data.extend(rss_articles)
            all_raw_data.extend(web_articles)
        
        # Method 2: API responses
        if use_api:
            logger.info("Method 2: Collecting data via APIs...")
            api_data = self.collect_api_data()
            all_raw_data.extend(api_data)
        
        # Save raw data
        if all_raw_data:
            self.storage.save_raw_data(all_raw_data)
            logger.info(f"Saved {len(all_raw_data)} raw data items")
        
        # Method 3: LLM extraction to structure data + generate signals
        processed_data = []
        
        # First, use keyword-based signal detection (always available)
        logger.info("Detecting signals using keyword matching (SSD-based)...")
        articles_with_signals = self.signal_detector.batch_detect(all_raw_data)
        
        # Then optionally use LLM for additional extraction and structuring
        if use_llm_extraction and self.llm_extractor:
            logger.info("Method 3: Using LLM to extract additional signals and structure data...")
            processed_data = self.llm_extractor.batch_extract(articles_with_signals, use_llm=True)
            
            # Merge LLM-extracted signals with keyword-detected signals
            for article in processed_data:
                keyword_signals = article.get('detected_signals', [])
                llm_signals = article.get('extracted_signals', [])
                
                # Combine signals (avoid duplicates)
                all_signals = keyword_signals.copy()
                for llm_signal in llm_signals:
                    # Check if signal already exists
                    signal_name = llm_signal.get('signal_name', '')
                    if not any(s.get('signal_name') == signal_name for s in all_signals):
                        all_signals.append({
                            'signal_name': signal_name,
                            'pestle_category': llm_signal.get('pestle_category', ''),
                            'swot_category': llm_signal.get('swot_category', ''),
                            'confidence': llm_signal.get('confidence', 0.0),
                            'detection_method': 'llm',
                            'matched_keywords': llm_signal.get('key_phrases', [])
                        })
                
                article['detected_signals'] = all_signals
                article['signal_count'] = len(all_signals)
        else:
            processed_data = articles_with_signals
        
        if processed_data:
            self.storage.save_processed_data(processed_data)
            logger.info(f"Saved {len(processed_data)} processed data items")
        
        # Get signal statistics
        signal_stats = self.signal_detector.get_signal_statistics(processed_data)
        
        summary = {
            'collection_timestamp': datetime.utcnow().isoformat(),
            'raw_data_count': len(all_raw_data),
            'processed_data_count': len(processed_data),
            'sources': {
                'rss_feeds': len([a for a in all_raw_data if 'rss' in a.get('source', '').lower()]),
                'web_scraping': len([a for a in all_raw_data if a.get('source') in ['Ada Derana', 'EconomyNext', 'Meteorological Department', 'Central Bank of Sri Lanka', 'Parliament of Sri Lanka', 'Ceylon Electricity Board', 'National Water Supply and Drainage Board']]),
                'api': len([a for a in all_raw_data if a.get('source') in ['Twitter', 'Google Trends']])
            },
            'signals_extracted': sum(len(a.get('detected_signals', [])) for a in processed_data),
            'signal_statistics': signal_stats
        }
        
        logger.info(f"Data collection complete. Summary: {summary}")
        return summary
    
    def close(self):
        """Close all connections"""
        self.storage.close()
        logger.info("Data collector closed")


if __name__ == '__main__':
    # Example usage
    collector = DataCollector(
        use_llm=True,
        llm_provider='openai',
        db_type='json'
    )
    
    try:
        summary = collector.collect_all(
            use_scraping=True,
            use_api=True,
            use_llm_extraction=True
        )
        print(f"\nCollection Summary:\n{summary}")
    finally:
        collector.close()

