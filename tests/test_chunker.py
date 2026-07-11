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

    # 2. Test Recursive Semantic Splitting Mock Variables
    print("\n=== Testing Recursive Semantic Splitting ===")
    paragraph_text = (
        "This is paragraph number one. It contains two sentences.\n\n"
        "Here is paragraph number two. It is slightly longer and contains details. "
        "We want to ensure that paragraphs split cleanly without cutting sentences."
    )

    # Split on paragraph boundaries (chunk_size=160, chunk_overlap=0)
    rec_chunker = SemanticChunker(chunk_size=160, chunk_overlap=0)
    rec_chunks = rec_chunker.split_text(paragraph_text)
    
    print("Recursive Paragraph Chunks:")
    for i, chunk in enumerate(rec_chunks):
        print(f"  Chunk {i + 1}: len={len(chunk)}: '{chunk}'")
        
    assert len(rec_chunks) == 2
    assert "paragraph number one" in rec_chunks[0]
    assert "paragraph number two" in rec_chunks[1]

    # Split on sentence boundaries (chunk_size=80, chunk_overlap=15)
    sentence_chunker = SemanticChunker(chunk_size=80, chunk_overlap=15)
    sentence_chunks = sentence_chunker.split_text(paragraph_text)
    
    print("\nRecursive Sentence Chunks:")
    for i, chunk in enumerate(sentence_chunks):
        print(f"  Chunk {i + 1}: len={len(chunk)}: '{chunk}'")
        
    # Verify that punctuation is preserved
    for chunk in sentence_chunks:
        assert chunk.endswith(".") or chunk.endswith("sentences.") or chunk.strip().endswith("sentences")
        
    print("[+] Recursive sentence boundary checks passed.")

if __name__ == "__main__":
    main()
