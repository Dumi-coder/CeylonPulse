"""
Twitter API Handler
Handles Twitter API v2 requests for data collection
"""

import requests
import os
from typing import List, Dict, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterAPI:
    """Handler for Twitter API v2"""
    
    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize Twitter API handler
        
        Args:
            bearer_token: Twitter Bearer Token (or set TWITTER_BEARER_TOKEN env var)
        """
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')
        self.base_url = 'https://api.twitter.com/2/'
        self.session = requests.Session()
        
        if self.bearer_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.bearer_token}'
            })
        else:
            logger.warning("Twitter Bearer Token not provided. API calls will fail.")
    
    def get_user_id(self, username: str) -> Optional[str]:
        """
        Get user ID from username
        
        Args:
            username: Twitter username (without @)
            
        Returns:
            User ID or None
        """
        if not self.bearer_token:
            return None
        
        try:
            url = f"{self.base_url}users/by/username/{username}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('id')
        except Exception as e:
            logger.error(f"Error getting user ID for {username}: {str(e)}")
            return None
    
    def get_user_tweets(self, user_id: str, max_results: int = 10) -> List[Dict]:
        """
        Get recent tweets from a user
        
        Args:
            user_id: Twitter user ID
            max_results: Maximum number of tweets to retrieve (max 100)
            
        Returns:
            List of tweet dictionaries
        """
        if not self.bearer_token:
            logger.warning("Twitter Bearer Token not available")
            return []
        
        try:
            url = f"{self.base_url}users/{user_id}/tweets"
            params = {
                'max_results': min(max_results, 100),
                'tweet.fields': 'created_at,public_metrics,text,author_id',
                'expansions': 'author_id'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            tweets = []
            for tweet in data.get('data', []):
                tweet_data = {
                    'id': tweet.get('id'),
                    'text': tweet.get('text', ''),
                    'created_at': tweet.get('created_at', ''),
                    'author_id': tweet.get('author_id'),
                    'retweet_count': tweet.get('public_metrics', {}).get('retweet_count', 0),
                    'like_count': tweet.get('public_metrics', {}).get('like_count', 0),
                    'reply_count': tweet.get('public_metrics', {}).get('reply_count', 0),
                    'source': 'Twitter',
                    'scraped_at': datetime.utcnow().isoformat()
                }
                tweets.append(tweet_data)
            
            logger.info(f"Retrieved {len(tweets)} tweets from user {user_id}")
            return tweets
        except Exception as e:
            logger.error(f"Error getting tweets for user {user_id}: {str(e)}")
            return []
    
    def search_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for tweets
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of tweet dictionaries
        """
        if not self.bearer_token:
            logger.warning("Twitter Bearer Token not available")
            return []
        
        try:
            url = f"{self.base_url}tweets/search/recent"
            params = {
                'query': query,
                'max_results': min(max_results, 100),
                'tweet.fields': 'created_at,public_metrics,text,author_id'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            tweets = []
            for tweet in data.get('data', []):
                tweet_data = {
                    'id': tweet.get('id'),
                    'text': tweet.get('text', ''),
                    'created_at': tweet.get('created_at', ''),
                    'author_id': tweet.get('author_id'),
                    'retweet_count': tweet.get('public_metrics', {}).get('retweet_count', 0),
                    'like_count': tweet.get('public_metrics', {}).get('like_count', 0),
                    'source': 'Twitter',
                    'scraped_at': datetime.utcnow().isoformat()
                }
                tweets.append(tweet_data)
            
            logger.info(f"Retrieved {len(tweets)} tweets for query: {query}")
            return tweets
        except Exception as e:
            logger.error(f"Error searching tweets: {str(e)}")
            return []
    
    def get_account_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """
        Get tweets from a specific account by username
        
        Args:
            username: Twitter username (without @)
            max_results: Maximum number of tweets
            
        Returns:
            List of tweet dictionaries
        """
        user_id = self.get_user_id(username)
        if user_id:
            return self.get_user_tweets(user_id, max_results)
        return []

