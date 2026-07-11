import os
from typing import List, Dict, Any, Optional

class VectorStoreManager:
    """
    Manages local document embeddings using ChromaDB vector database.
    """
    def __init__(self, persist_dir: str = "src/backend/data/chroma"):
        self.persist_dir = persist_dir
