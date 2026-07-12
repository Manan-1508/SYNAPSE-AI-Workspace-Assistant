import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from src.backend.llm.base import BaseLLMClient

class GeminiClient(BaseLLMClient):
    """
    Client for Google Gemini API services.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7, max_tokens: Optional[int] = None):
        super().__init__(temperature, max_tokens)
        self.model_name = model_name
        
        # Load API Key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            # Fallback warning instead of crash to facilitate unit testing
            print("Warning: GEMINI_API_KEY environment variable is not set.")

    def generate_response(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generates text completion based on prompt using Gemini models."""
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not configured.")
            
        generation_config = {
            "temperature": self.temperature,
        }
        if self.max_tokens:
            generation_config["max_output_tokens"] = self.max_tokens
            
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config,
                system_instruction=system_instruction
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini generation call failed: {str(e)}")
