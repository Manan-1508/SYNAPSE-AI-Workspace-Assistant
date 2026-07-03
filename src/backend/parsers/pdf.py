import os
from typing import Dict, Any
from pypdf import PdfReader
from src.backend.parsers.base import BaseParser

class PDFParser(BaseParser):
    """
    Parses PDF documents using the pypdf library.
    """

    def parse(self, file_path: str) -> str:
        """Extracts text from the PDF file by reading page by page."""
        try:
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n".join(text_parts)
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF {file_path}: {str(e)}")

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts metadata from the PDF file."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": "pdf"
        }
