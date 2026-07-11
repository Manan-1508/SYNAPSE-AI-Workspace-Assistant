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

    def index_file(self, file_path: str) -> Dict[str, Any]:
        """Indexes a single file by parsing, chunking, and encoding its content."""
        file_path = os.path.abspath(file_path)
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}", "file_path": file_path}
            
        file_size = os.path.getsize(file_path)
        file_hash = self._calculate_hash(file_path)
        
        # Check for incremental updates: skip if hash and status are unchanged
        existing = self.db_mgr.get_file(file_path)
        if existing and existing["file_hash"] == file_hash and existing["status"] == "indexed":
            return {"status": "skipped", "message": "File is already indexed and up to date.", "file_path": file_path}
            
        # Register file entry in SQLite (wipes old status/errors)
        self.db_mgr.register_file(file_path, file_hash, file_size)
        self.db_mgr.update_file_status(file_path, "indexing")
        
        try:
            # 1. Parse document text content
            parser = self.parser_mgr.get_parser(file_path)
            content = parser.parse(file_path)
            
            # 2. Segment document text into semantic chunks
            chunks = self.chunker.split_text(content)
            
            # 3. Clean existing vectors from database to avoid duplicates
            self.vector_mgr.delete_by_file(file_path)
            
            # 4. Generate embeddings and index chunks in ChromaDB
            self.vector_mgr.add_chunks(file_path, chunks)
            
            # 5. Commit status as indexed in SQLite DB on success
            self.db_mgr.update_file_status(file_path, "indexed", chunk_count=len(chunks))
            return {"status": "success", "chunk_count": len(chunks), "file_path": file_path}
        except Exception as e:
            # Commit status as failed in SQLite DB on error
            self.db_mgr.update_file_status(file_path, "failed", error_message=str(e))
            return {"status": "error", "message": str(e), "file_path": file_path}
