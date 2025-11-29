"""
Google Trends API Handler
Handles Google Trends data collection
Note: Google Trends doesn't have an official public API, 
so this uses pytrends library or web scraping as fallback
"""

import os
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False
    logger.warning("pytrends not available. Install with: pip install pytrends")


class GoogleTrendsAPI:
    """Handler for Google Trends data"""
    
    def __init__(self, hl: str = 'en-US', tz: int = 360):
        """
        Initialize Google Trends handler
        
        Args:
            hl: Host language (default: en-US)
            tz: Timezone offset (default: 360 for UTC+6, Sri Lanka)
        """
        self.hl = hl
        self.tz = tz
        self.pytrends = None
        
        if PYTRENDS_AVAILABLE:
            try:
                self.pytrends = TrendReq(hl=hl, tz=tz)
            except Exception as e:
                logger.error(f"Error initializing pytrends: {str(e)}")
        else:
            logger.warning("pytrends not available. Google Trends functionality limited.")
    
    def get_trending_searches(self, geo: str = 'LK') -> List[Dict]:
        """
        Get trending searches for a country
        
        Args:
            geo: Country code (LK for Sri Lanka)
            
        Returns:
            List of trending search dictionaries
        """
        if not self.pytrends:
            logger.warning("pytrends not available")
            return []
        
        try:
            trending = self.pytrends.trending_searches(pn=geo.lower())
            
            trends = []
            for idx, trend in enumerate(trending[0].head(20).values):
                trend_data = {
                    'rank': idx + 1,
                    'keyword': trend[0] if isinstance(trend, list) else str(trend),
                    'geo': geo,
                    'source': 'Google Trends',
                    'scraped_at': datetime.utcnow().isoformat()
                }
                trends.append(trend_data)
            
            logger.info(f"Retrieved {len(trends)} trending searches for {geo}")
            return trends
        except Exception as e:
            logger.error(f"Error getting trending searches: {str(e)}")
            return []
    
    def get_interest_over_time(self, keywords: List[str], geo: str = 'LK', 
                               timeframe: str = 'today 3-m') -> List[Dict]:
        """
        Get interest over time for keywords
        
        Args:
            keywords: List of keywords to search
            geo: Country code
            timeframe: Time range (e.g., 'today 3-m', 'today 12-m')
            
        Returns:
            List of interest data points
        """
        if not self.pytrends:
            logger.warning("pytrends not available")
            return []
        
        try:
            self.pytrends.build_payload(keywords, geo=geo, timeframe=timeframe)
            interest_data = self.pytrends.interest_over_time()
            
            trends = []
            for date, row in interest_data.iterrows():
                for keyword in keywords:
                    trend_data = {
                        'date': date.isoformat(),
                        'keyword': keyword,
                        'interest': int(row[keyword]) if keyword in row else 0,
                        'geo': geo,
                        'source': 'Google Trends',
                        'scraped_at': datetime.utcnow().isoformat()
                    }
                    trends.append(trend_data)
            
            logger.info(f"Retrieved interest data for {len(keywords)} keywords")
            return trends
        except Exception as e:
            logger.error(f"Error getting interest over time: {str(e)}")
            return []
    
    def get_related_queries(self, keywords: List[str], geo: str = 'LK') -> List[Dict]:
        """
        Get related queries for keywords
        
        Args:
            keywords: List of keywords
            geo: Country code
            
        Returns:
            List of related query dictionaries
        """
        if not self.pytrends:
            logger.warning("pytrends not available")
            return []
        
        try:
            self.pytrends.build_payload(keywords, geo=geo)
            related = self.pytrends.related_queries()
            
            related_queries = []
            for keyword in keywords:
                if keyword in related and related[keyword]['top'] is not None:
                    for idx, row in related[keyword]['top'].head(10).iterrows():
                        query_data = {
                            'keyword': keyword,
                            'related_query': row['query'],
                            'value': int(row['value']),
                            'geo': geo,
                            'source': 'Google Trends',
                            'scraped_at': datetime.utcnow().isoformat()
                        }
                        related_queries.append(query_data)
            
            logger.info(f"Retrieved related queries for {len(keywords)} keywords")
            return related_queries
        except Exception as e:
            logger.error(f"Error getting related queries: {str(e)}")
            return []

