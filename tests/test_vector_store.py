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
    
    # Clean up test directories
    if os.path.exists(test_chroma_dir):
        shutil.rmtree(test_chroma_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
