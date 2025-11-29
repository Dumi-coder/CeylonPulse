# 🚀 Complete Colab Notebook Guide

## Overview

**`CeylonPulse_Complete.ipynb`** contains **ALL** functionality from the Python modules - everything runs in Google Colab!

No need for local Python files - just upload and run! 🎉

---

## 📋 What's Included

### ✅ All Components:

1. **RSS Feed Scraping** - Ada Derana, EconomyNext
2. **Google Trends API** - Trending searches for Sri Lanka
3. **Signal Detection** - 40 PESTLE signals with keyword matching
4. **Mistral 7B LLM** - Signal extraction via Hugging Face API
5. **Data Storage** - Saves to Colab VM and Google Drive
6. **TensorFlow Setup** - Ready for ML models
7. **Statistics & Analysis** - Signal counts, summaries

---

## 🎯 How to Use

### Step 1: Upload to Colab

1. Open Google Colab: https://colab.research.google.com/
2. Upload `CeylonPulse_Complete.ipynb`
3. Or open directly if in Drive

### Step 2: Run All Cells

**Option A: Run All**
- Click "Runtime" → "Run all"
- Wait for all cells to complete

**Option B: Run Sequentially**
- Run each cell one by one (Shift+Enter)
- Check output before proceeding

### Step 3: Check Results

- Look for ✅ success messages
- Review data summary
- Check saved JSON files

---

## 📁 Data Storage Locations

### In Colab VM:
```
/content/collected_data_YYYYMMDD_HHMMSS.json
```

### In Google Drive (if mounted):
```
/content/drive/MyDrive/CeylonPulse/data/collected_data_YYYYMMDD_HHMMSS.json
```

---

## 🔧 Configuration

### Enable/Disable Features:

Edit Cell 4 (Configuration):

```python
USE_LLM = True  # Mistral 7B extraction
USE_GOOGLE_TRENDS = True  # Google Trends API
USE_TWITTER = False  # Twitter API (if you have token)
```

### Hugging Face Token:

Already configured in Cell 4:
```python
HUGGINGFACE_API_TOKEN = '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'
```

---

## 📊 Notebook Structure

| Cell | Step | Description |
|------|------|-------------|
| 1 | Setup | Install packages |
| 2 | Config | Import libraries, set tokens |
| 3 | Load | Load 40 signals & data sources |
| 4 | RSS | Scrape RSS feeds |
| 5 | Trends | Get Google Trends |
| 6 | Signals | Keyword-based detection |
| 7 | LLM | Mistral 7B extraction |
| 8 | Save | Save to JSON |
| 9 | TensorFlow | Text preprocessing |
| 10 | Summary | Statistics & results |

---

## ✅ Expected Output

```
✅ All packages installed successfully!
✅ Libraries imported!
✅ Hugging Face token configured
✅ Loaded 40 PESTLE signals
✅ Configured 6 data sources

Scraping RSS feeds...
✅ Scraped 20 articles from Ada Derana
✅ Scraped 15 articles from EconomyNext
📊 Total articles scraped: 35

✅ Retrieved 20 trending searches from Google Trends

Detecting signals in articles...
✅ Signal detection completed!
📊 Articles with signals: 12 / 35

Extracting signals using Mistral 7B...
✅ LLM extraction completed on 5 articles

✅ Saved 55 items to /content/collected_data_20250129_120000.json

📊 Data Summary:
Total items: 55

Sources:
Ada Derana             20
EconomyNext            15
Google Trends          20

📈 Top 10 Detected Signals:
   Fuel Shortage Mentions: 5
   Inflation Mentions: 4
   Power Outages (CEB): 3
   ...
```

---

## 🔍 Viewing Collected Data

### In Colab:

```python
import json
import glob

# Find latest file
files = glob.glob('/content/collected_data_*.json')
if files:
    latest = sorted(files)[-1]
    print(f"Latest: {latest}")
    
    with open(latest, 'r') as f:
        data = json.load(f)
    
    print(f"Total items: {len(data)}")
    print(f"\nFirst item:")
    print(json.dumps(data[0], indent=2))
```

