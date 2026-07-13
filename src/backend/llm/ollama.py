import httpx
import json
from typing import List, Dict, Any, Optional, Generator
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
        """Generates text completion based on prompt using Ollama."""
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }
        if system_instruction:
            payload["system"] = system_instruction
        if self.max_tokens:
            payload["options"]["num_predict"] = self.max_tokens

        try:
            response = httpx.post(url, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            raise RuntimeError(f"Ollama generation call failed: {str(e)}")

    def generate_stream(self, prompt: str, system_instruction: Optional[str] = None) -> Generator[str, None, None]:
        """Streams text token chunks based on prompt using Ollama."""
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.temperature
            }
        }
        if system_instruction:
            payload["system"] = system_instruction
        if self.max_tokens:
            payload["options"]["num_predict"] = self.max_tokens

        try:
            with httpx.stream("POST", url, json=payload, timeout=60.0) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line.strip():
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            yield token
        except Exception as e:
            raise RuntimeError(f"Ollama streaming call failed: {str(e)}")
