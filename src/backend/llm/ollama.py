import httpx
from typing import List, Dict, Any, Optional
from src.backend.llm.base import BaseLLMClient

class OllamaClient(BaseLLMClient):
    """
    Client for local Ollama service.
    """
    def __init__(self, host: str = "http://localhost:11434", model_name: str = "qwen2.5-coder:1.5b", temperature: float = 0.7, max_tokens: Optional[int] = None):
        super().__init__(temperature, max_tokens)
        self.host = host.rstrip("/")
        self.model_name = model_name

    def check_connection(self) -> bool:
        """Checks if local Ollama service is reachable."""
        try:
            response = httpx.get(f"{self.host}/")
            return response.status_code == 200
        except Exception:
            return False

    def generate_response(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generates text completion based on prompt."""
        return ""
