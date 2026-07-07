import os
from typing import Dict, Any
import pandas as pd
from src.backend.parsers.base import BaseParser

class ExcelParser(BaseParser):
    """
    Parses Excel (.xlsx, .xls) and CSV files using pandas.
    """

    def parse(self, file_path: str) -> str:
        """Extracts text from Excel workbooks or CSV files, formatting as clean token-efficient CSV structures."""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in [".xlsx", ".xls"]:
                # Load Excel file to retrieve all sheet names
                excel_file = pd.ExcelFile(file_path)
                sheets_text = []
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    # Clean empty rows and columns to save token window budgets
                    df = df.dropna(how="all").dropna(axis=1, how="all")
                    csv_data = df.to_csv(index=False)
                    sheets_text.append(f"--- SHEET: {sheet_name} ---\n{csv_data.strip()}")
                return "\n\n".join(sheets_text)
            elif ext == ".csv":
                df = pd.read_csv(file_path)
                df = df.dropna(how="all").dropna(axis=1, how="all")
                return df.to_csv(index=False).strip()
            return ""
        except Exception as e:
            raise RuntimeError(f"Failed to parse spreadsheet {file_path}: {str(e)}")

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts basic metadata from the spreadsheet file."""
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": os.path.splitext(file_path)[1].lstrip(".").lower() or "csv"
        }
