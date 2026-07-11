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
