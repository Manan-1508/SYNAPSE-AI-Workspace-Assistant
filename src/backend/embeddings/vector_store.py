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
        # Get or create the workspace documents collection
        self.collection = self.client.get_or_create_collection(
            name="workspace_documents"
        )
