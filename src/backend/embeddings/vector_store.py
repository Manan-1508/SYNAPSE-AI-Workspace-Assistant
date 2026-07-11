import os
from typing import List, Dict, Any, Optional
import chromadb

class VectorStoreManager:
    """
    Manages local document embeddings using ChromaDB vector database.
    """
    def __init__(self, persist_dir: str = "src/backend/data/chroma"):
        self.persist_dir = os.path.abspath(persist_dir)
        # Initialize persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        # Get or create the collection with cosine distance similarity configuration
        self.collection = self.client.get_or_create_collection(
            name="workspace_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def delete_by_file(self, file_path: str):
        """Deletes all chunks associated with a specific file path from the vector store."""
        try:
            self.collection.delete(
                where={"file_path": file_path}
            )
        except Exception as e:
            raise RuntimeError(f"Failed to delete vectors for {file_path}: {str(e)}")
