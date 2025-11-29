# 🚀 Quick Start Guide

## Current Status ✅

You've successfully:
- ✅ Pulled the latest code from main
- ✅ Have the Colab notebook ready (`CeylonPulse_DataCollection.ipynb`)
- ✅ All components are in place

## Next Steps

### Option 1: Run in Google Colab (Easiest)

1. **Open the Notebook**
   - Upload `CeylonPulse_DataCollection.ipynb` to Google Colab
   - Or open it directly if it's in your Drive

2. **Run All Cells**
   - Click "Runtime" → "Run all"
   - Or run each cell sequentially (Shift+Enter)

3. **What to Expect**
   ```
   ✅ All packages installed successfully!
   ✅ Loaded 40 PESTLE signals
   ✅ Scraped X from Ada Derana, Y from EconomyNext
   ✅ Retrieved X trending searches
   ✅ Signal detection completed!
   ✅ Mistral 7B extracted X signals
   ✅ Saved X items to collected_data_*.json
   ```

### Option 2: Run Locally

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test System First** (Recommended)
   ```bash
   python test_system.py
   ```
   This verifies everything works before running the full collection.

3. **Run Data Collection**
   ```bash
   python run_collector.py
   ```

4. **Check Results**
   ```bash
   # View collected data
   ls -la data/raw/
   ls -la data/processed/
   
   # View a sample file
   cat data/raw/articles_*.json | head -100
   ```

---

## Verification Checklist

After running, verify:

- [ ] **Packages installed** - No import errors
- [ ] **RSS feeds working** - Articles scraped from Ada Derana & EconomyNext
- [ ] **Google Trends working** - Trending searches retrieved
- [ ] **Signal detection working** - Some articles have detected signals
- [ ] **LLM extraction working** - Mistral 7B extracts signals (may take 30-60s first time)
- [ ] **Data saved** - JSON files created in `data/raw/` and `data/processed/`

---

## Common Issues & Solutions

### Issue: "No articles scraped"
- **Check**: Internet connection
- **Solution**: RSS feeds may be temporarily unavailable, try again later

### Issue: "Mistral 7B API error - 503"
- **Check**: Model is loading
- **Solution**: Wait 30-60 seconds and try again (first request loads the model)

### Issue: "Import errors"
- **Check**: All packages installed
- **Solution**: Run `pip install -r requirements.txt`

### Issue: "No signals detected"
- **Check**: Test with known text
- **Solution**: Run `python test_system.py` to verify signal detection

---

## File Structure

```
CeylonPulse/
├── CeylonPulse_DataCollection.ipynb  # Colab notebook
├── run_collector.py                  # Local runner
├── test_system.py                    # Test script
├── requirements.txt                  # Dependencies
├── config/
│   └── sources.py                    # Data source URLs
├── src/
│   ├── scrapers/                     # Web scraping
│   ├── api/                          # API handlers
│   ├── signal_detection/            # Signal detection
│   ├── llm_extraction/              # Mistral 7B
│   └── database/                     # Data storage
└── data/
    ├── raw/                          # Raw collected data
    └── processed/                    # Processed data with signals
```

---

## What Each Component Does

1. **Scrapers** (`src/scrapers/`)
   - RSS feeds: Ada Derana, EconomyNext
   - Web scraping: Government sites, news portals

2. **API Handlers** (`src/api/`)
   - Google Trends: Trending searches
   - Twitter: Social media data (optional)

3. **Signal Detection** (`src/signal_detection/`)
   - Keyword matching for 40 PESTLE signals
   - Based on SSD (Signal Specification Document)

4. **LLM Extraction** (`src/llm_extraction/`)
   - Mistral 7B Instruct (FREE via Hugging Face)
   - Extracts signals and structures data

5. **Data Storage** (`src/database/`)
   - Saves to JSON files (default)
   - Can use PostgreSQL/MongoDB (optional)

---

## Expected Output

### Terminal/Colab Output:
```
============================================================
CeylonPulse Data Collector
============================================================
LLM Extraction: Enabled
LLM Provider: mistral
Database Type: json
============================================================

Starting data collection...
Method 1: Scraping data...
✅ Scraped 20 articles from Ada Derana RSS
✅ Scraped 15 articles from EconomyNext RSS
✅ Collected 35 articles via web scraping

Method 2: Collecting data via APIs...
✅ Retrieved 20 trending searches from Google Trends

Detecting signals using keyword matching (SSD-based)...
✅ Detected signals in 12 articles

Method 3: Using LLM to extract additional signals...
✅ Mistral 7B extracted signals from articles

Saved 55 raw data items
Saved 55 processed data items

============================================================
Collection Summary
============================================================
Raw Data Collected: 55
Processed Data: 55
Signals Extracted: 28
Sources:
  - rss_feeds: 35
  - web_scraping: 0
  - api: 20
============================================================
```

### Generated Files:
- `data/raw/articles_YYYYMMDD_HHMMSS.json` - Raw collected data
- `data/processed/processed_YYYYMMDD_HHMMSS.json` - Processed data with signals

---

## Next Steps After Data Collection

Once data collection works:

1. **Review Collected Data**
   - Check signal detection accuracy
   - Verify data quality

2. **Proceed to Step 3** (from Workflow.md)
   - NLP Preprocessing
   - Text cleaning, tokenization
   - SBERT embeddings

3. **Proceed to Step 4** (from Workflow.md)
   - Deep Learning Models
   - BERT for classification
   - LSTM for sentiment/forecasting

---

## Getting Help

- **Detailed Guide**: See `RUNNING_GUIDE.md`
- **Colab Setup**: See `COLAB_SETUP.md`
- **Mistral Setup**: See `MISTRAL_SETUP.md`
- **Test System**: Run `python test_system.py`

---

## Quick Commands Reference

```bash
# Test everything works
python test_system.py

# Run data collection
python run_collector.py

# Check collected data
ls -la data/raw/
cat data/raw/articles_*.json | python -m json.tool | head -50

# View signal statistics
python -c "
import json
import glob
files = glob.glob('data/processed/*.json')
if files:
    with open(files[-1]) as f:
        data = json.load(f)
    signals = [s for item in data for s in item.get('detected_signals', [])]
    print(f'Total signals: {len(signals)}')
    from collections import Counter
    print('Top signals:', Counter(s['signal_name'] for s in signals).most_common(5))
"
```

---

**Ready to go!** 🚀

Just run the Colab notebook or `python run_collector.py` and you're all set!

