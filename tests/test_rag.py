import os
import sys
import shutil
from unittest.mock import MagicMock, patch

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.database.manager import DatabaseManager
from src.backend.embeddings.vector_store import VectorStoreManager
from src.backend.llm.ollama import OllamaClient
from src.backend.llm.rag import RagOrchestrator

def main():
    print("=== Testing RAG Orchestration Ingestion & Flow ===")
    
    test_db = "data/test_rag.db"
    test_chroma = "data/test_rag_chroma"
    
    # Fresh test environment state
    for path in [test_db, test_db + "-shm", test_db + "-wal"]:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
    if os.path.exists(test_chroma):
        shutil.rmtree(test_chroma, ignore_errors=True)
        
    db_mgr = DatabaseManager(db_path=test_db)
    vector_mgr = VectorStoreManager(persist_dir=test_chroma)
    
    # Mock OllamaClient completion response
    llm_client = OllamaClient()
    mock_llm_response = "I have reviewed your request. Cosine distance hnsw:space is used."
    llm_client.generate_response = MagicMock(return_value=mock_llm_response)
    
    # 1. Add mock chunks to vector store representing workspace guide
    vector_mgr.add_chunks(
        file_path="C:/workspace/guide.md",
        chunks=["Cosine distance HNSW space configs.", "Local index SQLite databases."]
    )
    
    orchestrator = RagOrchestrator(db_mgr, vector_mgr, llm_client)
    
    try:
        session_id = db_mgr.create_chat_session(title="RAG Test Thread")
        
        # 2. Run RAG Orchestration Flow
        print("Running chat query through RAG Orchestrator...")
        res = orchestrator.generate_chat_response(
            session_id=session_id,
            query="Explain cosine distance space configurations.",
            search_limit=1
        )
        
        print(f"RAG response: {res}")
        assert res["response"] == mock_llm_response
        assert len(res["sources"]) == 1
        assert "guide.md" in res["sources"][0]["file_path"]
        
        # 3. Assert database logs: user message + assistant response with sources
        messages = db_mgr.get_chat_messages(session_id)
        assert len(messages) == 2
        assert messages[0]["sender"] == "user"
        assert messages[0]["content"] == "Explain cosine distance space configurations."
        assert messages[1]["sender"] == "assistant"
        assert messages[1]["content"] == mock_llm_response
        assert len(messages[1]["sources"]) == 1
        assert "guide.md" in messages[1]["sources"][0]["file_path"]
        
        print("[+] RAG Orchestrator integration tests completed successfully.")
        
    finally:
        # Clean up database files
        for path in [test_db, test_db + "-shm", test_db + "-wal"]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
        if os.path.exists(test_chroma):
            shutil.rmtree(test_chroma, ignore_errors=True)

if __name__ == "__main__":
    main()
