# Mistral 7B Setup Guide

CeylonPulse now uses **Mistral 7B Instruct** instead of OpenAI - it's **FREE**! 🎉

## Why Mistral 7B?

- ✅ **100% Free** - No API costs
- ✅ **Open Source** - No vendor lock-in
- ✅ **High Quality** - Excellent instruction following
- ✅ **Privacy** - Can run locally or via free API

## Setup Options

### Option 1: Hugging Face Inference API (Recommended for Colab)

**Free tier available!** No credit card required.

1. **Get a free API token** (optional but recommended):
   - Go to https://huggingface.co/settings/tokens
   - Create a free account
   - Generate a new token
   - Copy the token

2. **Set the token**:
   ```python
   import os
   os.environ['HUGGINGFACE_API_TOKEN'] = 'your_token_here'
   ```

3. **That's it!** The code will automatically use the API.

**Note**: First request may take 30-60 seconds (model loading), subsequent requests are fast.

### Option 2: Run Locally (Advanced)

If you have a GPU and want to run the model locally:

```python
from src.llm_extraction.llm_extractor import LLMExtractor

# Load model locally (requires GPU)
extractor = LLMExtractor(
    provider='mistral',
    model='mistralai/Mistral-7B-Instruct-v0.2',
    use_api=False  # Load locally
)
```

**Requirements**:
- GPU with 8GB+ VRAM (or use CPU, but slower)
- ~14GB disk space for model
- Install: `pip install transformers torch accelerate`

### Option 3: Google Colab (Free GPU!)

Colab provides free GPU access:

1. Upload the notebook
2. Enable GPU: Runtime → Change runtime type → GPU
3. The notebook will automatically use Mistral 7B

## Usage

### In Python Code

```python
from src.llm_extraction.llm_extractor import LLMExtractor

# Initialize (uses API by default)
extractor = LLMExtractor(provider='mistral', use_api=True)

# Extract signals
signals = extractor.extract_signals(
    text="Fuel shortage reported in Colombo...",
    title="Fuel Crisis"
)
```

### In Colab Notebook

The notebook is already configured! Just run the cells.

## API Limits

**Hugging Face Free Tier**:
- ✅ Unlimited requests (with rate limiting)
- ✅ No credit card required
- ⚠️ First request may be slow (model loading)
- ⚠️ Rate limits apply (but generous)

**To avoid rate limits**:
- Use an API token (recommended)
- Add small delays between requests
- Consider running locally for high-volume

## Troubleshooting

### "Model is loading" error
- **Solution**: Wait 30-60 seconds and try again. First request loads the model.

### "Rate limit exceeded"
- **Solution**: 
  - Add delays between requests
  - Use an API token (higher limits)
  - Consider running locally

### "Out of memory" (local)
- **Solution**: 
  - Use `use_api=True` instead
  - Or use a smaller model variant
  - Or use CPU (slower but works)

### Slow responses
- **Solution**: 
  - First request is always slow (model loading)
  - Subsequent requests are faster
  - Consider batching requests

## Model Information

- **Model**: `mistralai/Mistral-7B-Instruct-v0.2`
- **Size**: ~14GB
- **Type**: Instruction-tuned LLM
- **License**: Apache 2.0 (commercial use allowed)

## Cost Comparison

| Provider | Cost per 1M tokens | Free Tier |
|----------|-------------------|-----------|
| OpenAI GPT-4 | ~$30 | ❌ |
| OpenAI GPT-3.5 | ~$2 | ❌ |
| **Mistral 7B (HF API)** | **$0** | ✅ |
| **Mistral 7B (Local)** | **$0** | ✅ |

**Savings**: 100% free! 💰

## Next Steps

1. Run the Colab notebook
2. Test signal extraction
3. Enjoy free LLM-powered analysis!

For questions, check the main README or open an issue.

