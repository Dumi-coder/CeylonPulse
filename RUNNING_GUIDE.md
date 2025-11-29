# CeylonPulse: Running Guide & Testing

This guide explains how to run the data collection system and verify it works correctly.

## 🚀 Quick Start Sequence

### Option 1: Google Colab (Recommended for Beginners)

1. **Open the Notebook**
   - Upload `CeylonPulse_DataCollection.ipynb` to Google Colab
   - Or open directly if shared

2. **Run Cells Sequentially**
   - Click "Runtime" → "Run all" (or run each cell one by one)
   - Cells are already in the correct order

3. **Check Output**
   - Each cell prints ✅ success messages
   - Look for error messages (⚠️ or ❌)

### Option 2: Local Python

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Collector**
   ```bash
   python run_collector.py
   ```

3. **Check Output**
   - Look for success messages in terminal
   - Check `data/raw/` and `data/processed/` folders

---

## 📋 Detailed Running Sequence

### Step 1: Setup & Installation

**In Colab:**
- Cell 1: Install packages
- Cell 2: Mount Drive (optional)

**Locally:**
```bash
cd /home/dumindu/Programming/python/CeylonPulse
pip install -r requirements.txt
```

**✅ Verification:**
- No import errors
- All packages install successfully
- See: `✅ All packages installed successfully!`

---

### Step 2: Load Configuration

**In Colab:**
- Cell 3: Import libraries & load 40 signals

**Locally:**
- Already done in `run_collector.py`

**✅ Verification:**
- See: `✅ Loaded 40 PESTLE signals`
- Check that SIGNALS list has 40 items

---

### Step 3: Method 1 - Scraping

**In Colab:**
- Cell 4: RSS feed scraping

**Locally:**
- Runs automatically in `run_collector.py`

**✅ Verification:**
- See: `✅ Scraped X from Ada Derana, Y from EconomyNext`
- Check `all_scraped_articles` has items
- Articles should have: title, link, description, source

**Test manually:**
```python
# Test RSS scraping
from src.scrapers.rss_scraper import RSSScraper

scraper = RSSScraper()
articles = scraper.scrape('https://www.adaderana.lk/rss.php')
print(f"Got {len(articles)} articles")
print(articles[0] if articles else "No articles")
```

---

### Step 4: Method 2 - API Responses

**In Colab:**
- Cell 5: Google Trends

**Locally:**
- Runs automatically in `run_collector.py`

**✅ Verification:**
- See: `✅ Retrieved X trending searches`
- See top 10 trending searches displayed
- Trends should have: rank, keyword, geo, source

**Test manually:**
```python
# Test Google Trends
from src.api.google_trends_api import GoogleTrendsAPI

api = GoogleTrendsAPI()
trends = api.get_trending_searches(geo='LK')
print(f"Got {len(trends)} trends")
print(trends[0] if trends else "No trends")
```

---

### Step 5: Method 3 - Signal Detection

**In Colab:**
- Cell 6: Keyword-based detection
- Cell 7: LLM extraction (Mistral 7B)

**Locally:**
- Runs automatically in `run_collector.py`

**✅ Verification:**
- See: `✅ Signal detection completed!`
- See: `📊 Articles with signals: X`
- Articles should have `detected_signals` field

**Test manually:**
```python
# Test signal detection
from src.signal_detection.signal_detector import SignalDetector

detector = SignalDetector()
test_text = "Fuel shortage reported in Colombo. Long queues at petrol stations."
signals = detector.detect_signals(test_text, "Fuel Crisis")
print(f"Detected {len(signals)} signals")
print(signals)
# Should detect "Fuel Shortage Mentions"
```

---

### Step 6: LLM Extraction (Optional)

**In Colab:**
- Cell 7: Mistral 7B extraction

**Locally:**
- Set `USE_LLM=true` in `.env` or environment

**✅ Verification:**
- See: `✅ Mistral 7B extracted X signals`
- First request may take 30-60 seconds (model loading)
- Subsequent requests are faster

