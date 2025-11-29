"""
Database Storage Module
Handles storage of raw and processed data
Supports both PostgreSQL and MongoDB
"""

import os
import json
from typing import List, Dict, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import database libraries
try:
    import psycopg2
    from psycopg2.extras import execute_batch
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    logger.warning("PostgreSQL libraries not available. Install with: pip install psycopg2-binary")

try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("MongoDB libraries not available. Install with: pip install pymongo")


class DataStorage:
    """Database storage handler"""
    
    def __init__(self, db_type: str = 'json', connection_string: Optional[str] = None):
        """
        Initialize data storage
        
        Args:
            db_type: 'postgres', 'mongodb', or 'json' (file-based)
            connection_string: Database connection string
        """
        self.db_type = db_type
        self.connection_string = connection_string
        self.connection = None
        
        if db_type == 'postgres' and POSTGRES_AVAILABLE:
            self._init_postgres()
        elif db_type == 'mongodb' and MONGODB_AVAILABLE:
            self._init_mongodb()
        elif db_type == 'json':
            self.data_dir = 'data/raw'
            os.makedirs(self.data_dir, exist_ok=True)
            logger.info("Using JSON file-based storage")
        else:
            logger.warning(f"Database type {db_type} not available, falling back to JSON")
            self.db_type = 'json'
            self.data_dir = 'data/raw'
            os.makedirs(self.data_dir, exist_ok=True)
    
    def _init_postgres(self):
        """Initialize PostgreSQL connection"""
        try:
            if self.connection_string:
                self.connection = psycopg2.connect(self.connection_string)
            else:
                # Try environment variables
                self.connection = psycopg2.connect(
                    host=os.getenv('POSTGRES_HOST', 'localhost'),
                    port=os.getenv('POSTGRES_PORT', '5432'),
                    database=os.getenv('POSTGRES_DB', 'ceylonpulse'),
                    user=os.getenv('POSTGRES_USER', 'postgres'),
                    password=os.getenv('POSTGRES_PASSWORD', '')
                )
            self._create_tables()
            logger.info("PostgreSQL connection established")
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {str(e)}")
            self.db_type = 'json'
            self.data_dir = 'data/raw'
            os.makedirs(self.data_dir, exist_ok=True)
    
    def _init_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            if self.connection_string:
                client = MongoClient(self.connection_string)
            else:
                client = MongoClient(
                    host=os.getenv('MONGODB_HOST', 'localhost'),
                    port=int(os.getenv('MONGODB_PORT', '27017'))
                )
            self.db = client[os.getenv('MONGODB_DB', 'ceylonpulse')]
            self.connection = client
            logger.info("MongoDB connection established")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            self.db_type = 'json'
            self.data_dir = 'data/raw'
            os.makedirs(self.data_dir, exist_ok=True)
    
    def _create_tables(self):
        """Create PostgreSQL tables if they don't exist"""
        if not self.connection:
            return
        
        cursor = self.connection.cursor()
        
        # Raw articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_articles (
                id SERIAL PRIMARY KEY,
                title TEXT,
                link TEXT,
                description TEXT,
                source TEXT,
                source_url TEXT,
                published_at TIMESTAMP,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_data JSONB
            )
        """)
        
        # Processed articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_articles (
                id SERIAL PRIMARY KEY,
                raw_article_id INTEGER REFERENCES raw_articles(id),
                structured_data JSONB,
                extracted_signals JSONB,
                pestle_category TEXT,
                swot_category TEXT,
                severity_score FLOAT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id SERIAL PRIMARY KEY,
                signal_name TEXT,
                article_id INTEGER REFERENCES raw_articles(id),
                confidence FLOAT,
                severity_estimate FLOAT,
                pestle_category TEXT,
                swot_category TEXT,
                key_phrases TEXT[],
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON raw_articles(source)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_scraped_at ON raw_articles(scraped_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_signal_name ON signals(signal_name)")
        
        self.connection.commit()
        cursor.close()
    
    def save_raw_data(self, articles: List[Dict]) -> bool:
        """
        Save raw articles to database
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            True if successful
        """
        if not articles:
            return False
        
        try:
            if self.db_type == 'postgres' and self.connection:
                cursor = self.connection.cursor()
                insert_query = """
                    INSERT INTO raw_articles (title, link, description, source, source_url, published_at, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                data = []
                for article in articles:
                    # Parse published date if available
                    published_at = None
                    if article.get('published'):
                        try:
                            from dateutil import parser
                            published_at = parser.parse(article['published'])
                        except:
                            pass
                    
                    data.append((
                        article.get('title', ''),
                        article.get('link', ''),
                        article.get('description', ''),
                        article.get('source', ''),
                        article.get('source_url', ''),
                        published_at,
                        json.dumps(article)
                    ))
                
                execute_batch(cursor, insert_query, data)
                self.connection.commit()
                cursor.close()
                logger.info(f"Saved {len(articles)} articles to PostgreSQL")
                return True
            
            elif self.db_type == 'mongodb' and self.connection:
                collection = self.db['raw_articles']
                # Add timestamps
                for article in articles:
                    article['stored_at'] = datetime.utcnow()
                collection.insert_many(articles)
                logger.info(f"Saved {len(articles)} articles to MongoDB")
                return True
            
            else:  # JSON file storage
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                filename = f"{self.data_dir}/articles_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(articles, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved {len(articles)} articles to {filename}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving raw data: {str(e)}")
            return False
    
    def save_processed_data(self, processed_articles: List[Dict]) -> bool:
        """
        Save processed articles with signals
        
        Args:
            processed_articles: List of processed article dictionaries
            
        Returns:
            True if successful
        """
        if not processed_articles:
            return False
        
        try:
            if self.db_type == 'postgres' and self.connection:
                cursor = self.connection.cursor()
                
                # Insert processed articles
                processed_query = """
                    INSERT INTO processed_articles (raw_article_id, structured_data, extracted_signals, 
                                                    pestle_category, swot_category, severity_score)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                # Insert signals
                signal_query = """
                    INSERT INTO signals (signal_name, article_id, confidence, severity_estimate,
                                       pestle_category, swot_category, key_phrases)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                for article in processed_articles:
                    signals = article.get('extracted_signals', [])
                    structured = article.get('structured_data', {})
                    
                    # Get primary signal for categorization
                    primary_signal = signals[0] if signals else {}
                    
                    # Insert processed article (assuming raw_article_id exists)
                    cursor.execute(processed_query, (
                        article.get('id'),  # This should be the raw article ID
                        json.dumps(structured),
                        json.dumps(signals),
                        primary_signal.get('pestle_category', ''),
                        primary_signal.get('swot_category', ''),
                        primary_signal.get('severity_estimate', 0.0)
                    ))
                    
                    # Insert individual signals
                    for signal in signals:
                        cursor.execute(signal_query, (
                            signal.get('signal_name', ''),
                            article.get('id'),
                            signal.get('confidence', 0.0),
                            signal.get('severity_estimate', 0.0),
                            signal.get('pestle_category', ''),
                            signal.get('swot_category', ''),
                            signal.get('key_phrases', [])
                        ))
                
                self.connection.commit()
                cursor.close()
                logger.info(f"Saved {len(processed_articles)} processed articles to PostgreSQL")
                return True
            
            elif self.db_type == 'mongodb' and self.connection:
                collection = self.db['processed_articles']
                for article in processed_articles:
                    article['stored_at'] = datetime.utcnow()
                collection.insert_many(processed_articles)
                logger.info(f"Saved {len(processed_articles)} processed articles to MongoDB")
                return True
            
            else:  # JSON file storage
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                filename = f"data/processed/processed_{timestamp}.json"
                os.makedirs('data/processed', exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(processed_articles, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved {len(processed_articles)} processed articles to {filename}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            if self.db_type == 'postgres':
                self.connection.close()
            elif self.db_type == 'mongodb':
                self.connection.close()
            logger.info("Database connection closed")

