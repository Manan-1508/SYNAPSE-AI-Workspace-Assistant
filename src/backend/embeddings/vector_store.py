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

    def add_chunks(self, file_path: str, chunks: List[str]):
        """Generates embeddings for text chunks and adds them to the vector store."""
        if not chunks:
            return
            
        model = self._get_model()
        # Generate numerical vector representations for each text segment
        embeddings = model.encode(chunks, convert_to_numpy=True).tolist()
        
        # Construct unique Chroma IDs and matching metadata trackers
        ids = [f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]
        metadatas = [{"file_path": file_path, "chunk_index": i} for i in range(len(chunks))]
        
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=chunks
            )
        except Exception as e:
            raise RuntimeError(f"Failed to add document chunks: {str(e)}")

    def delete_by_file(self, file_path: str):
        """Deletes all chunks associated with a specific file path from the vector store."""
        try:
            self.collection.delete(
                where={"file_path": file_path}
            )
        except Exception as e:
            raise RuntimeError(f"Failed to delete vectors for {file_path}: {str(e)}")

    def search(self, query: str, limit: int = 5, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Searches the vector store, supporting optional metadata filters by file path."""
        model = self._get_model()
        query_embedding = model.encode(query, convert_to_numpy=True).tolist()
        
        where_filter = {}
        if file_path:
            where_filter["file_path"] = os.path.abspath(file_path)
            
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_filter if where_filter else None
            )
            
            formatted = []
            if not results or not results["ids"] or len(results["ids"]) == 0:
                return formatted
                
            ids = results["ids"][0]
            docs = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(ids)
            
            for idx in range(len(ids)):
                # Convert cosine distance to a similarity score between 0.0 and 1.0
                similarity_score = 1.0 - distances[idx]
                formatted.append({
                    "id": ids[idx],
                    "text": docs[idx],
                    "metadata": metadatas[idx],
                    "score": round(similarity_score, 4)
                })
                
            return formatted
        except Exception as e:
            raise RuntimeError(f"Search query failed: {str(e)}")
