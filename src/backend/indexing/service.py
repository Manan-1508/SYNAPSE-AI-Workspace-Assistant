import os
import hashlib
from typing import List, Dict, Any, Optional

from src.backend.database.manager import DatabaseManager
from src.backend.embeddings.vector_store import VectorStoreManager
from src.backend.parsers.manager import ParserManager
from src.backend.chunks.splitter import SemanticChunker

class IndexingService:
    """
    Orchestrates document parsing, recursive text splitting, vector indexing,
    and document metadata status updates in SQLite.
    """
    def __init__(self, 
                 db_mgr: DatabaseManager, 
                 vector_mgr: VectorStoreManager, 
                 parser_mgr: ParserManager, 
                 chunker: SemanticChunker):
        self.db_mgr = db_mgr
        self.vector_mgr = vector_mgr
        self.parser_mgr = parser_mgr
        self.chunker = chunker

    def _calculate_hash(self, file_path: str) -> str:
        """Computes the SHA-256 hash of a local file to check for content updates."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            raise IOError(f"Failed to read file hash for {file_path}: {str(e)}")
