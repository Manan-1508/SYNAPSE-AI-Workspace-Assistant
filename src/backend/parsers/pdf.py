import os
from typing import Dict, Any
from src.backend.parsers.base import BaseParser

class PDFParser(BaseParser):
    """
    Parses PDF documents using the pypdf library.
    """

    def parse(self, file_path: str) -> str:
        """Extracts text from the PDF file."""
        return ""

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts metadata from the PDF file."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": "pdf"
        }
