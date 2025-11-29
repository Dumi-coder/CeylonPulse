# ✅ Status Check & Verification Guide

## Current Status

Based on your Colab run, here's what's working:

### ✅ Working Components:
1. **Package Installation** - ✅ All packages installed
2. **RSS Scraping** - ✅ Scraped 20 articles from EconomyNext
3. **Signal Detection** - ✅ Detected signals in articles
4. **Data Saving** - ✅ Saved 20 items to JSON
5. **TensorFlow** - ✅ TensorFlow 2.19.0 imported, GPU available
6. **Text Preprocessing** - ✅ Completed

### ⚠️ Needs Attention:
1. **Google Trends** - Error 404 (may be temporary or API change)
2. **Ada Derana RSS** - Not showing in output (may need check)
3. **Mistral 7B** - Extracted 0 signals (may need better prompt or API token)

---

## Verification Steps

### 1. Check Collected Data

In Colab, run:
```python
# Check what was collected
import json
import glob

# Find the latest file
files = glob.glob('/content/collected_data_*.json')
if files:
    latest_file = sorted(files)[-1]
    print(f"Latest file: {latest_file}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    print(f"\nTotal items: {len(data)}")
    print(f"\nSample item:")
    print(json.dumps(data[0], indent=2))
    
    # Check signals
    items_with_signals = [item for item in data if item.get('detected_signals')]
    print(f"\nItems with signals: {len(items_with_signals)}")
    if items_with_signals:
        print(f"Sample signals: {items_with_signals[0]['detected_signals']}")
```

### 2. Test Signal Detection

```python
# Test signal detection with known text
import re

SIGNAL_KEYWORDS = {
    "Fuel Shortage Mentions": ["fuel shortage", "petrol shortage", "diesel shortage"],
    "Power Outages (CEB)": ["power outage", "power cut", "load shedding"],
    "Flood Warnings": ["flood", "flooding", "flood warning"],
}

def detect_signals(text, title=""):
    full_text = f"{title} {text}".lower()
    detected = []
    for signal_name, keywords in SIGNAL_KEYWORDS.items():
        matches = [k for k in keywords if re.search(r'\b' + re.escape(k.lower()) + r'\b', full_text)]
        if matches:
            detected.append({
                'signal_name': signal_name,
                'confidence': min(0.5 + (len(matches) * 0.15), 1.0),
                'matched_keywords': matches
            })
    return detected

# Test cases
test_cases = [
    ("Fuel shortage reported in Colombo", "Fuel Shortage Mentions"),
    ("Power outage in several areas", "Power Outages (CEB)"),
    ("Flood warning issued", "Flood Warnings")
]

print("Testing Signal Detection:")
for text, expected in test_cases:
    signals = detect_signals(text)
    found = any(s['signal_name'] == expected for s in signals)
    print(f"  {'✅' if found else '❌'} {text} -> {expected}")
```

### 3. Test Mistral 7B API

```python
# Test Mistral 7B API directly
import requests
import json
import os

MISTRAL_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
API_URL = f"https://api-inference.huggingface.co/models/{MISTRAL_MODEL}"

# Optional: Add token for higher rate limits
# HUGGINGFACE_API_TOKEN = "your_token_here"  # Get from https://huggingface.co/settings/tokens
# headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"} if HUGGINGFACE_API_TOKEN else {}

headers = {}

prompt = """Analyze this text and extract relevant signals.

Text: Fuel shortage reported in Colombo. Long queues at petrol stations. Inflation rising.

Available signals: Fuel Shortage Mentions, Inflation Mentions, Power Outages (CEB)

Return JSON: {"signals": [{"signal_name": "Fuel Shortage Mentions", "confidence": 0.9}]}"""

formatted_prompt = f"<s>[INST] {prompt} [/INST]"

payload = {
    "inputs": formatted_prompt,
    "parameters": {
        "max_new_tokens": 500,
        "temperature": 0.3,
        "return_full_text": False
    }
}

print("Testing Mistral 7B API...")
print("(First request may take 30-60 seconds - model loading)")

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            content = result[0].get('generated_text', '')
        else:
            content = str(result)
        print(f"✅ Response received:")
        print(content[:500])
    elif response.status_code == 503:
        print("⚠️ Model is loading. Wait 30-60 seconds and try again.")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:200])
except Exception as e:
    print(f"❌ Error: {e}")
```

### 4. Check RSS Feeds

