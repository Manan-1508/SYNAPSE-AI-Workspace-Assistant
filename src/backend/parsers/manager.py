import os
from typing import Dict, Type, Optional
from src.backend.parsers.base import BaseParser
from src.backend.parsers.text import TextParser
from src.backend.parsers.pdf import PDFParser
from src.backend.parsers.docx import DocxParser
from src.backend.parsers.excel import ExcelParser

class ParserManager:
    """
    Factory class that routes document files to their respective BaseParser adapters.
    """
    def __init__(self):
        # Instantiate and register parser instances for specific file extensions
        self._parsers: Dict[str, BaseParser] = {
            ".txt": TextParser(),
            ".md": TextParser(),
            ".markdown": TextParser(),
            ".pdf": PDFParser(),
            ".docx": DocxParser(),
            ".xlsx": ExcelParser(),
            ".xls": ExcelParser(),
            ".csv": ExcelParser()
        }
        # Fallback parser for unsupported extensions (defaults to plain text)
        self._default_parser = TextParser()

    def get_parser(self, file_path: str) -> BaseParser:
        """Retrieves the parser mapped to the file's extension, falling back to the text parser."""
        ext = os.path.splitext(file_path)[1].lower()
        return self._parsers.get(ext, self._default_parser)

    def is_supported(self, file_path: str) -> bool:
        """Returns True if the file type is natively supported."""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self._parsers
