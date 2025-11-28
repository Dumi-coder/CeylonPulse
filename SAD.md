Below is your **System Architecture Document (SAD v1.0)** in **perfect README.md format** — ready to paste into GitHub.

You can directly copy this into your project’s README.

---

# # 📘 System Architecture Document (SAD v1.0)

### **National Signal Intelligence System – Sri Lanka**

**Purpose:** Collect, process, and interpret real-time signals relevant to Sri Lanka’s socio-economic and operational environment, producing:

* **National Activity Indicators**
* **Operational Environment Indicators**
* **Risk & Opportunity Insights (via PESTLE + SWOT)**

---

# ## 📑 Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Data Sources](#data-sources)
4. [Data Pipeline](#data-pipeline)
5. [NLP Pipeline](#nlp-pipeline)
6. [Event Detection Engine](#event-detection-engine)
7. [PESTLE Classification Engine](#pestle-classification-engine)
8. [SWOT Insight Engine](#swot-insight-engine)
9. [API Structure](#api-structure)
10. [Dashboard Architecture](#dashboard-architecture)
11. [System Data Flow Diagram](#system-data-flow-diagram)
12. [Tech Stack](#tech-stack)
13. [Team Responsibilities](#team-responsibilities)

---

# ## 1. Overview

This system monitors **40 real-time signals** across Political, Economic, Social, Technological, Legal, and Environmental domains.

The system transforms raw information → cleaned data → events → insights for businesses.

---

# ## 2. High-Level Architecture

```
DATA SOURCES  
      ↓  
SCRAPERS & API FETCHERS  
      ↓  
RAW DATA STORAGE (JSON)  
      ↓  
NLP PROCESSOR  
      - Cleaning  
      - Keyword Extraction  
      - NER  
      - SBERT Embeddings  
      - Clustering  
      - Sentiment Analysis  
      ↓  
EVENT DETECTION ENGINE  
      - Frequency Burst  
      - Severity Scoring  
      - Location Extraction  
      ↓  
PESTLE CLASSIFICATION  
      ↓  
SWOT INSIGHT ENGINE  
      ↓  
INSIGHTS API  
      ↓  
DASHBOARD (Web UI)
```

---

# ## 3. Data Sources

### **News**

* DailyMirror, Newswire, Ada Derana, FT.lk

### **Social Media**

* Twitter (X)

### **Government**

* Met Department
* Disaster Management Center
* CEB (Power Outage)
* NWSDB (Water Supply)
* Parliament & Cabinet updates

### **Search Trends**

* Google Trends (tourism, fuel, migration, etc.)

### **Research Institutions**

* Advocata
* BRS Equity Research
* John Keells Research

---

# ## 4. Data Pipeline

### **4.1 Data Collection**

* Python scrapers (Requests, BeautifulSoup)
* API ingestion (weather, search trends, gov data)
* Social media (Tweepy/revX API)

### **4.2 Data Storage**

Structure:

```
/data/raw/
    source_name_YYYYMMDD.json
/data/processed/
    processed_signal_data.json
```

### **4.3 Data Normalization**

* lowercase conversion
* remove noise
* timestamp normalization
* JSON standardization

---

# ## 5. NLP Pipeline

### **5.1 Cleaning**

* removing emojis, URLs, symbols
* stopword filtering

### **5.2 Keyword Extraction**

* predefined dictionary per signal
* additional dynamic extraction (RAKE, YAKE)

### **5.3 Named Entity Recognition (NER)**

Extract:

* **Locations**
* **Organizations**
* **Persons**
* **Events**

### **5.4 Sentence Embeddings**

* Model: **SBERT (all-mpnet-base-v2)**
* Used for clustering similar news/tweets

### **5.5 Clustering**

* Algorithm: **HDBSCAN**
* Removes duplicates
* Groups similar incidents

### **5.6 Sentiment Analysis**

* Model: **HuggingFace - DistilBERT**
* Polarity: +1 to –1

---

# ## 6. Event Detection Engine

### Each event must satisfy:

* **Signal match**
* **Keyword presence**
* **Frequency spike**
* **Clustering score > threshold**
* **Severity score computed**
* **Location extracted**

### Event Object Format:

```
{
  "event_id": "EVT_20251127_1832",
  "signal": "Fuel Shortage",
  "severity": 0.82,
  "sentiment": -0.44,
  "location": "Colombo",
  "frequency_change": "+27%",
  "timestamp": "2025-11-27T14:00:00",
  "raw_text": "Long queues seen at several fuel stations..."
}
```

---

# ## 7. PESTLE Classification Engine

Uses mapping from SSD:

| PESTLE                | Types of Signals                      |
| --------------------- | ------------------------------------- |
| **P – Political**     | Protests, policy changes, strikes     |
| **E – Economic**      | Fuel, inflation, dollar rate, tourism |
| **S – Social**        | Crime, public sentiment, migration    |
| **T – Technological** | Power outages, telecom outages        |
| **L – Legal**         | Regulations, court rulings            |
| **E – Environmental** | Floods, rainfall, heat waves          |

### PESTLE Output Example:

```
"pestle": "Economic"
```

---

# ## 8. SWOT Insight Engine

Mapping:

| PESTLE        | SWOT Output            |
| ------------- | ---------------------- |
| Political     | Threat                 |
| Economic      | Opportunity / Threat   |
| Social        | Opportunity / Weakness |
| Technological | Strength / Opportunity |
| Legal         | Threat                 |
| Environmental | Threat                 |

### Final Insight Example:

```
{
  "event": "Fuel shortages increasing",
  "pestle": "Economic",
  "swot": "Threat",
  "impact_score": 0.78,
  "recommendation": "Businesses should prepare for supply delays."
}
```

---

# ## 9. API Structure

### `/api/events`

Returns real-time detected events.

### `/api/signals`

Returns frequency and trend data for each signal.

### `/api/insights`

Returns SWOT + PESTLE insights.

### `/api/pestle`

Distribution of events per PESTLE category.

### `/api/swot`

Business insight summary.

---

# ## 10. Dashboard Architecture

### Panels:

* **National Activity Indicators**
* **Operational Environment Indicators**
* **Risk & Opportunity Insights**
* **PESTLE Wheel / Radar Chart**
* **SWOT Matrix**
* **Top Events Today**
* **Sri Lanka Heat Map (district-wise events)**

### Frontend:

* React / Next.js
* Tailwind CSS
* Chart.js / Plotly

### Backend:

* FastAPI / Flask
* Cron jobs for periodic updates

---

# ## 11. System Data Flow Diagram (ASCII)

```
[ Scrapers ] --> [ Raw Data Store ]
                       ↓
                  [ NLP Engine ]
                       ↓
              [ Event Detection ]
                       ↓
            [ PESTLE Classification ]
                       ↓
               [ SWOT Insights ]
                       ↓
                 [ Insights API ]
                       ↓
                 [ Dashboard UI ]
```

---

# ## 12. Tech Stack

### **Backend**

* Python
* FastAPI
* BeautifulSoup / Requests
* spaCy
* SBERT
* scikit-learn
* HuggingFace transformers

### **Frontend**

* React / Next.js
* Tailwind CSS
* Chart.js

### **Database**

* MongoDB / PostgreSQL
* Or simple JSON files if rushed

---

# ## 13. Team Responsibilities

### 👤 **Member 1 – Data Engineer**

* All scrapers
* Data standardization
* API fetchers

### 👤 **Member 2 – NLP/ML Engineer**

* NER
* Keyword extraction
* Clustering
* Event detection

### 👤 **Member 3 – Insight Engineer**

* PESTLE engine
* SWOT logic
* Scoring system
* Recommendations

### 👤 **Member 4 – Frontend Engineer**

* Dashboard
* API integration
* Visualizations

---

# ✅ **SAD v1.0 is Ready**

Your next step is:

👉 **Start implementing scrapers & NLP based on this architecture.**
If you want, I can now generate:

### ✔ Code templates

### ✔ Folder structure

### ✔ API design

### ✔ Dashboard UI mockup

Just tell me: **“Next step.”**
