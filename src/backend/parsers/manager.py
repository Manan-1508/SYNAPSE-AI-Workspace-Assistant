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
