# 📁 Data Storage Locations

This guide shows where all collected data is stored.

## 🗂️ Storage Locations

### **Option 1: Google Colab**

When running in Colab, data is saved to:

```
/content/collected_data_YYYYMMDD_HHMMSS.json
```

**Example:**
```
/content/collected_data_20251129_154143.json
```

**To save to Google Drive (optional):**
```python
# In Colab notebook, after mounting Drive
drive_file = f'/content/drive/MyDrive/CeylonPulse/data/collected_data_{timestamp}.json'
os.makedirs(os.path.dirname(drive_file), exist_ok=True)
with open(drive_file, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)
```

---

### **Option 2: Local Python (run_collector.py)**

When running locally, data is saved to:

#### **Raw Data:**
```
CeylonPulse/
└── data/
    └── raw/
        └── articles_YYYYMMDD_HHMMSS.json
```

**Example:**
```
/home/dumindu/Programming/python/CeylonPulse/data/raw/articles_20251129_154143.json
```

#### **Processed Data (with signals):**
```
CeylonPulse/
└── data/
    └── processed/
        └── processed_YYYYMMDD_HHMMSS.json
```

**Example:**
```
/home/dumindu/Programming/python/CeylonPulse/data/processed/processed_20251129_154143.json
```

---

## 📊 Data Structure

### Raw Data File (`articles_*.json`)

Contains all collected articles before processing:

```json
[
  {
    "title": "Article Title",
    "link": "https://...",
    "description": "Article description...",
    "source": "Ada Derana",
    "source_url": "https://www.adaderana.lk/rss.php",
    "published": "2025-11-29T10:00:00",
    "scraped_at": "2025-11-29T15:41:43.123456"
  },
  ...
]
```

### Processed Data File (`processed_*.json`)

Contains articles with detected signals:

```json
[
  {
    "title": "Article Title",
    "link": "https://...",
    "description": "Article description...",
    "source": "Ada Derana",
    "detected_signals": [
      {
        "signal_name": "Fuel Shortage Mentions",
        "confidence": 0.85,
        "matched_keywords": ["fuel shortage", "petrol"],
        "pestle_category": "Economic",
        "swot_category": "Threat",
        "priority": "HIGH"
      }
    ],
    "signal_count": 1,
    "primary_signal": {...}
  },
  ...
]
```

---

## 🔍 How to Find Your Data

### In Colab:

```python
# List all collected data files
import glob
import os

files = glob.glob('/content/collected_data_*.json')
print(f"Found {len(files)} data files:")
for f in sorted(files):
    size = os.path.getsize(f) / 1024  # KB
    print(f"  - {os.path.basename(f)} ({size:.1f} KB)")

# Get latest file
if files:
    latest = sorted(files)[-1]
    print(f"\nLatest file: {latest}")
    
    # Load and check
    import json
    with open(latest, 'r') as f:
        data = json.load(f)
    print(f"Total items: {len(data)}")
```

### Locally:

```bash
# List raw data files
ls -lh data/raw/

# List processed data files
ls -lh data/processed/

# View latest raw file
ls -t data/raw/*.json | head -1 | xargs cat | head -100

# Count items in latest file
python3 -c "
import json
import glob
files = sorted(glob.glob('data/raw/*.json'))
if files:
    with open(files[-1]) as f:
        data = json.load(f)
    print(f'Latest file: {files[-1]}')
    print(f'Total items: {len(data)}')
    print(f'Items with signals: {sum(1 for item in data if item.get(\"detected_signals\"))}')
"
```

---

## 📂 Directory Structure

```
CeylonPulse/
├── data/
│   ├── raw/                          # Raw collected data
│   │   ├── articles_20251129_120000.json
│   │   ├── articles_20251129_150000.json
│   │   └── ...
│   └── processed/                    # Processed data with signals
│       ├── processed_20251129_120000.json
│       ├── processed_20251129_150000.json
│       └── ...
│
└── (Colab: /content/)
    └── collected_data_YYYYMMDD_HHMMSS.json
```

