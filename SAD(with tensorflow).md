# 🌟 CeylonPlus: Real-Time Situational Awareness System for Sri Lanka

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)

---

## 🔹 Overview

CeylonPlus is a **real-time situational awareness platform** designed to monitor, classify, and forecast events across Sri Lanka. The system leverages **advanced deep learning**, **natural language processing (NLP)**, and **trend forecasting** to provide actionable insights for stakeholders.

Key capabilities:

- **Signal Classification** (e.g., fuel shortage, floods, protests)  
- **Sentiment Analysis** (Positive / Neutral / Negative)  
- **Event Severity Scoring** (0–1 scale)  
- **Trend Forecasting** (LSTM for signal spikes)  
- **Explainable & Ethical AI insights**  

---

## 🏗️ System Architecture

```text
SCRAPERS → NLP CLEANING → DEEP LEARNING MODELS
                                  ↓
          (Classification / Sentiment / Severity / Forecast)
                                  ↓
                  SHAP/LIME Explainability
                                  ↓
                    EVENT DETECTION ENGINE
                                  ↓
                    PESTLE + SWOT ENGINE
                                  ↓
                         INSIGHTS API
                                  ↓
                          DASHBOARD UI
````

**Components:**

1. **Scrapers & Collectors**

   * News websites, social media, government feeds
   * Real-time and historical data collection

2. **NLP Cleaning**

   * Tokenization, stop-word removal, lemmatization
   * Sinhala, Tamil, English normalization
   * Feature extraction (TF-IDF, embeddings)

3. **Deep Learning Models**

   * **Signal Classification:** Transformer / BERT
   * **Sentiment Analysis:** LSTM / Bi-LSTM
   * **Severity Predictor:** Dense Neural Network (DNN)
   * **Trend Forecasting:** LSTM / GRU

4. **Explainability Layer**

   * SHAP / LIME to explain model predictions
   * Highlights important words/features contributing to predictions

5. **Event Detection Engine**

   * Aggregates classified signals and severity scores
   * Filters duplicates and false alerts

6. **PESTLE + SWOT Engine**

   * Maps events to political, economic, social, technological, legal, environmental factors
   * Provides strategic insights for stakeholders

7. **Insights API**

   * REST API for dashboards or external apps
   * Supports filtering by location, category, severity

8. **Dashboard UI**

   * Interactive map, charts, trend graphs
   * Customizable views for government or corporate users

---

## 🧠 Deep Learning Components

CeylonPlus uses **Deep Learning** for real-time event analysis:

| Model                 | Type                       | Purpose                                        | Deep Learning Details                                        |
| --------------------- | -------------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| Signal Classification | Transformer / BERT         | Classify events into 40+ categories            | Fine-tuned BERT with text embeddings                         |
| Sentiment Analysis    | LSTM / Bi-LSTM             | Detect positive / neutral / negative sentiment | Two-layer LSTM with 128 units, dropout 0.3                   |
| Severity Prediction   | Dense Neural Network (DNN) | Predict severity 0–1                           | 3 fully connected layers, ReLU activation, L2 regularization |
| Trend Forecasting     | LSTM / GRU                 | Predict signal spikes over time                | 2 LSTM layers, look-back window 7 days, dropout 0.2          |

**Deep Learning Features:**

* TensorFlow / Keras backend
* Sequence modeling with **LSTM / GRU** for temporal forecasting
* Transformer-based **BERT** for text classification
* Dropout & L2 regularization to prevent overfitting
* Early stopping & checkpointing during training
* Explainability via **SHAP / LIME**

---

## 🧩 Machine Learning Workflow

### 1. Data Pipeline

* Data Collection → structured database
* Preprocessing → tokenization, embeddings, missing value handling
* Train / Validation / Test split
* Temporal split for time-series models

### 2. Model Training

* Batching, checkpointing, early stopping
* Regularization: Dropout, L2 weight decay
* Optional data augmentation (synonym replacement, back translation)

### 3. Hyperparameter Tuning

* Learning rate, batch size, optimizer (Adam / RMSProp)
* Sequence length, layers, neurons, dropout
* Tools: **Keras Tuner**, **Optuna**
* Strategies: Random Search / Bayesian Optimization

### 4. Evaluation Metrics

| Model                  | Metric   | Score |
| ---------------------- | -------- | ----- |
| Signal Classifier      | F1-score | 0.86  |
| Sentiment Model        | Accuracy | 91%   |
| Severity Predictor     | MAE      | 0.08  |
| Trend Forecasting LSTM | MAPE     | 7.2%  |

---

## 🔍 Explainability & Ethical AI

**Explainability (SHAP / LIME):**

* Highlights which features/words contributed to model predictions
* Example:

```text
Signal: "Protest Event"
Top contributing words: protest, crowd, demonstration, strike
```

**Ethical AI Principles:**

* Bias mitigation: diverse news sources and geographic coverage
* Transparency: explainable ML predictions
* Fairness: no targeting political groups or individuals
* Privacy: only publicly available data
* Safety: risk-focused insights, not political opinions
* Human-in-the-loop: stakeholders interpret insights

---

## ⚙️ Deployment & Tools

* **Backend:** Python, TensorFlow, scikit-learn
* **Database:** PostgreSQL / MongoDB
* **Frontend:** ReactJS / VueJS / D3.js
* **APIs:** REST for dashboard integration
* **Explainability:** SHAP, LIME
* **Hyperparameter Tuning:** Keras Tuner, Optuna

---

## 📂 Folder Structure (Example)

```
CeylonPlus/
│
├─ data/
│   ├─ raw/
│   └─ processed/
├─ notebooks/
│   └─ EDA, preprocessing, experiments.ipynb
├─ models/
│   ├─ classification/
│   ├─ sentiment/
│   ├─ severity/
│   └─ forecasting/
├─ src/
│   ├─ scrapers/
│   ├─ nlp/
│   ├─ ml/
│   ├─ api/
│   └─ dashboard/
├─ tests/
├─ requirements.txt
└─ README.md
```

---

## 🌐 Roadmap / Next Steps

1. Complete full signals table (40+ categories)
2. Integrate real-time scrapers with NLP pipeline
3. Train & evaluate Deep Learning models
4. Deploy models to production
5. Build Insights API & Dashboard
6. Continuous monitoring & hyperparameter tuning
7. Add explainability dashboards for stakeholders

---

## 📌 Key Features

* Real-time collection & processing of multi-source signals
* NLP-powered classification & sentiment detection
* Severity scoring & trend forecasting using **Deep Learning**
* Explainable ML using SHAP / LIME
* Ethical AI principles embedded in design
* Integration with PESTLE & SWOT for strategic insights
* Interactive dashboards for visual monitoring

---

**© 2025 CeylonPlus*
