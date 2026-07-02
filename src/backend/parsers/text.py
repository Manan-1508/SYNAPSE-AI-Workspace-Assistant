import os
from typing import Dict, Any
from src.backend.parsers.base import BaseParser

class TextParser(BaseParser):
    """
    Parses standard plain text and markdown documents.
    """

    def parse(self, file_path: str) -> str:
        """Reads document content assuming UTF-8 encoding."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts basic OS-level metadata."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": "txt"
        }