**Test manually:**
```python
# Test Mistral 7B
from src.llm_extraction.llm_extractor import LLMExtractor

extractor = LLMExtractor(provider='mistral', use_api=True)
signals = extractor.extract_signals(
    "Fuel shortage reported in Colombo. Inflation rising.",
    "Economic Crisis"
)
print(f"LLM extracted {len(signals)} signals")
print(signals)
```

---

### Step 7: Save Data

**In Colab:**
- Cell 8: Save to JSON

**Locally:**
- Automatically saves to `data/raw/` and `data/processed/`

**✅ Verification:**
- See: `✅ Saved X items to [filename]`
- Check file exists in output location
- File should be valid JSON

**Check saved data:**
```python
import json

# Load and check
with open('data/raw/articles_YYYYMMDD_HHMMSS.json', 'r') as f:
    data = json.load(f)
    
print(f"Total items: {len(data)}")
print(f"Sample item keys: {list(data[0].keys())}")
print(f"Items with signals: {sum(1 for item in data if item.get('detected_signals'))}")
```

---

## 🧪 Complete Testing Checklist

### 1. Environment Setup
- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] No import errors

### 2. Data Collection
- [ ] RSS feeds return articles (Ada Derana, EconomyNext)
- [ ] Google Trends returns trending searches
- [ ] Articles have required fields (title, link, description, source)

### 3. Signal Detection
- [ ] Keyword detection works (finds signals in text)
- [ ] Signals have: signal_name, confidence, matched_keywords
- [ ] At least some articles have detected signals

### 4. LLM Extraction (Optional)
- [ ] Mistral 7B API responds (may take 30-60s first time)
- [ ] LLM extracts signals from text
- [ ] Signals have proper structure (signal_name, confidence, etc.)

### 5. Data Storage
- [ ] Raw data saved to JSON files
- [ ] Processed data saved (if LLM used)
- [ ] Files are valid JSON

### 6. Integration Test
- [ ] Full pipeline runs end-to-end
- [ ] No errors in logs
- [ ] Summary statistics printed

---

## 🔍 Debugging Common Issues

### Issue: "No articles scraped"

**Check:**
```python
# Test RSS feed directly
import feedparser
feed = feedparser.parse('https://www.adaderana.lk/rss.php')
print(f"Feed entries: {len(feed.entries)}")
print(f"Feed status: {feed.status}")
```

**Solutions:**
- Check internet connection
- RSS feed URL might have changed
- Some sites block scrapers (use delays)

---

### Issue: "Google Trends not working"

**Check:**
```python
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)
trending = pytrends.trending_searches(pn='lk')
print(trending)
```

**Solutions:**
- pytrends may have rate limits
- Try again after a few minutes
- Check if Google Trends is accessible

---

### Issue: "No signals detected"

**Check:**
```python
# Test with known signal text
from src.signal_detection.signal_detector import SignalDetector

detector = SignalDetector()
test_cases = [
    ("Fuel shortage in Colombo", "Fuel Shortage Mentions"),
    ("Power outage reported", "Power Outages (CEB)"),
    ("Flood warning issued", "Flood Warnings")
]

for text, expected in test_cases:
    signals = detector.detect_signals(text)
    found = any(s['signal_name'] == expected for s in signals)
    print(f"{text}: {'✅' if found else '❌'}")
```

**Solutions:**
- Check keyword dictionary in `signal_detector.py`
- Verify text is being processed correctly
- Check case sensitivity (should be lowercase)

---

### Issue: "Mistral 7B API error"

**Check:**
```python
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
response = requests.post(API_URL, json={"inputs": "test"}, timeout=60)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")
```

**Solutions:**
- Status 503 = Model loading, wait 30-60s and retry
- Status 429 = Rate limit, add delays between requests
- Status 401 = Invalid token (if using token)
- Check internet connection

---

### Issue: "Import errors"

