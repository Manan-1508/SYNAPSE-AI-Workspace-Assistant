from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMClient(ABC):
    """
    Abstract base interface for interacting with LLM models.
    """
    def __init__(self, temperature: float = 0.7, max_tokens: Optional[int] = None):
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def generate_response(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generates text completion based on prompt."""
        pass
