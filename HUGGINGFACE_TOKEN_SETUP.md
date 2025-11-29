# Hugging Face Token Setup

Your Hugging Face read access token has been configured! 🎉

## ✅ Token Configured

Your token: `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`

This token provides:
- ✅ Better rate limits (more requests per hour)
- ✅ Faster API responses
- ✅ More reliable access to Mistral 7B

## 📍 Where It's Configured

### 1. Colab Notebook
The token is set in `CeylonPulse_DataCollection.ipynb` (Cell 13)

**Current setup:**
```python
HUGGINGFACE_API_TOKEN = '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'
```

### 2. Local Environment
The token is in `.env` file (for local runs)

**To use:**
```bash
# Load environment variables
source .env  # or use python-dotenv
python run_collector.py
```

### 3. Environment Variable
You can also set it as an environment variable:

```bash
export HUGGINGFACE_API_TOKEN='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'
python run_collector.py
```

## 🔒 Security Note

**Important:** The token is currently visible in the code. For better security:

### Option 1: Use Colab Secrets (Recommended for Colab)

1. In Colab, click the 🔑 icon (Secrets)
2. Add a new secret:
   - Name: `HUGGINGFACE_API_TOKEN`
   - Value: `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`
3. Update notebook cell:
   ```python
   from google.colab import userdata
   HUGGINGFACE_API_TOKEN = userdata.get('HUGGINGFACE_API_TOKEN', '')
   ```

### Option 2: Use .env File (Recommended for Local)

The `.env` file is already created. Make sure it's in `.gitignore`:

```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

### Option 3: Remove from Notebook

For Colab, you can remove the token from the notebook and use Colab secrets instead.

## ✅ Verification

### Test in Colab:

```python
# Test token works
import requests

HUGGINGFACE_API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
payload = {
    "inputs": "<s>[INST] Say hello [/INST]",
    "parameters": {"max_new_tokens": 50}
}

response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ Token works!")
    print(response.json())
else:
    print(f"❌ Error: {response.text}")
```

### Test Locally:

```bash
# Set token and test
export HUGGINGFACE_API_TOKEN='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'
python -c "
from src.llm_extraction.llm_extractor import LLMExtractor
extractor = LLMExtractor(provider='mistral', use_api=True)
signals = extractor.extract_signals('Fuel shortage in Colombo', 'Test')
print(f'✅ Extracted {len(signals)} signals')
"
```

## 📊 Benefits

With the token, you get:

| Feature | Without Token | With Token |
|---------|--------------|------------|
| Rate Limit | ~30 req/hour | ~1000 req/hour |
| Response Time | Slower | Faster |
| Reliability | Lower | Higher |
| Model Loading | Slower | Faster |

## 🚀 Next Steps

1. **Test the token** - Run the verification code above
2. **Use in Colab** - Token is already in the notebook
3. **Use locally** - Load from `.env` file
4. **Improve security** - Move to Colab secrets or environment variables

## 🔧 Troubleshooting

### Issue: "Invalid token"
- **Check**: Token is correct (no extra spaces)
- **Solution**: Copy token exactly as provided

### Issue: "Token not found"
- **Check**: Environment variable is set
- **Solution**: Use `os.getenv('HUGGINGFACE_API_TOKEN')` or set directly

### Issue: "Rate limit still exceeded"
- **Check**: Token is being used in requests
- **Solution**: Verify headers include `Authorization: Bearer {token}`

## 📝 Token Management

Your token is a **read-only** token, which is perfect for inference.

**To manage your token:**
1. Visit: https://huggingface.co/settings/tokens
2. View all your tokens
3. Revoke if needed
4. Create new tokens

**Token type:** Read (sufficient for API inference)

---

**Your system is now configured with the Hugging Face token!** 🎉

The token will be used automatically when:
- Running the Colab notebook
- Running `run_collector.py` (if .env is loaded)
- Using `LLMExtractor` with `use_api=True`

Enjoy better API access! 🚀

