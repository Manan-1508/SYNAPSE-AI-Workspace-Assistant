import os
from typing import Dict, Any
import pandas as pd
from src.backend.parsers.base import BaseParser

class ExcelParser(BaseParser):
    """
    Parses Excel (.xlsx, .xls) and CSV files using pandas.
    """

    def parse(self, file_path: str) -> str:
        """Extracts text sheet-by-sheet from Excel files."""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in [".xlsx", ".xls"]:
                # Load Excel file to retrieve all sheet names
                excel_file = pd.ExcelFile(file_path)
                sheets_text = []
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    # Convert dataframe to string representation
                    sheets_text.append(f"--- SHEET: {sheet_name} ---\n{df.to_string(index=False)}")
                return "\n\n".join(sheets_text)
            return ""
        except Exception as e:
            raise RuntimeError(f"Failed to parse Excel workbook {file_path}: {str(e)}")

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts basic metadata from the spreadsheet file."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": os.path.splitext(file_path)[1].lstrip(".").lower() or "csv"
        }
