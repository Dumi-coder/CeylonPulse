#!/usr/bin/env python3
"""
Data Collection Runner Script
Run this script to collect data from all sources
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.data_collector import DataCollector

def main():
    """Main function to run data collection"""
    
    # Configuration
    use_llm = os.getenv('USE_LLM', 'true').lower() == 'true'
    llm_provider = 'mistral'  # Using Mistral 7B (free)
    db_type = os.getenv('DB_TYPE', 'json')  # 'postgres', 'mongodb', or 'json'
    db_connection = os.getenv('DB_CONNECTION_STRING', None)
    
    # Check for Hugging Face token
    hf_token = os.getenv('HUGGINGFACE_API_TOKEN', '')
    if hf_token:
        print(f"✅ Hugging Face token found (for better API access)")
    else:
        print("⚠️ No Hugging Face token - using public API (may have rate limits)")
    
    print("=" * 60)
    print("CeylonPulse Data Collector")
    print("=" * 60)
    print(f"LLM Extraction: {'Enabled' if use_llm else 'Disabled'}")
    print(f"LLM Provider: {llm_provider}")
    print(f"Database Type: {db_type}")
    print("=" * 60)
    print()
    
    # Initialize collector
    collector = DataCollector(
        use_llm=use_llm,
        llm_provider=llm_provider,
        db_type=db_type,
        db_connection=db_connection
    )
    
    try:
        # Collect data using all three methods
        summary = collector.collect_all(
            use_scraping=True,      # Method 1: Scrape
            use_api=True,           # Method 2: Use API responses
            use_llm_extraction=use_llm  # Method 3: LLM extraction
        )
        
        print("\n" + "=" * 60)
        print("Collection Summary")
        print("=" * 60)
        print(f"Raw Data Collected: {summary['raw_data_count']}")
        print(f"Processed Data: {summary['processed_data_count']}")
        print(f"Signals Extracted: {summary['signals_extracted']}")
        print("\nSources:")
        for source, count in summary['sources'].items():
            print(f"  - {source}: {count}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during collection: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        collector.close()

if __name__ == '__main__':
    main()

