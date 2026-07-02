from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    Defines the standard interface for text extraction and metadata parsing.
    """

    @abstractmethod
    def parse(self, file_path: str) -> str:
        """
        Extracts all textual content from the document.
        
        Args:
            file_path: The absolute path to the file.
            
        Returns:
            The extracted text as a single string.
        """
        pass

    @abstractmethod
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extracts structural and system metadata from the document.
        
        Args:
            file_path: The absolute path to the file.
            
        Returns:
            A dictionary containing metadata key-value pairs.
        """
        pass
