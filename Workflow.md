# 🌟 CeylonPlus: Real-Time Situational Awareness System for Sri Lanka

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)


---

## 🔹 Overview

CeylonPlus is a **real-time situational awareness platform** designed to monitor, classify, and forecast events across Sri Lanka. The system leverages **Deep Learning**, **Natural Language Processing (NLP)**, and **trend forecasting** to provide actionable insights for stakeholders.

Key capabilities:

- **Signal Classification** (40+ categories)  
- **Sentiment Analysis** (Positive / Neutral / Negative)  
- **Event Severity Scoring** (0–1 scale)  
- **Trend Forecasting** (LSTM for signal spikes)  
- **Explainable & Ethical AI insights**  

---

## 🏗️ Step-by-Step Workflow

### **Step 1 — Define Signal Categories**
1. List all **signal categories** (e.g., fuel shortage, flood, protest, inflation).  
2. Map each signal to **PESTLE & SWOT categories**:
   - Political, Economic, Social, Technological, Legal, Environmental  
   - Strengths, Weaknesses, Opportunities, Threats  
3. Save the signals table in **CSV/JSON** for ML ingestion.

---

### **Step 2 — Data Collection**
- Collect data from:
  - News websites  
  - Social media (Twitter, Facebook)  
  - Government feeds  
- Store raw data in **database** (PostgreSQL / MongoDB).  
- Maintain historical and real-time streams.

---

### **Step 3 — NLP Preprocessing**
- Clean and normalize text:
  - Tokenization  
  - Stop-word removal  
  - Lemmatization  
  - Language normalization (Sinhala, Tamil, English)  
- Feature extraction:
  - TF-IDF vectors  
  - Word embeddings (BERT, FastText)  

---

### **Step 4 — Deep Learning Models**

| Model | Type | Purpose | Deep Learning Details |
|-------|------|---------|--------------------|
| Signal Classification | Transformer / BERT | Classify events | Fine-tuned BERT with embeddings |
| Sentiment Analysis | LSTM / Bi-LSTM | Detect sentiment | 2-layer LSTM, 128 units, dropout 0.3 |
| Severity Prediction | Dense NN | Predict severity 0–1 | 3 fully connected layers, ReLU, L2 regularization |
| Trend Forecasting | LSTM / GRU | Predict signal spikes | 2 LSTM layers, look-back 7 days, dropout 0.2 |

**Deep Learning Features:**
- TensorFlow / Keras backend  
- Sequence modeling for temporal trends (LSTM/GRU)  
- Transformer-based text classification (BERT)  
- Regularization (Dropout, L2), Early Stopping, Checkpoints  
- Optional text augmentation (synonyms, back translation)  

---

### **Step 5 — Model Training Workflow**
1. **Data Splitting**:
   - Train / Validation / Test  
   - Cross-validation for stability  
   - Temporal split for time-series models  
2. **Training**:
   - Mini-batch gradient descent  
   - Early stopping & checkpointing  
   - Dropout & L2 regularization  
3. **Hyperparameter Tuning**:
   - Learning rate, batch size, optimizer selection  
   - Sequence length, layers, neurons, dropout  
   - Tools: Keras Tuner, Optuna  
   - Strategies: Random Search, Bayesian Optimization  

---

### **Step 6 — Model Evaluation**
| Model                  | Metric   | Score  |
|------------------------|---------|--------|
| Signal Classifier      | F1-score | 0.86   |
| Sentiment Model        | Accuracy | 91%    |
| Severity Predictor     | MAE      | 0.08   |
| Trend Forecasting LSTM | MAPE     | 7.2%   |

- Generate **confusion matrices** for classification.  
- Save evaluation metrics for **dashboard display**.  

---

### **Step 7 — Explainability**
- Apply **SHAP / LIME** to all deep learning models.  
- Show **feature importance** for each prediction.  

**Example:**
```text
Signal: "Protest Event"
Top contributing words: protest, crowd, demonstration, strike
````

---

### **Step 8 — Event Detection Engine**

* Aggregate outputs from:

  * Signal Classification
  * Sentiment Analysis
  * Severity Predictor
  * Trend Forecasting
* Filter duplicates and false alerts.
* Assign events to **PESTLE + SWOT categories**.

---

### **Step 9 — Insights API**

* Provide **REST API** for external access.
* Filter insights by:

  * Location
  * Signal category
  * Severity score
* Supports **dashboard integration**.

---

### **Step 10 — Dashboard & Visualization**

* Interactive map showing event locations.
* Trend charts & alert graphs.
* Severity & sentiment indicators.
* SHAP/LIME overlays for **explainable predictions**.

---

### **Step 11 — Ethical AI**

* Bias mitigation: diverse data sources
* Transparency: explainable models
* Fairness: no targeting of political groups or individuals
* Privacy: only publicly available data
* Safety: risk-focused insights, not political opinions
* Human-in-the-loop: stakeholders interpret insights

---

### **Step 12 — Deployment & Monitoring**

* Deploy end-to-end pipeline:

  * Scrapers → NLP → Deep Learning → Explainability → API → Dashboard
* Monitor model performance and update hyperparameters regularly.

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
6. Monitor performance and tune models
7. Enhance explainability dashboards for stakeholders

---

## 📌 Key Features

* Real-time multi-source signal collection
* NLP-powered classification & sentiment detection
* **Deep Learning-based severity scoring & trend forecasting**
* Explainable ML with SHAP / LIME
* Ethical AI principles embedded in design
* PESTLE + SWOT insights for strategic decision-making
* Interactive dashboards with alerts and trends

---

**© 2025 CeylonPlus | MIT License**
