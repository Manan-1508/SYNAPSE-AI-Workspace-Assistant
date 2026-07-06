import os
from typing import Dict, Any
from src.backend.parsers.base import BaseParser

class DocxParser(BaseParser):
    """
    Parses Microsoft Word (.docx) files using python-docx.
    """

    def parse(self, file_path: str) -> str:
        """Extracts text from the Word document."""
        return ""

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts basic metadata from the Word file."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": "docx"
        }
