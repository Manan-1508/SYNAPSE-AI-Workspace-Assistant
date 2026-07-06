import os
from typing import Dict, Any
from docx import Document
from src.backend.parsers.base import BaseParser

class DocxParser(BaseParser):
    """
    Parses Microsoft Word (.docx) files using python-docx.
    """

    def parse(self, file_path: str) -> str:
        """Extracts text from the Word document paragraphs."""
        try:
            doc = Document(file_path)
            paragraphs_text = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs_text)
        except Exception as e:
            raise RuntimeError(f"Failed to parse Word document {file_path}: {str(e)}")

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts basic metadata from the Word file."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": "docx"
        }
