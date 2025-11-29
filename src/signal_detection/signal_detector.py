"""
Signal Detection Module
Based on SSD (Signal Specification Document) - 40 PESTLE signals
Uses keyword matching, frequency analysis, and source-specific detection
"""

import json
import re
from typing import List, Dict, Optional, Set
from datetime import datetime
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SignalDetector:
    """Detects signals from collected data based on SSD specifications"""
    
    def __init__(self, signals_json_path: str = 'signals_pestel_swot.json'):
        """
        Initialize signal detector
        
        Args:
            signals_json_path: Path to signals JSON file
        """
        self.signals = self._load_signals(signals_json_path)
        self.signal_keywords = self._build_keyword_dictionary()
        self.signal_priorities = self._load_priorities()
        logger.info(f"Initialized SignalDetector with {len(self.signals)} signals")
    
    def _load_signals(self, json_path: str) -> List[Dict]:
        """Load signals from JSON file"""
        try:
            with open(json_path, 'r') as f:
                signals = json.load(f)
            return signals
        except Exception as e:
            logger.error(f"Error loading signals: {str(e)}")
            return []
    
    def _load_priorities(self) -> Dict[str, str]:
        """Load signal priorities from SSD"""
        priorities = {
            # Political (8 signals)
            "Government Policy Announcements": "HIGH",
            "Cabinet/Parliament Decisions": "HIGH",
            "Government Sector Strike Warnings": "HIGH",
            "Police/Security Alerts": "HIGH",
            "Election-related Discussions": "MEDIUM",
            "Foreign Policy / International Agreements": "MEDIUM",
            "Tax Revision Rumors": "HIGH",
            "Public Protests & Demonstrations": "HIGH",
            
            # Economic (8 signals)
            "Inflation Mentions": "HIGH",
            "Fuel Shortage Mentions": "HIGH",
            "Dollar Rate Discussions": "HIGH",
            "Tourism Search Trend (Google Trends)": "HIGH",
            "Food Price Spikes": "MEDIUM",
            "Stock Market Volatility": "MEDIUM",
            "Foreign Investment News": "LOW",
            "Currency Black Market Mentions": "MEDIUM",
            
            # Social (6 signals)
            "Crime & Safety Alerts": "HIGH",
            "Public Sentiment (Social Media)": "HIGH",
            "Migration / Visa Interest": "MEDIUM",
            "Public Health Discussions": "HIGH",
            "Viral Social Trends": "MEDIUM",
            "Cultural Event Mentions": "LOW",
            
            # Technological (5 signals)
            "Power Outages (CEB)": "HIGH",
            "Telecom Outages": "HIGH",
            "Cyberattack Mentions": "MEDIUM",
            "E-commerce Growth Indicators": "LOW",
            "Digital Payments Failure Reports": "HIGH",
            
            # Legal (4 signals)
            "New Regulations Affecting Businesses": "HIGH",
            "Court Rulings Impacting Industries": "MEDIUM",
            "Import/Export Restriction Changes": "HIGH",
            "Customs/Port Delays": "MEDIUM",
            
            # Environmental (9 signals)
            "Rainfall Alerts": "HIGH",
            "Flood Warnings": "HIGH",
            "Heat Wave Alerts": "MEDIUM",
            "Landslide Warnings": "HIGH",
            "Cyclone Updates": "HIGH",
            "Air Quality Index Changes": "MEDIUM",
            "Drought Warnings": "MEDIUM",
            "Water Supply Cuts (NWSDB)": "HIGH",
            "Coastal Erosion / Tsunami Alerts": "LOW"
        }
        return priorities
    
    def _build_keyword_dictionary(self) -> Dict[str, List[str]]:
        """
        Build keyword dictionary for each signal based on SSD specifications
        Returns dictionary mapping signal name to list of keywords
        """
        keywords = {
            # Political Signals
            "Government Policy Announcements": [
                "policy", "tax", "cabinet approves", "budget", "government policy",
                "ministry announces", "policy change", "new policy", "policy decision"
            ],
            "Cabinet/Parliament Decisions": [
                "cabinet decision", "parliament decision", "cabinet meeting",
                "parliament approves", "cabinet approves", "parliament passes",
                "bill passed", "legislation", "cabinet nod"
            ],
            "Government Sector Strike Warnings": [
                "strike", "trade union", "government sector strike", "union warning",
                "work stoppage", "industrial action", "strike threat", "union protest"
            ],
            "Police/Security Alerts": [
                "police alert", "security alert", "police warning", "security threat",
                "police operation", "security operation", "police raid", "security measures"
            ],
            "Election-related Discussions": [
                "election", "voting", "poll", "election campaign", "election date",
                "election results", "by-election", "general election"
            ],
            "Foreign Policy / International Agreements": [
                "foreign policy", "international agreement", "bilateral agreement",
                "trade agreement", "diplomatic", "foreign relations", "international treaty"
            ],
            "Tax Revision Rumors": [
                "tax revision", "tax increase", "tax cut", "tax change", "tax reform",
                "vat change", "income tax", "tax policy", "tax hike"
            ],
            "Public Protests & Demonstrations": [
                "protest", "demonstration", "rally", "march", "protesters",
                "demonstrators", "public protest", "street protest", "sit-in"
            ],
            
            # Economic Signals
            "Inflation Mentions": [
                "inflation", "price increase", "cost of living", "inflation rate",
                "cpi", "consumer price index", "price rise", "inflationary"
            ],
            "Fuel Shortage Mentions": [
                "fuel shortage", "petrol shortage", "diesel shortage", "fuel crisis",
                "fuel queues", "fuel supply", "fuel availability", "fuel stock"
            ],
            "Dollar Rate Discussions": [
                "dollar rate", "usd rate", "exchange rate", "rupee dollar",
                "currency rate", "forex rate", "dollar exchange", "usd lkr"
            ],
            "Tourism Search Trend (Google Trends)": [
                "tourism", "tourist", "visitor", "travel sri lanka", "sri lanka tourism",
                "hotel booking", "tourist arrivals", "tourism sector"
            ],
            "Food Price Spikes": [
                "food price", "rice price", "vegetable price", "price spike",
                "food cost", "grocery price", "food inflation", "price hike"
            ],
            "Stock Market Volatility": [
                "stock market", "cse", "share market", "market volatility",
                "stock exchange", "market crash", "market fall", "share price"
            ],
            "Foreign Investment News": [
                "foreign investment", "fdi", "foreign direct investment",
                "investment opportunity", "foreign investor", "investment deal"
            ],
            "Currency Black Market Mentions": [
                "black market", "underground market", "illegal currency",
                "black market rate", "unofficial exchange"
            ],
            
            # Social Signals
            "Crime & Safety Alerts": [
                "crime", "robbery", "theft", "murder", "assault", "safety alert",
                "crime rate", "criminal activity", "security concern"
            ],
            "Public Sentiment (Social Media)": [
                "public sentiment", "social media", "twitter", "facebook",
                "viral", "trending", "public opinion", "social reaction"
            ],
            "Migration / Visa Interest": [
                "migration", "emigration", "visa", "immigration", "migrate",
                "overseas job", "work visa", "migration trend"
            ],
            "Public Health Discussions": [
                "disease", "outbreak", "epidemic", "health alert", "public health",
                "health crisis", "dengue", "covid", "health emergency"
            ],
            "Viral Social Trends": [
                "viral", "trending", "social media trend", "viral video",
                "trending topic", "social trend", "viral content"
            ],
            "Cultural Event Mentions": [
                "cultural event", "festival", "celebration", "cultural festival",
                "religious festival", "event", "cultural celebration"
            ],
            
            # Technological Signals
            "Power Outages (CEB)": [
                "power outage", "power cut", "electricity cut", "blackout",
                "load shedding", "power failure", "ceb", "electricity board"
            ],
            "Telecom Outages": [
                "telecom outage", "internet outage", "network outage",
                "mobile network", "internet down", "connection issue", "service disruption"
            ],
            "Cyberattack Mentions": [
                "cyberattack", "cyber attack", "hacking", "data breach",
                "cyber security", "cyber threat", "malware", "ransomware"
            ],
            "E-commerce Growth Indicators": [
                "e-commerce", "online shopping", "digital commerce",
                "online retail", "ecommerce growth", "digital sales"
            ],
            "Digital Payments Failure Reports": [
                "payment failure", "digital payment", "payment system down",
                "online payment", "payment issue", "transaction failure"
            ],
            
            # Legal Signals
            "New Regulations Affecting Businesses": [
                "regulation", "new regulation", "business regulation",
                "regulatory change", "compliance", "regulatory framework"
            ],
            "Court Rulings Impacting Industries": [
                "court ruling", "court decision", "legal ruling", "judgment",
                "court order", "supreme court", "high court"
            ],
            "Import/Export Restriction Changes": [
                "import restriction", "export restriction", "import ban",
                "export ban", "trade restriction", "import control"
            ],
            "Customs/Port Delays": [
                "customs delay", "port delay", "customs clearance",
                "port congestion", "shipping delay", "cargo delay"
            ],
            
            # Environmental Signals
            "Rainfall Alerts": [
                "rainfall", "heavy rain", "rain alert", "rainfall warning",
                "monsoon", "rainfall forecast", "heavy rainfall"
            ],
            "Flood Warnings": [
                "flood", "flooding", "flood warning", "flood alert",
                "flash flood", "flood risk", "inundation"
            ],
            "Heat Wave Alerts": [
                "heat wave", "heatwave", "extreme heat", "high temperature",
                "heat alert", "temperature rise", "hot weather"
            ],
            "Landslide Warnings": [
                "landslide", "landslide warning", "mudslide", "slope failure",
                "landslide risk", "earth movement"
            ],
            "Cyclone Updates": [
                "cyclone", "tropical cyclone", "storm", "cyclone warning",
                "cyclone alert", "tropical storm", "severe weather"
            ],
            "Air Quality Index Changes": [
                "air quality", "aqi", "air pollution", "pollution",
                "air quality index", "pollution level", "air quality warning"
            ],
            "Drought Warnings": [
                "drought", "drought warning", "water shortage", "dry spell",
                "drought condition", "water scarcity"
            ],
            "Water Supply Cuts (NWSDB)": [
                "water supply cut", "water cut", "water interruption",
                "nwsdb", "water board", "water supply disruption", "water shortage"
            ],
            "Coastal Erosion / Tsunami Alerts": [
                "tsunami", "tsunami alert", "tsunami warning", "coastal erosion",
                "sea level", "coastal threat", "tsunami risk"
            ]
        }
        return keywords
    
    def detect_signals(self, text: str, title: str = '', source: str = '') -> List[Dict]:
        """
        Detect signals from text content
        
        Args:
            text: Text content to analyze
            title: Article title
            source: Source name (for source-specific detection)
            
        Returns:
            List of detected signals with confidence scores
        """
        if not text and not title:
            return []
        
        # Combine title and text for analysis
        full_text = f"{title} {text}".lower()
        
        detected_signals = []
        
        # Check each signal
        for signal in self.signals:
            signal_name = signal.get('Signal', '')
            keywords = self.signal_keywords.get(signal_name, [])
            
            if not keywords:
                continue
            
            # Count keyword matches
            matches = []
            for keyword in keywords:
                # Use word boundaries for better matching
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, full_text):
                    matches.append(keyword)
            
            # Source-specific detection
            source_match = self._check_source_specific(signal_name, source, full_text)
            
            if matches or source_match:
                # Calculate confidence based on number of matches
                confidence = min(0.5 + (len(matches) * 0.15) + (0.2 if source_match else 0), 1.0)
                
                # Higher confidence for source-specific matches
                if source_match:
                    confidence = min(confidence + 0.2, 1.0)
                
                signal_data = {
                    'signal_name': signal_name,
                    'pestle_category': signal.get('PESTLE', ''),
                    'swot_category': signal.get('SWOT', ''),
                    'confidence': round(confidence, 2),
                    'priority': self.signal_priorities.get(signal_name, 'MEDIUM'),
                    'matched_keywords': matches[:5],  # Top 5 keywords
                    'source_specific_match': source_match,
                    'detected_at': datetime.utcnow().isoformat()
                }
                detected_signals.append(signal_data)
        
        # Sort by confidence (highest first)
        detected_signals.sort(key=lambda x: x['confidence'], reverse=True)
        
        return detected_signals
    
    def _check_source_specific(self, signal_name: str, source: str, text: str) -> bool:
        """
        Check for source-specific signal detection
        Based on SSD: CEB for power outages, NWSDB for water, etc.
        """
        source_lower = source.lower()
        signal_lower = signal_name.lower()
        
        # Power Outages from CEB
        if "power outage" in signal_lower or "ceb" in signal_lower:
            if "ceb" in source_lower or "electricity" in source_lower:
                return True
        
        # Water Supply from NWSDB
        if "water supply" in signal_lower or "nwsdb" in signal_lower:
            if "nwsdb" in source_lower or "water board" in source_lower:
                return True
        
        # Met Department for weather signals
        if any(term in signal_lower for term in ["rainfall", "flood", "cyclone", "heat", "drought", "landslide"]):
            if "met" in source_lower or "meteorological" in source_lower or "weather" in source_lower:
                return True
        
        # Central Bank for economic signals
        if any(term in signal_lower for term in ["inflation", "dollar rate", "currency"]):
            if "central bank" in source_lower or "cbsl" in source_lower:
                return True
        
        # Parliament for policy signals
        if any(term in signal_lower for term in ["policy", "cabinet", "parliament", "regulation"]):
            if "parliament" in source_lower or "cabinet" in source_lower:
                return True
        
        # Google Trends for tourism
        if "tourism" in signal_lower and "google trends" in signal_lower:
            if "google trends" in source_lower:
                return True
        
        return False
    
    def batch_detect(self, articles: List[Dict]) -> List[Dict]:
        """
        Detect signals from multiple articles
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of articles with detected signals
        """
        results = []
        
        for article in articles:
            text = article.get('description', '') or article.get('text', '')
            title = article.get('title', '')
            source = article.get('source', '')
            
            signals = self.detect_signals(text, title, source)
            article['detected_signals'] = signals
            article['signal_count'] = len(signals)
            
            # Add primary signal (highest confidence)
            if signals:
                article['primary_signal'] = signals[0]
            else:
                article['primary_signal'] = None
            
            results.append(article)
        
        logger.info(f"Detected signals in {len(results)} articles")
        return results
    
    def get_signal_statistics(self, articles: List[Dict]) -> Dict:
        """
        Get statistics on detected signals
        
        Args:
            articles: List of articles with detected signals
            
        Returns:
            Statistics dictionary
        """
        signal_counts = Counter()
        pestle_counts = Counter()
        swot_counts = Counter()
        priority_counts = Counter()
        
        for article in articles:
            signals = article.get('detected_signals', [])
            for signal in signals:
                signal_name = signal.get('signal_name', '')
                signal_counts[signal_name] += 1
                pestle_counts[signal.get('pestle_category', '')] += 1
                swot_counts[signal.get('swot_category', '')] += 1
                priority_counts[signal.get('priority', '')] += 1
        
        return {
            'total_articles': len(articles),
            'articles_with_signals': len([a for a in articles if a.get('detected_signals')]),
            'total_signal_detections': sum(signal_counts.values()),
            'top_signals': dict(signal_counts.most_common(10)),
            'pestle_distribution': dict(pestle_counts),
            'swot_distribution': dict(swot_counts),
            'priority_distribution': dict(priority_counts)
        }

