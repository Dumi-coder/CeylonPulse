# CeylonPulse 🇱🇰

**Real-time Situational Awareness & Business Intelligence Platform for Sri Lanka**

## 👥 Team Structure

### **Backend & Analysis Team** 
- Dumindu ,  Kavindu
  
### **Dashboard Team** 
- Dimath  ,  Harshad

## 🎯 Overview

CeylonPulse is an intelligent platform that monitors real-time socio-economic signals across Sri Lanka, providing businesses with actionable insights through **PESTLE analysis** and **SWOT intelligence**. Our system transforms raw data from news, social media, and public sources into strategic business intelligence.

> Built for the **ModelX Final Competition** | Turning data into strategic advantage

## 🚀 Features

### 🔍 **Real-time Monitoring**
- **Multi-source Data Collection**: News websites, social media trends, public datasets
- **Continuous Updates**: Automated data pipelines refresh every 30 minutes
- **Sri Lanka Focus**: Tailored data sources specifically for Lankan context

### 📊 **PESTLE Analysis Engine**
- **Political**: Government policies, regulations, political stability
- **Economic**: Market trends, inflation, currency fluctuations
- **Social**: Public sentiment, cultural events, demographic shifts
- **Technological**: Digital adoption, innovation, infrastructure
- **Legal**: Compliance requirements, legal reforms
- **Environmental**: Weather patterns, climate events, sustainability

### 💡 **SWOT Intelligence**
- **Strengths**: Positive internal business environment factors
- **Weaknesses**: Operational challenges and limitations
- **Opportunities**: Emerging market trends and positive developments
- **Threats**: External risks and competitive pressures

### 📈 **Business Insights**
- **National Activity Indicators**: Trending topics and major developments
- **Operational Environment Scores**: Business impact metrics (0-100)
- **Risk & Opportunity Alerts**: Early warnings and positive trend detection
- **Industry-specific Intelligence**: Retail, Tourism, Manufacturing, Technology

## 🚀 Quick Start

### Run Data Collection

**Option 1: Google Colab (Recommended)**
1. Upload `CeylonPulse_DataCollection.ipynb` to Google Colab
2. Run all cells sequentially
3. Check output for ✅ success messages

**Option 2: Local Python**
```bash
# Install dependencies
pip install -r requirements.txt

# Run data collection
python run_collector.py

# Or test system first
python test_system.py
```

**For detailed instructions, see:**
- `RUNNING_GUIDE.md` - Complete running guide
- `COLAB_SETUP.md` - Colab-specific setup
- `MISTRAL_SETUP.md` - Mistral 7B setup

---

## 🏗️ Architecture

```mermaid
graph TB
    A[Data Sources] --> B[Data Acquisition]
    B --> C[Data Processing]
    C --> D[PESTLE Analysis]
    D --> E[SWOT Classification]
    E --> F[Business Intelligence]
    F --> G[Dashboard]
    
    A1[News Websites] --> B
    A2[Social Media] --> B
    A3[Public Datasets] --> B
    
    G --> H[Alerts & Notifications]
    G --> I[Visual Analytics]
    G --> J[Exportable Reports]
    
    style B fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style G fill:#fff3e0