```python
# Test RSS feeds directly
import feedparser

feeds = [
    ('Ada Derana', 'https://www.adaderana.lk/rss.php'),
    ('EconomyNext', 'https://economynext.com/rss')
]

for name, url in feeds:
    try:
        feed = feedparser.parse(url)
        print(f"{name}: {len(feed.entries)} entries, status: {feed.status}")
        if feed.entries:
            print(f"  Latest: {feed.entries[0].title[:50]}...")
    except Exception as e:
        print(f"{name}: ❌ Error - {e}")
```

---

## Expected Results

### ✅ Success Indicators:

1. **Data Collection**
   - At least 10-20 articles from RSS feeds
   - Articles have: title, link, description, source, scraped_at

2. **Signal Detection**
   - At least 1-2 articles have detected signals
   - Signals have: signal_name, confidence, matched_keywords

3. **Data Storage**
   - JSON file created in `/content/`
   - File is valid JSON
   - Contains all collected items

4. **Mistral 7B** (Optional)
   - API responds (may take 30-60s first time)
   - Extracts at least 1 signal from test text
   - Returns valid JSON structure

---

## Fixing Common Issues

### Issue 1: Google Trends 404 Error

**Solution:**
- This is a known pytrends issue
- Can be ignored for now (RSS feeds are more important)
- Or try alternative: Use Google Trends manually or skip this step

### Issue 2: Mistral 7B Returns 0 Signals

**Possible Causes:**
1. Model still loading (503 error) - Wait and retry
2. Prompt not clear enough - Improve prompt format
3. API rate limit - Add token or wait

**Solution:**
```python
# Improve the prompt
prompt = f"""You are an expert analyst. Extract signals from this news:

Title: {title}
Content: {text[:1000]}

Signals to look for: Fuel Shortage, Inflation, Power Outages, Floods, Protests

For each signal found, return JSON:
{{"signals": [
  {{"signal_name": "Fuel Shortage Mentions", "confidence": 0.9, "pestle_category": "Economic"}}
]}}

Only return valid JSON, nothing else."""
```

### Issue 3: Ada Derana Not Scraping

**Check:**
```python
# Test Ada Derana RSS directly
import feedparser
feed = feedparser.parse('https://www.adaderana.lk/rss.php')
print(f"Entries: {len(feed.entries)}")
print(f"Status: {feed.status}")
print(f"Feed title: {feed.feed.get('title', 'N/A')}")
```

**Solution:**
- Check if RSS URL is still valid
- May need to update URL in config
- Check if site blocks scrapers

---

## Next Steps

### If Everything Works ✅:

1. **Review Collected Data**
   - Check signal detection accuracy
   - Verify data quality
   - Review sample articles

2. **Improve Signal Detection**
   - Add more keywords to SIGNAL_KEYWORDS
   - Test with more articles
   - Fine-tune confidence thresholds

3. **Proceed to Step 3** (Workflow.md)
   - NLP Preprocessing
   - Text cleaning and normalization
   - SBERT embeddings

### If Issues Found ❌:

1. **Run Test Script** (if available locally)
   ```bash
   python test_system.py
   ```

2. **Check Logs**
   - Review error messages
   - Check API responses
   - Verify network connectivity

3. **Fix Issues**
   - Update URLs if changed
   - Add API tokens if needed
   - Check dependencies

---

## Quick Verification Checklist

- [ ] RSS feeds return articles (10+ articles)
- [ ] Articles have all required fields
- [ ] Signal detection finds signals in test cases
- [ ] At least 1 article has detected signals
- [ ] Data saved to JSON file
- [ ] JSON file is valid and readable
- [ ] Mistral 7B API responds (optional)
- [ ] TensorFlow imports successfully
- [ ] Text preprocessing works

---

## Summary

**Current Status:** ✅ Mostly Working
- Data collection: ✅ Working
- Signal detection: ✅ Working  
- Data storage: ✅ Working
- Google Trends: ⚠️ Needs fix (optional)
- Mistral 7B: ⚠️ May need better prompts

**Recommendation:** 
- System is functional for data collection
- Focus on improving signal detection keywords
- Proceed to NLP preprocessing (Step 3)

---

**Need Help?** Check:
- `RUNNING_GUIDE.md` - Detailed running instructions
- `QUICK_START.md` - Quick reference
- `MISTRAL_SETUP.md` - Mistral 7B setup