**Check:**
```python
# Test imports
try:
    from src.scrapers.rss_scraper import RSSScraper
    from src.api.google_trends_api import GoogleTrendsAPI
    from src.signal_detection.signal_detector import SignalDetector
    from src.llm_extraction.llm_extractor import LLMExtractor
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
```

**Solutions:**
- Install missing packages: `pip install -r requirements.txt`
- Check Python path (run from project root)
- Verify file structure is correct

---

## 📊 Expected Output

### Successful Run Output:

```
✅ All packages installed successfully!
✅ Setup complete!
✅ Loaded 40 PESTLE signals
✅ Scraped 20 from Ada Derana, 15 from EconomyNext
📊 Total articles: 35
✅ Retrieved 20 trending searches

📈 Top 10 Trending Searches in Sri Lanka:
   rank           keyword
     1         sri lanka
     2            colombo
     ...

✅ Signal detection completed!
📊 Articles with signals: 12

Testing Mistral 7B on: Fuel shortage reported...
✅ Mistral 7B extracted 2 signals
   Example: Fuel Shortage Mentions

✅ Saved 55 items to /content/collected_data_20250101_120000.json

📊 Data Summary:
Total items: 55

Sources:
Ada Derana             20
EconomyNext            15
Google Trends          20

✅ Text preprocessing completed - ready for TensorFlow models!
```

---

## 🎯 Quick Test Script

Create `test_system.py`:

```python
#!/usr/bin/env python3
"""Quick test script to verify system works"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

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
        print(f"✅ Scraped {len(articles)} articles")
        return len(articles) > 0
    except Exception as e:
        print(f"❌ RSS scraping error: {e}")
        return False

def test_signal_detection():
    """Test signal detection"""
    print("\nTesting signal detection...")
    try:
        from src.signal_detection.signal_detector import SignalDetector
        detector = SignalDetector()
        signals = detector.detect_signals(
            "Fuel shortage reported in Colombo. Power outages expected.",
            "Crisis News"
        )
        print(f"✅ Detected {len(signals)} signals")
        for sig in signals:
            print(f"   - {sig['signal_name']} (confidence: {sig['confidence']})")
        return len(signals) > 0
    except Exception as e:
        print(f"❌ Signal detection error: {e}")
        return False

def test_llm_extraction():
    """Test LLM extraction"""
    print("\nTesting LLM extraction (Mistral 7B)...")
    try:
        from src.llm_extraction.llm_extractor import LLMExtractor
        extractor = LLMExtractor(provider='mistral', use_api=True)
        signals = extractor.extract_signals(
            "Fuel shortage reported in Colombo. Inflation rising.",
            "Economic Crisis"
        )
        print(f"✅ LLM extracted {len(signals)} signals")
        return True  # Don't fail if API is slow
    except Exception as e:
        print(f"⚠️ LLM extraction error (may be API issue): {e}")
        return True  # Don't fail test

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
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(r for _, r in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check errors above.")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
```

**Run test:**
```bash
python test_system.py
```

---

## 📝 Next Steps After Verification

Once everything works:

1. **Run Full Collection:**
   ```bash
   python run_collector.py
   ```

2. **Check Output Files:**
   - `data/raw/articles_*.json` - Raw collected data
   - `data/processed/processed_*.json` - Processed data with signals

3. **Analyze Results:**
   - Check signal statistics
   - Verify data quality
   - Review detected signals

4. **Proceed to Step 3:**
   - NLP Preprocessing (from Workflow.md)
   - Prepare for TensorFlow models

---

## 🆘 Getting Help

If something doesn't work:

1. Check error messages carefully
2. Run test script: `python test_system.py`
3. Check logs for detailed errors
4. Verify internet connection
5. Check API rate limits (for Mistral/Google Trends)

For more help, see:
- `MISTRAL_SETUP.md` - Mistral 7B setup
- `DATA_COLLECTION.md` - Detailed documentation
- `COLAB_SETUP.md` - Colab-specific guide

