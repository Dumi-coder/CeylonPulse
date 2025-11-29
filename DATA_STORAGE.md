# 📁 Data Storage Locations

This document explains where CeylonPulse stores collected data.

## 🗂️ Storage Locations

### 1. **Local Python (Default)**

When running `python run_collector.py` locally:

#### Raw Data (Unprocessed)
```
CeylonPulse/
└── data/
    └── raw/
        └── articles_YYYYMMDD_HHMMSS.json
```

**Example:**
- `data/raw/articles_20250129_120000.json`
- `data/raw/articles_20250129_150000.json`

#### Processed Data (With Signals)
```
CeylonPulse/
└── data/
    └── processed/
        └── processed_YYYYMMDD_HHMMSS.json
```

**Example:**
- `data/processed/processed_20250129_120000.json`
- `data/processed/processed_20250129_150000.json`

---

### 2. **Google Colab**

When running the notebook in Colab:

#### Default Location (Colab VM)
```
/content/
└── collected_data_YYYYMMDD_HHMMSS.json
```

**Example:**
- `/content/collected_data_20250129_154143.json`

#### Google Drive (If Mounted)
```
/content/drive/MyDrive/
└── CeylonPulse/
    └── data/
        └── collected_data_YYYYMMDD_HHMMSS.json
```

**Note:** The notebook saves to `/content/` by default. To save to Drive, mount it first.

---

### 3. **Database Storage (Optional)**

If configured with PostgreSQL or MongoDB:

#### PostgreSQL
- **Raw Data**: `raw_articles` table
- **Processed Data**: `processed_articles` table
- **Signals**: `signals` table

#### MongoDB
- **Raw Data**: `raw_articles` collection
- **Processed Data**: `processed_articles` collection

---

## 📊 Data Structure

### Raw Data Format
```json
[
  {
    "title": "Article Title",
    "link": "https://...",
    "description": "Article description...",
    "source": "Ada Derana",
    "source_url": "https://...",
    "published": "2025-01-29T12:00:00",
    "scraped_at": "2025-01-29T12:05:00"
  },
  ...
]
```

### Processed Data Format
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
    "primary_signal": {...},
    "structured_data": {...}
  },
  ...
]
```

---

## 🔍 How to Find Your Data

### In Colab:

```python
import glob
import os

# Find all data files
files = glob.glob('/content/collected_data_*.json')
print(f"Found {len(files)} data files:")

for f in sorted(files):
    size = os.path.getsize(f) / 1024  # KB
    print(f"  - {f} ({size:.1f} KB)")

# Latest file
if files:
    latest = sorted(files)[-1]
    print(f"\nLatest: {latest}")
```

### Locally:

```bash
# List all raw data files
ls -lh data/raw/

# List all processed data files
ls -lh data/processed/

# View latest file
ls -t data/raw/ | head -1 | xargs cat | head -50

# Count items in latest file
python -c "
import json
import glob
files = glob.glob('data/raw/*.json')
if files:
    with open(sorted(files)[-1]) as f:
        data = json.load(f)
    print(f'Items: {len(data)}')
"
```

---

## 📂 Directory Structure

### Complete Structure:

```
CeylonPulse/
├── data/                          # Main data directory
│   ├── raw/                       # Raw collected data
│   │   ├── articles_20250129_120000.json
│   │   ├── articles_20250129_150000.json
│   │   └── ...
│   └── processed/                 # Processed data with signals
│       ├── processed_20250129_120000.json
│       ├── processed_20250129_150000.json
│       └── ...
│
├── config/                        # Configuration
├── src/                           # Source code
│   ├── database/
│   │   └── storage.py            # Storage logic
│   └── ...
└── ...
```

---

## 🔧 Configuration

### Change Storage Location

#### For Local Python:

Edit `src/database/storage.py`:
```python
# Change default directory
self.data_dir = 'your/custom/path/raw'
```

Or set environment variable:
```bash
export DATA_DIR='/path/to/data'
```

#### For Colab:

Edit the notebook cell that saves data:
```python
# Change output path
output_file = f'/content/drive/MyDrive/CeylonPulse/data/collected_data_{timestamp}.json'
```

---

## 💾 Database Storage

### PostgreSQL Setup:

1. **Set environment variables:**
```bash
export DB_TYPE=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=ceylonpulse
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=your_password
```

2. **Data stored in:**
   - `raw_articles` table
   - `processed_articles` table
   - `signals` table

### MongoDB Setup:

1. **Set environment variables:**
```bash
export DB_TYPE=mongodb
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_DB=ceylonpulse
```

2. **Data stored in:**
   - `raw_articles` collection
   - `processed_articles` collection

---

## 📈 Viewing Data

### Quick View (Python):

```python
import json
import glob

# Get latest file
files = glob.glob('data/raw/*.json')
if files:
    latest = sorted(files)[-1]
    
    with open(latest, 'r') as f:
        data = json.load(f)
    
    print(f"Total items: {len(data)}")
    print(f"\nFirst item:")
    print(json.dumps(data[0], indent=2))
    
    # Statistics
    sources = {}
    for item in data:
        source = item.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print(f"\nSources:")
    for source, count in sources.items():
        print(f"  {source}: {count}")
```

### Quick View (Command Line):

```bash
# View first item
cat data/raw/articles_*.json | python -m json.tool | head -30

# Count items
cat data/raw/articles_*.json | python -c "import sys, json; print(len(json.load(sys.stdin)))"

# List all files with sizes
find data/ -name "*.json" -exec ls -lh {} \;
```

---

## 🗑️ Managing Storage

### Delete Old Files:

```bash
# Delete files older than 7 days
find data/raw/ -name "*.json" -mtime +7 -delete
find data/processed/ -name "*.json" -mtime +7 -delete

# Keep only last 10 files
ls -t data/raw/*.json | tail -n +11 | xargs rm
```

### Archive Data:

```bash
# Create archive
tar -czf data_backup_$(date +%Y%m%d).tar.gz data/

# Or zip
zip -r data_backup_$(date +%Y%m%d).zip data/
```

---

## 📝 Summary

| Location | Type | Path |
|----------|------|------|
| **Local** | Raw | `data/raw/articles_*.json` |
| **Local** | Processed | `data/processed/processed_*.json` |
| **Colab** | Combined | `/content/collected_data_*.json` |
| **Colab Drive** | Combined | `/content/drive/MyDrive/CeylonPulse/data/` |
| **PostgreSQL** | Tables | `raw_articles`, `processed_articles`, `signals` |
| **MongoDB** | Collections | `raw_articles`, `processed_articles` |

---

## 🚀 Quick Access

### Find Latest File:

**Colab:**
```python
import glob
latest = sorted(glob.glob('/content/collected_data_*.json'))[-1]
print(f"Latest: {latest}")
```

**Local:**
```bash
ls -t data/raw/*.json | head -1
```

### View Data:

**Colab:**
```python
import json
with open(latest, 'r') as f:
    data = json.load(f)
print(f"Items: {len(data)}")
```

**Local:**
```bash
cat $(ls -t data/raw/*.json | head -1) | python -m json.tool | head -50
```

---

**Your data is stored safely!** 📁

Check the paths above to find your collected data.

