# CeylonPulse
Real-time situational awareness platform for Sri Lankan businesses.  Monitors news, social media &amp; public data to provide PESTLE+SWOT business intelligence.

# CeylonPulse 🇱🇰

**Real-time Situational Awareness & Business Intelligence Platform for Sri Lanka**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.23%2B-red)](https://streamlit.io)
[![MongoDB](https://img.shields.io/badge/MongoDB-5.0%2B-green)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/your-username/CeylonPulse)

## 👥 Team Structure

### 🎨 **Dashboard Team** (2 Members)
- **Frontend Developer** - Streamlit UI, visualizations, user experience
- **Dashboard Architect** - Layout design, component integration, deployment

### 🔧 **Backend & Analysis Team** (2 Members) 
- **Data Engineer** - Data pipelines, APIs, database, infrastructure
- **Analysis Specialist** - PESTLE/SWOT engines, algorithms, business logic

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