### Download from Colab:

```python
from google.colab import files

# Download the latest file
files.download('/content/collected_data_20250129_120000.json')
```

---

## 🐛 Troubleshooting

### Issue: "No articles scraped"

**Solution:**
- Check internet connection
- RSS feeds may be temporarily unavailable
- Try running the cell again

### Issue: "Google Trends 404"

**Solution:**
- This is a known pytrends issue
- Can be ignored (RSS feeds are more important)
- Or disable: `USE_GOOGLE_TRENDS = False`

### Issue: "Mistral 7B API error 503"

**Solution:**
- Model is loading (first request)
- Wait 30-60 seconds and try again
- Subsequent requests are faster

### Issue: "Import errors"

**Solution:**
- Run Cell 1 (install packages) first
- Check all packages installed successfully
- Restart runtime if needed

---

## 🚀 Advantages of Colab-Only Approach

### ✅ Benefits:

1. **No Local Setup** - Everything in browser
2. **Free GPU** - TensorFlow can use GPU
3. **Easy Sharing** - Share notebook link
4. **Persistent Storage** - Save to Drive
5. **Version Control** - Save notebook versions
6. **Collaboration** - Multiple people can use

### 📝 Notes:

- Colab sessions timeout after inactivity
- Free tier has usage limits
- Data in `/content/` is temporary (save to Drive!)

---

## 💾 Saving to Drive

### Mount Drive:

The notebook automatically tries to mount Drive in Cell 8.

**Manual mount:**
```python
from google.colab import drive
drive.mount('/content/drive')
```

**Save to Drive:**
```python
drive_file = '/content/drive/MyDrive/CeylonPulse/data/collected_data.json'
with open(drive_file, 'w') as f:
    json.dump(all_data, f, indent=2)
```

---

## 📈 Next Steps

After data collection:

1. **Review Data** - Check signal detection accuracy
2. **Step 3** - NLP Preprocessing (add cells for SBERT)
3. **Step 4** - Deep Learning Models (BERT, LSTM)
4. **Step 5** - Model Training
5. **Step 6** - Model Evaluation

---

## 🔄 Updating the Notebook

### Add New Features:

1. Add new cells for new functionality
2. Keep cells organized by step
3. Add markdown cells for documentation
4. Test each cell before proceeding

### Example: Add NLP Preprocessing

```python
# New cell after Step 9
# Install sentence-transformers
%pip install -q sentence-transformers

from sentence_transformers import SentenceTransformer

# Load SBERT model
model = SentenceTransformer('all-mpnet-base-v2')

# Generate embeddings
embeddings = model.encode(df['processed_text'].tolist())
print(f"✅ Generated {len(embeddings)} embeddings")
```

---

## 📚 Comparison: Notebook vs Python Files

| Feature | Notebook | Python Files |
|---------|----------|--------------|
| **Setup** | ✅ Easy (just upload) | ❌ Need local Python |
| **GPU Access** | ✅ Free GPU | ❌ Need own GPU |
| **Sharing** | ✅ Share link | ❌ Need Git/repo |
| **Collaboration** | ✅ Multiple users | ❌ Local only |
| **Version Control** | ✅ Save versions | ✅ Git |
| **Persistence** | ⚠️ Save to Drive | ✅ Local files |

**Recommendation:** Use notebook for development/experimentation, Python files for production.

---

## 🎉 Summary

**`CeylonPulse_Complete.ipynb`** is a self-contained notebook with all functionality!

**Just:**
1. Upload to Colab
2. Run all cells
3. Get collected data

**No local Python setup needed!** 🚀

---

**Need Help?**
- Check cell outputs for errors
- Review this guide
- See `RUNNING_GUIDE.md` for detailed instructions

