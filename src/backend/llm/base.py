from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMClient(ABC):
    """
    Abstract base interface for interacting with LLM models.
    """
    @abstractmethod
    def generate_response(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generates text completion based on prompt."""
        pass
