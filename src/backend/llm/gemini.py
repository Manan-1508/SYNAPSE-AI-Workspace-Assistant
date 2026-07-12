from typing import List, Dict, Any, Optional
from src.backend.llm.base import BaseLLMClient

class GeminiClient(BaseLLMClient):
    """
    Client for Google Gemini API services.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7, max_tokens: Optional[int] = None):
        super().__init__(temperature, max_tokens)
        self.model_name = model_name