---

## 💾 Database Storage (Optional)

If you configure PostgreSQL or MongoDB:

### PostgreSQL:
- **Raw data**: `raw_articles` table
- **Processed data**: `processed_articles` table
- **Signals**: `signals` table

### MongoDB:
- **Raw data**: `raw_articles` collection
- **Processed data**: `processed_articles` collection

**To use database:**
```python
# In run_collector.py or notebook
collector = DataCollector(
    db_type='postgres',  # or 'mongodb'
    db_connection='postgresql://user:pass@localhost/ceylonpulse'
)
```

---

## 📥 Downloading Data from Colab

### Option 1: Download directly
```python
# In Colab
from google.colab import files

files.download('/content/collected_data_20251129_154143.json')
```

### Option 2: Save to Drive
```python
# Mount Drive first
from google.colab import drive
drive.mount('/content/drive')

# Save to Drive
drive_path = '/content/drive/MyDrive/CeylonPulse/data/'
os.makedirs(drive_path, exist_ok=True)

with open(f'{drive_path}collected_data_{timestamp}.json', 'w') as f:
    json.dump(all_data, f, indent=2)
```

### Option 3: Copy to local
```bash
# If you have Colab connected to local machine
scp user@colab:/content/collected_data_*.json ./data/raw/
```

---

## 🔄 Data File Naming

Files are named with timestamps:

- **Format**: `articles_YYYYMMDD_HHMMSS.json`
- **Example**: `articles_20251129_154143.json`
  - Date: 2025-11-29
  - Time: 15:41:43

This allows you to:
- Track when data was collected
- Keep historical data
- Sort files by time

---

## 📈 Checking Data Size

```python
# In Python
import os
import glob

# Check file sizes
raw_files = glob.glob('data/raw/*.json')
processed_files = glob.glob('data/processed/*.json')

total_raw = sum(os.path.getsize(f) for f in raw_files) / (1024*1024)  # MB
total_processed = sum(os.path.getsize(f) for f in processed_files) / (1024*1024)  # MB

print(f"Raw data: {total_raw:.2f} MB ({len(raw_files)} files)")
print(f"Processed data: {total_processed:.2f} MB ({len(processed_files)} files)")
```

```bash
# In terminal
du -sh data/raw/
du -sh data/processed/
```

---

## 🗑️ Cleaning Old Data

```python
# Keep only last N files
import glob
import os

# Keep last 10 files
files = sorted(glob.glob('data/raw/*.json'))
if len(files) > 10:
    for f in files[:-10]:
        os.remove(f)
        print(f"Deleted: {f}")
```

---

## 📋 Summary

| Location | Path | Contains |
|----------|------|----------|
| **Colab** | `/content/collected_data_*.json` | All collected data |
| **Local Raw** | `data/raw/articles_*.json` | Raw articles |
| **Local Processed** | `data/processed/processed_*.json` | Articles with signals |
| **PostgreSQL** | `raw_articles` table | Raw data (if configured) |
| **MongoDB** | `raw_articles` collection | Raw data (if configured) |

---

## ✅ Quick Check Commands

```bash
# Check if data exists
ls -la data/raw/
ls -la data/processed/

# Count files
ls data/raw/*.json | wc -l
ls data/processed/*.json | wc -l

# View latest file info
ls -lh data/raw/*.json | tail -1
```

```python
# In Python/Colab
import glob
import json

# Find and load latest file
files = glob.glob('data/raw/*.json')  # or '/content/collected_data_*.json'
if files:
    latest = sorted(files)[-1]
    with open(latest) as f:
        data = json.load(f)
    print(f"File: {latest}")
    print(f"Items: {len(data)}")
    print(f"Sample: {data[0] if data else 'Empty'}")
```

---

**Your data is stored in these locations!** 📁

Check the paths above to find your collected data files.

