import os
import sys
import shutil

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.database.manager import DatabaseManager
from src.backend.embeddings.vector_store import VectorStoreManager
from src.backend.parsers.manager import ParserManager
from src.backend.chunks.splitter import SemanticChunker
from src.backend.indexing.service import IndexingService

def main():
    print("=== Running Integration Ingestion & Search verification ===")
    
    test_db = "data/integration_test.db"
    test_chroma = "data/integration_chroma"
    mock_txt = "tests/integration_guide.txt"
    mock_md = "tests/integration_notes.md"
    
    # Clean up test directories
    for path in [test_db, test_db + "-shm", test_db + "-wal", mock_txt, mock_md]:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
    if os.path.exists(test_chroma):
        shutil.rmtree(test_chroma, ignore_errors=True)
        
    # Setup data components
    db_mgr = DatabaseManager(db_path=test_db)
    vector_mgr = VectorStoreManager(persist_dir=test_chroma)
    parser_mgr = ParserManager()
    chunker = SemanticChunker(chunk_size=150, chunk_overlap=20)
    
    service = IndexingService(db_mgr, vector_mgr, parser_mgr, chunker)
    
    # Write mock content to disk
    with open(mock_txt, "w", encoding="utf-8") as f:
        f.write("SYNAPSE is a local AI coding assistant.\nIt uses SQLite to index document files.\n")
    with open(mock_md, "w", encoding="utf-8") as f:
        f.write("Markdown document details:\nChromaDB collections run cosine similarity.\n")
        
    try:
        # Index both documents
        res1 = service.index_file(mock_txt)
        res2 = service.index_file(mock_md)
        assert res1["status"] == "success"
        assert res2["status"] == "success"
        
        # Verify SQLite registration counts
        files = db_mgr.list_files()
        print(f"Registered files: {len(files)}")
        assert len(files) == 2
        
        # Verify ChromaDB counts
        total_chunks = sum(f["chunk_count"] for f in files)
        v_count = vector_mgr.collection.count()
        print(f"Collection count: {v_count}, Total chunk count: {total_chunks}")
        assert v_count == total_chunks

        # Run semantic search queries
        print("\nRunning semantic queries...")
        matches = vector_mgr.search(query="SQLite database indexes", limit=2)
        print(f"Query matches: {matches}")
        assert len(matches) > 0
        assert "sqlite" in matches[0]["text"].lower()
        assert 0.0 <= matches[0]["score"] <= 1.0
        
        # Test file path filtering scope
        filtered_matches = vector_mgr.search(
            query="cosine similarity", 
            limit=2, 
            file_path=mock_md
        )
        print(f"Filtered matches: {filtered_matches}")
        for match in filtered_matches:
            # Resolve to absolute path to verify
            assert os.path.abspath(match["metadata"]["file_path"]) == os.path.abspath(mock_md)
            
        print("\n=== Integration Ingestion & Search verification passed successfully ===")
        
    finally:
        # Clean up files
        for path in [test_db, test_db + "-shm", test_db + "-wal", mock_txt, mock_md]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
        if os.path.exists(test_chroma):
            shutil.rmtree(test_chroma, ignore_errors=True)

if __name__ == "__main__":
    main()
