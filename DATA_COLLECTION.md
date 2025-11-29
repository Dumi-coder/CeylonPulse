# Data Collection Module

This module implements **Step 2** of the CeylonPulse workflow: Data Collection from multiple sources using three methods:

1. **Scraping** - Web scraping and RSS feed parsing
2. **API Responses** - Twitter API, Google Trends API
3. **LLM Extraction** - Structure data and generate signals using LLM

## Architecture

```
src/
├── scrapers/          # Web scraping modules
│   ├── rss_scraper.py    # RSS feed parser
│   └── web_scraper.py    # HTML page scraper
├── api/               # API integration modules
│   ├── twitter_api.py    # Twitter API v2 handler
│   └── google_trends_api.py  # Google Trends handler
├── llm_extraction/    # LLM-based extraction
│   └── llm_extractor.py   # Signal extraction and data structuring
├── database/          # Storage modules
│   └── storage.py        # Database storage (PostgreSQL/MongoDB/JSON)
└── data_collector.py  # Main orchestrator

config/
└── sources.py         # All data source URLs

data/
├── raw/               # Raw collected data
└── processed/         # Processed data with signals
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (copy `.env.example` to `.env`):
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Basic Usage

Run the data collector:
```bash
python run_collector.py
```

### Programmatic Usage

```python
from src.data_collector import DataCollector

# Initialize collector
collector = DataCollector(
    use_llm=True,              # Enable LLM extraction
    llm_provider='openai',     # or 'anthropic'
    db_type='json'             # 'postgres', 'mongodb', or 'json'
)

# Collect data from all sources
summary = collector.collect_all(
    use_scraping=True,         # Method 1: Scrape
    use_api=True,              # Method 2: API responses
    use_llm_extraction=True    # Method 3: LLM extraction
)

print(summary)
collector.close()
```

## Data Sources

### Scraping Sources
- **Ada Derana**: RSS feeds, news pages, breaking news, business, sports
- **EconomyNext**: RSS feeds, main site, Sri Lanka news, business, politics
- **Meteorological Department**: Warnings, weather forecasts
- **Central Bank**: Statistics, economic indicators, publications, news
- **Parliament**: News, bills, hansard, cabinet decisions
- **CEB**: Outage notices, load shedding schedules
- **NWSDB**: Announcements, water interruptions
- **Advocata**: Publications, research, commentary
- **CSE**: Market summary, listed companies, trading statistics

### API Sources
- **Twitter**: Key accounts (AdaDerana, NewsFirst, PresSecSL, PMD_SL, DMCSriLanka, CBSL, CEBSriLanka)
- **Google Trends**: Trending searches, interest over time for Sri Lanka

## Configuration

All data source URLs are configured in `config/sources.py`. You can modify or add new sources there.

## Environment Variables

Required (for LLM extraction):
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

Optional (for Twitter API):
- `TWITTER_BEARER_TOKEN`

Optional (for database):
- `DB_TYPE`: 'postgres', 'mongodb', or 'json' (default: 'json')
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `MONGODB_HOST`, `MONGODB_PORT`, `MONGODB_DB`

## Output

### Raw Data
Raw collected data is stored in:
- **JSON**: `data/raw/articles_YYYYMMDD_HHMMSS.json`
- **PostgreSQL**: `raw_articles` table
- **MongoDB**: `raw_articles` collection

### Processed Data
Processed data with extracted signals is stored in:
- **JSON**: `data/processed/processed_YYYYMMDD_HHMMSS.json`
- **PostgreSQL**: `processed_articles` and `signals` tables
- **MongoDB**: `processed_articles` collection

## Data Structure

### Raw Article
```json
{
  "title": "Article title",
  "link": "https://...",
  "description": "Article description",
  "source": "Source name",
  "source_url": "Source URL",
  "published": "Publication date",
  "scraped_at": "2025-01-XX..."
}
```

### Processed Article
```json
{
  "title": "Article title",
  "link": "https://...",
  "description": "Article description",
  "source": "Source name",
  "extracted_signals": [
    {
      "signal_name": "Inflation Mentions",
      "confidence": 0.85,
      "key_phrases": ["inflation", "price increase"],
      "pestle_category": "Economic",
      "swot_category": "Threat",
      "severity_estimate": 0.7
    }
  ],
  "structured_data": {
    "title": "Clean title",
    "summary": "2-3 sentence summary",
    "key_entities": ["entity1", "entity2"],
    "location": "Colombo",
    "impact_level": "high"
  }
}
```

## Notes

- **Rate Limiting**: The scrapers include delays between requests to be respectful to servers
- **Error Handling**: All modules include comprehensive error handling and logging
- **Fallback**: If database connections fail, the system automatically falls back to JSON file storage
- **LLM Costs**: Using LLM extraction will incur API costs. Set `USE_LLM=false` in `.env` to disable

## Troubleshooting

1. **Import Errors**: Make sure you're running from the project root directory
2. **API Errors**: Check that your API keys are set correctly in `.env`
3. **Scraping Errors**: Some websites may block scrapers. Check logs for specific errors
4. **Database Errors**: Ensure database is running and credentials are correct, or use JSON storage

