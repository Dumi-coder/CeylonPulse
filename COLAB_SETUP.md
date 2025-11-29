# Google Colab Setup Guide for CeylonPulse

This guide explains how to use CeylonPulse data collection in Google Colab.

## Quick Start

1. **Open the Notebook**
   - Upload `CeylonPulse_DataCollection.ipynb` to Google Colab
   - Or use the Colab link if shared

2. **Set Up API Keys (Optional)**
   - Go to Colab Settings → Secrets
   - Add your API keys:
     - `OPENAI_API_KEY` (for LLM extraction)
     - `TWITTER_BEARER_TOKEN` (for Twitter API)
   - Or set them directly in the notebook (less secure)

3. **Run the Cells**
   - Execute cells sequentially
   - The notebook will:
     - Install dependencies
     - Collect data from all sources
     - Detect signals using keyword matching
     - Optionally use LLM for extraction
     - Save data to JSON

## Features

### ✅ Three Data Collection Methods

1. **Scraping**
   - RSS feeds (Ada Derana, EconomyNext)
   - Web scraping (government sites, news)

2. **API Responses**
   - Google Trends (trending searches)
   - Twitter API (if token provided)

3. **LLM Extraction**
   - OpenAI/Anthropic for signal extraction
   - Structures unstructured data

### ✅ Signal Detection

- **40 PESTLE signals** from SSD
- Keyword-based detection
- LLM-based extraction (optional)
- Confidence scoring

### ✅ TensorFlow Ready

- Text preprocessing
- Data prepared for ML models
- Ready for Step 4-6 (Deep Learning models)

## Data Output

- **JSON file**: All collected data
- **DataFrame**: For analysis
- **Processed text**: Ready for TensorFlow

## Next Steps

After data collection, you can:

1. **Train Models** (Step 4-6)
   - Signal Classification (BERT)
   - Sentiment Analysis (LSTM)
   - Severity Prediction (DNN)
   - Trend Forecasting (LSTM/GRU)

2. **NLP Pipeline** (Step 3)
   - Tokenization
   - Embeddings (SBERT)
   - Clustering (HDBSCAN)

3. **Event Detection** (Step 8)
   - Aggregate signals
   - Filter duplicates
   - Generate events

## Tips

- **Save to Drive**: Mount Google Drive to persist data
- **GPU**: Enable GPU runtime for TensorFlow models
- **Scheduling**: Use Colab Pro for scheduled runs
- **API Limits**: Be mindful of API rate limits

## Troubleshooting

- **Import Errors**: Make sure all cells run in order
- **API Errors**: Check API keys are set correctly
- **Memory Issues**: Use smaller batches or Colab Pro
- **Scraping Errors**: Some sites may block scrapers

## Resources

- [Colab Documentation](https://colab.research.google.com/)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- Project Workflow: `Workflow.md`
- System Architecture: `SAD.md` and `SAD(with tensorflow).md`

