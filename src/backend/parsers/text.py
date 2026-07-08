import os
from typing import Dict, Any
from src.backend.parsers.base import BaseParser

class TextParser(BaseParser):
    """
    Parses standard plain text and markdown documents.
    Supports auto-detection of multiple encodings (utf-8, cp1252, latin-1) to avoid decode crashes.
    """

    def parse(self, file_path: str) -> str:
        for encoding in ["utf-8", "cp1252", "latin-1"]:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                pass
                
        # Final fallback: read with character replacement handler
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extracts text statistics and system metadata."""
        content = self.parse(file_path)
        
        # Calculate document metrics
        lines = content.splitlines()
        line_count = len(lines)
        word_count = len(content.split())
        char_count = len(content)
        
        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": os.path.splitext(file_path)[1].lstrip(".").lower() or "txt",
            "line_count": line_count,
            "word_count": word_count,
            "character_count": char_count
        }
