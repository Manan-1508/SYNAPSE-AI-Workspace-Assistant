import os
from typing import List, Dict, Any, Optional
import chromadb
from sentence_transformers import SentenceTransformer

class VectorStoreManager:
    """
    Manages local document embeddings using ChromaDB vector database.
    Integrates SentenceTransformers for encoding text chunks locally.
    """
    def __init__(self, persist_dir: str = "src/backend/data/chroma", model_name: str = "all-MiniLM-L6-v2"):
        self.persist_dir = os.path.abspath(persist_dir)
        self.model_name = model_name
        self._model: Optional[SentenceTransformer] = None
        
        # Initialize persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        # Get or create the collection with cosine distance similarity configuration
        self.collection = self.client.get_or_create_collection(
            name="workspace_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def _get_model(self) -> SentenceTransformer:
        """Lazy loads the SentenceTransformer model on the CPU for safety."""
        if self._model is None:
            # Force CPU execution to prevent Torch VRAM allocations on integrated GPUs
            self._model = SentenceTransformer(self.model_name, device="cpu")
        return self._model

    def delete_by_file(self, file_path: str):
        """Deletes all chunks associated with a specific file path from the vector store."""
        try:
            self.collection.delete(
                where={"file_path": file_path}
            )
        except Exception as e:
            raise RuntimeError(f"Failed to delete vectors for {file_path}: {str(e)}")
