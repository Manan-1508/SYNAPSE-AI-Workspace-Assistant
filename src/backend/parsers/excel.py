import os
from typing import Dict, Any
from src.backend.parsers.base import BaseParser

class ExcelParser(BaseParser):
    """
    Parses Excel (.xlsx, .xls) and CSV files using pandas.
    """

    def parse(self, file_path: str) -> str:
        """Extracts text from Excel or CSV files."""
        return ""

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts basic metadata from the spreadsheet file."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": os.path.splitext(file_path)[1].lstrip(".").lower() or "csv"
        }
