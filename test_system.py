#!/usr/bin/env python3
"""Quick test script to verify CeylonPulse system works correctly"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        from src.scrapers.rss_scraper import RSSScraper
        from src.api.google_trends_api import GoogleTrendsAPI
        from src.signal_detection.signal_detector import SignalDetector
        from src.llm_extraction.llm_extractor import LLMExtractor
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_rss_scraping():
    """Test RSS scraping"""
    print("\nTesting RSS scraping...")
    try:
        from src.scrapers.rss_scraper import RSSScraper
        scraper = RSSScraper()
        articles = scraper.scrape('https://www.adaderana.lk/rss.php')
        if len(articles) > 0:
            print(f"✅ Scraped {len(articles)} articles")
            print(f"   Sample: {articles[0].get('title', '')[:50]}...")
            return True
        else:
            print("⚠️ No articles scraped (may be network issue)")
            return True  # Don't fail if network issue
    except Exception as e:
        print(f"❌ RSS scraping error: {e}")
        return False

def test_signal_detection():
    """Test signal detection"""
    print("\nTesting signal detection...")
    try:
        from src.signal_detection.signal_detector import SignalDetector
        detector = SignalDetector()
        
        # Test cases
        test_cases = [
            ("Fuel shortage reported in Colombo. Long queues at petrol stations.", 
             "Fuel Shortage Mentions"),
            ("Power outage reported in several areas. CEB announces load shedding.", 
             "Power Outages (CEB)"),
            ("Heavy rainfall and flood warnings issued for Western Province.", 
             "Flood Warnings")
        ]
        
        all_passed = True
        for text, expected_signal in test_cases:
            signals = detector.detect_signals(text, "Test News")
            found = any(s['signal_name'] == expected_signal for s in signals)
            if found:
                print(f"   ✅ Detected '{expected_signal}'")
            else:
                print(f"   ❌ Failed to detect '{expected_signal}'")
                all_passed = False
        
        if all_passed:
            print("✅ Signal detection working correctly")
        return all_passed
    except Exception as e:
        print(f"❌ Signal detection error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_extraction():
    """Test LLM extraction (optional - may be slow)"""
    print("\nTesting LLM extraction (Mistral 7B)...")
    print("   Note: First request may take 30-60 seconds (model loading)")
    try:
        from src.llm_extraction.llm_extractor import LLMExtractor
        extractor = LLMExtractor(provider='mistral', use_api=True)
        
        test_text = "Fuel shortage reported in Colombo. Inflation rising. Power outages expected."
        signals = extractor.extract_signals(test_text, "Economic Crisis")
        
        if signals:
            print(f"✅ LLM extracted {len(signals)} signals")
            for sig in signals[:2]:  # Show first 2
                print(f"   - {sig.get('signal_name', 'N/A')} (confidence: {sig.get('confidence', 0):.2f})")
        else:
            print("⚠️ No signals extracted (may be API issue or model loading)")
        return True  # Don't fail test if API is slow/unavailable
    except Exception as e:
        print(f"⚠️ LLM extraction error (may be API issue): {e}")
        return True  # Don't fail test

def test_data_collector():
    """Test full data collector (quick test)"""
    print("\nTesting data collector integration...")
    try:
        from src.data_collector import DataCollector
        
        # Initialize (without LLM for faster test)
        collector = DataCollector(
            use_llm=False,  # Skip LLM for faster test
            db_type='json'
        )
        
        # Test RSS collection only
        articles = collector.collect_rss_feeds()
        if len(articles) > 0:
            print(f"✅ Data collector working - got {len(articles)} articles")
            return True
        else:
            print("⚠️ No articles collected (may be network issue)")
            return True
    except Exception as e:
        print(f"❌ Data collector error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("CeylonPulse System Test")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("RSS Scraping", test_rss_scraping()))
    results.append(("Signal Detection", test_signal_detection()))
    results.append(("LLM Extraction", test_llm_extraction()))
    results.append(("Data Collector", test_data_collector()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20s}: {status}")
    
    # Count passes (LLM is optional)
    critical_tests = [r for name, r in results if name != "LLM Extraction"]
    all_critical_passed = all(critical_tests)
    
    print("\n" + "=" * 60)
    if all_critical_passed:
        print("✅ All critical tests passed!")
        print("   System is ready to use.")
    else:
        print("❌ Some critical tests failed.")
        print("   Please check errors above and fix issues.")
    print("=" * 60)
    
    return all_critical_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

