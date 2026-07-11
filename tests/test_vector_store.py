import os
import sys
import shutil

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.embeddings.vector_store import VectorStoreManager

def main():
    print("=== Testing VectorStoreManager & ChromaDB ===")
    
    test_chroma_dir = "data/test_chroma"
    if os.path.exists(test_chroma_dir):
        shutil.rmtree(test_chroma_dir, ignore_errors=True)
        
    db = VectorStoreManager(persist_dir=test_chroma_dir)
    print("[+] ChromaDB persistent client connected successfully.")
    
    # 2. Test mock chunk additions and embedding generations
    print("\nTesting chunk additions and embedding generation...")
    mock_chunks = [
        "SYNAPSE uses local embeddings to run queries.",
        "We enforce sentence-transformers execution on CPU."
    ]
    db.add_chunks("C:/docs/guide.txt", mock_chunks)
    
    # Verify count
    count = db.collection.count()
    print(f"Collection items count: {count}")
    assert count == 2
    
    # Clean up test directories
    if os.path.exists(test_chroma_dir):
        shutil.rmtree(test_chroma_dir, ignore_errors=True)
        
    print("=== Vector store tests passed successfully! ===")

if __name__ == "__main__":
    main()
