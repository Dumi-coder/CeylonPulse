"""
LLM-based Data Extraction and Signal Generation
Uses LLM to structure unstructured data and generate signals
"""

import os
import json
from typing import List, Dict, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers library not available. Install with: pip install transformers torch")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("Requests library not available")


class LLMExtractor:
    """LLM-based extractor for structuring data and generating signals"""
    
    def __init__(self, provider: str = 'mistral', model: str = 'mistralai/Mistral-7B-Instruct-v0.2', use_api: bool = True):
        """
        Initialize LLM extractor
        
        Args:
            provider: LLM provider ('mistral' for Mistral 7B)
            model: Model name to use (default: Mistral-7B-Instruct)
            use_api: If True, use Hugging Face Inference API (free), else load model locally
        """
        self.provider = provider
        self.model_name = model
        self.use_api = use_api
        self.tokenizer = None
        self.model = None
        self.api_token = os.getenv('HUGGINGFACE_API_TOKEN', '')
        
        if provider == 'mistral':
            if use_api and REQUESTS_AVAILABLE:
                # Use Hugging Face Inference API (free tier available)
                logger.info("Using Mistral 7B via Hugging Face Inference API")
                self.api_url = f"https://api-inference.huggingface.co/models/{model}"
            elif TRANSFORMERS_AVAILABLE:
                # Load model locally (requires GPU for good performance)
                logger.info(f"Loading Mistral 7B model locally: {model}")
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained(model)
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        device_map="auto" if torch.cuda.is_available() else None
                    )
                    logger.info("Mistral 7B model loaded successfully")
                except Exception as e:
                    logger.error(f"Error loading model locally: {str(e)}")
                    logger.info("Falling back to API mode")
                    self.use_api = True
            else:
                logger.warning("Transformers not available. Install with: pip install transformers torch")
        else:
            logger.warning(f"LLM provider {provider} not supported. Using Mistral 7B.")
    
    def load_signal_categories(self, json_path: str = 'signals_pestel_swot.json') -> Dict:
        """Load signal categories from JSON file"""
        try:
            with open(json_path, 'r') as f:
                signals = json.load(f)
            return signals
        except Exception as e:
            logger.error(f"Error loading signal categories: {str(e)}")
            return []
    
    def extract_signals(self, text: str, title: str = '') -> List[Dict]:
        """
        Extract signals from text using LLM
        
        Args:
            text: Text content to analyze
            title: Title of the article/content
            
        Returns:
            List of extracted signal dictionaries
        """
        if not (self.model or (self.use_api and REQUESTS_AVAILABLE)):
            logger.warning("LLM not available")
            return []
        
        signals = self.load_signal_categories()
        signal_list = [s.get('Signal', '') for s in signals]
        
        prompt = f"""Analyze the following news article/content and extract relevant signals for Sri Lanka situational awareness.

Article Title: {title}
Content: {text[:2000]}

Available Signal Categories:
{json.dumps(signal_list, indent=2)}

For each relevant signal found, provide:
1. Signal category name (must match one from the list)
2. Confidence score (0-1)
3. Key phrases from the text that indicate this signal
4. PESTLE category
5. SWOT category
6. Severity estimate (0-1, where 1 is most severe)

Return the response as a JSON array of objects with these fields:
- signal_name
- confidence
- key_phrases (array)
- pestle_category
- swot_category
- severity_estimate

If no relevant signals are found, return an empty array."""

        try:
            if self.provider == 'mistral':
                if self.use_api and REQUESTS_AVAILABLE:
                    # Use Hugging Face Inference API
                    content = self._call_mistral_api(prompt)
                    extracted_signals = self._parse_llm_response(content)
                elif self.model and self.tokenizer:
                    # Use local model
                    content = self._call_mistral_local(prompt)
                    extracted_signals = self._parse_llm_response(content)
                else:
                    logger.warning("Mistral model not available")
                    return []
            
            # Add metadata to each signal
            for signal in extracted_signals:
                signal['extracted_at'] = datetime.utcnow().isoformat()
                signal['source_title'] = title
                signal['source_text'] = text[:500]  # Store first 500 chars
            
            logger.info(f"Extracted {len(extracted_signals)} signals from content")
            return extracted_signals
            
        except Exception as e:
            logger.error(f"Error extracting signals with LLM: {str(e)}")
            return []
    
    def _call_mistral_api(self, prompt: str) -> str:
        """Call Mistral 7B via Hugging Face Inference API"""
        try:
            headers = {}
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            
            # Format prompt for Mistral Instruct
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
            
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_new_tokens": 1000,
                    "temperature": 0.3,
                    "return_full_text": False
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get('generated_text', '')
                else:
                    content = str(result)
                
                return content
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ""
        except Exception as e:
            logger.error(f"Error calling Mistral API: {str(e)}")
            return ""
    
    def _call_mistral_local(self, prompt: str) -> str:
        """Call Mistral 7B locally using transformers"""
        try:
            # Format prompt for Mistral Instruct
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
            
            # Tokenize
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1000,
                    temperature=0.3,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the response part (after [/INST])
            if "[/INST]" in generated_text:
                content = generated_text.split("[/INST]")[-1].strip()
            else:
                content = generated_text
            
            return content
        except Exception as e:
            logger.error(f"Error calling Mistral locally: {str(e)}")
            return ""
    
    def _parse_llm_response(self, content: str) -> List[Dict]:
        """Parse LLM response to extract signals"""
        try:
            # Try to find JSON in response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                signals = result.get('signals', [])
                if not signals and 'signal' in result:
                    # Single signal
                    signals = [result['signal']]
                return signals if isinstance(signals, list) else []
            else:
                # Try to parse as JSON directly
                result = json.loads(content)
                signals = result.get('signals', [])
                return signals if isinstance(signals, list) else []
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract signal names from text
            logger.warning("Could not parse JSON response, attempting text extraction")
            signals = []
            for signal in self.signals:
                signal_name = signal.get('Signal', '')
                if signal_name.lower() in content.lower():
                    signals.append({
                        'signal_name': signal_name,
                        'confidence': 0.6,
                        'pestle_category': signal.get('PESTLE', ''),
                        'swot_category': signal.get('SWOT', ''),
                        'key_phrases': []
                    })
            return signals
    
    def structure_unstructured_data(self, raw_data: Dict) -> Dict:
        """
        Structure unstructured data using LLM
        
        Args:
            raw_data: Raw data dictionary with title, content, etc.
            
        Returns:
            Structured data dictionary
        """
        if not (self.model or (self.use_api and REQUESTS_AVAILABLE)):
            logger.warning("LLM not available")
            return raw_data
        
        text = f"{raw_data.get('title', '')}\n{raw_data.get('description', '')}\n{raw_data.get('text', '')}"
        
        prompt = f"""Structure the following unstructured news/data into a standardized format.

Raw Data:
{text[:2000]}

Extract and structure:
1. Title (clean and concise)
2. Summary (2-3 sentences)
3. Key entities (people, organizations, locations)
4. Date/time mentioned
5. Category (news type)
6. Location (if mentioned, specific to Sri Lanka)
7. Impact level (low/medium/high)
8. Keywords (5-10 relevant keywords)

Return as JSON with these fields."""
        
        try:
            if self.provider == 'mistral':
                if self.use_api and REQUESTS_AVAILABLE:
                    content = self._call_mistral_api(prompt)
                    # Parse as structured data (not signals)
                    try:
                        import re
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            structured = json.loads(json_match.group())
                        else:
                            structured = json.loads(content)
                    except:
                        structured = {}
                elif self.model and self.tokenizer:
                    content = self._call_mistral_local(prompt)
                    try:
                        import re
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            structured = json.loads(json_match.group())
                        else:
                            structured = json.loads(content)
                    except:
                        structured = {}
                else:
                    structured = {}
            
            # Merge with original data
            structured.update({
                'original_data': raw_data,
                'structured_at': datetime.utcnow().isoformat()
            })
            
            logger.info("Successfully structured unstructured data")
            return structured
            
        except Exception as e:
            logger.error(f"Error structuring data with LLM: {str(e)}")
            return raw_data
    
    def batch_extract(self, articles: List[Dict], use_llm: bool = True) -> List[Dict]:
        """
        Batch extract signals from multiple articles
        
        Args:
            articles: List of article dictionaries
            use_llm: Whether to use LLM (if False, returns empty signals)
            
        Returns:
            List of articles with extracted signals
        """
        results = []
        
        for article in articles:
            if use_llm and (self.model or (self.use_api and REQUESTS_AVAILABLE)):
                text = f"{article.get('title', '')}\n{article.get('description', '')}"
                signals = self.extract_signals(text, article.get('title', ''))
                article['extracted_signals'] = signals
                article['structured_data'] = self.structure_unstructured_data(article)
            else:
                article['extracted_signals'] = []
                article['structured_data'] = article
            
            results.append(article)
        
        logger.info(f"Processed {len(results)} articles")
        return results

