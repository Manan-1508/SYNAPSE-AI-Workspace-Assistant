import os
import sys
import shutil
from typing import Dict, Any

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.database.manager import DatabaseManager
from src.backend.embeddings.vector_store import VectorStoreManager
from src.backend.parsers.manager import ParserManager
from src.backend.chunks.splitter import SemanticChunker
from src.backend.indexing.service import IndexingService

def main():
    print("=== Testing IndexingService & Incremental Ingestion ===")
    
    test_db = "data/test_index.db"
    test_chroma = "data/test_chroma"
    mock_file = "tests/mock_index_doc.txt"
    
    # Ensure fresh test states
    for path in [test_db, test_db + "-shm", test_db + "-wal", mock_file]:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
    if os.path.exists(test_chroma):
        shutil.rmtree(test_chroma, ignore_errors=True)
        
    # Setup data orchestrator layers
    db_mgr = DatabaseManager(db_path=test_db)
    vector_mgr = VectorStoreManager(persist_dir=test_chroma)
    parser_mgr = ParserManager()
    chunker = SemanticChunker(chunk_size=100, chunk_overlap=10)
    
    service = IndexingService(db_mgr, vector_mgr, parser_mgr, chunker)
    
    # Create mock document
    with open(mock_file, "w", encoding="utf-8") as f:
        f.write("Line 1: SYNAPSE indexing test document.\n" * 5)
        
    try:
        # Index document first time
        print("Indexing file for the first time...")
        res = service.index_file(mock_file)
        print(f"Index result: {res}")
        assert res["status"] == "success"
        
        # Verify db status transition
        abs_mock_file = os.path.abspath(mock_file)
        record = db_mgr.get_file(abs_mock_file)
        print(f"SQLite Record: path={record['file_path']}, status={record['status']}")
        assert record["status"] == "indexed"
        assert record["chunk_count"] > 0
        
        # Verify vector collection count matches chunk_count
        v_count = vector_mgr.collection.count()
        print(f"Vector Count: {v_count}")
        assert v_count == record["chunk_count"]
        
        # Index document second time (should be skipped!)
        print("\nIndexing file for the second time...")
        res_skipped = service.index_file(mock_file)
        print(f"Index result: {res_skipped}")
        assert res_skipped["status"] == "skipped"
        
    finally:
        # Clean up files
        for path in [test_db, test_db + "-shm", test_db + "-wal", mock_file]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
        if os.path.exists(test_chroma):
            shutil.rmtree(test_chroma, ignore_errors=True)
            
    print("=== Indexing tests passed successfully! ===")

if __name__ == "__main__":
    main()
