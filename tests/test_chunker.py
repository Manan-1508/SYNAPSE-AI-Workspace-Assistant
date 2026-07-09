import os
import sys

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.chunks.splitter import SemanticChunker

def main():
    print("=== Testing Document Chunker (Fixed-Size Characters) ===")
    
    # 100 character sample string
    sample_text = "0123456789" * 10 
    assert len(sample_text) == 100
    
    # Test splitting with chunk_size=30, chunk_overlap=10
    chunker = SemanticChunker(chunk_size=30, chunk_overlap=10)
    chunks = chunker.split_text(sample_text)
    
    print("Generated Chunks:")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i + 1}: len={len(chunk)}: '{chunk}'")
        
    # Assertions checking overlap alignment bounds
    assert len(chunks) == 5
    assert chunks[0] == sample_text[0:30]
    assert chunks[1] == sample_text[20:50]
    assert chunks[2] == sample_text[40:70]
    assert chunks[3] == sample_text[60:90]
    assert chunks[4] == sample_text[80:100]
    
    print("[+] Fixed-size character splitting with overlaps verified successfully.")

if __name__ == "__main__":
    main()
