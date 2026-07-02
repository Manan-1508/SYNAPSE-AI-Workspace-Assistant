import os
import sys

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.parsers.text import TextParser

def main():
    print("=== Testing BaseParser & TextParser ===")
    
    # 1. Create a mock UTF-8 plain text file
    utf8_path = "tests/mock_utf8.txt"
    with open(utf8_path, "w", encoding="utf-8") as f:
        f.write("Line 1: Hello from SYNAPSE.\nLine 2: Semantic text parsing test.\nLine 3: Finished.")
        
    # 2. Create a mock CP1252 (Windows-1252) text file
    cp1252_path = "tests/mock_cp1252.txt"
    with open(cp1252_path, "w", encoding="cp1252") as f:
        f.write("Line 1: Specially characters test: £, ¥, ©.\nLine 2: Windows encoding.")

    parser = TextParser()
    
    # Test UTF-8 parsing
    print("\nTesting UTF-8 Text Parsing...")
    content_utf8 = parser.parse(utf8_path)
    metadata_utf8 = parser.get_metadata(utf8_path)
    
    print(f"Content:\n{content_utf8}")
    print(f"Metadata: {metadata_utf8}")
    
    assert "SYNAPSE" in content_utf8
    assert metadata_utf8["line_count"] == 3
    assert metadata_utf8["word_count"] == 14
    
    # Test CP1252 parsing
    print("\nTesting CP1252 Text Parsing...")
    content_cp1252 = parser.parse(cp1252_path)
    metadata_cp1252 = parser.get_metadata(cp1252_path)
    
    print(f"Content:\n{content_cp1252}")
    print(f"Metadata: {metadata_cp1252}")
    
    assert "£" in content_cp1252
    assert metadata_cp1252["line_count"] == 2
    
    # Clean up test files
    for path in [utf8_path, cp1252_path]:
        if os.path.exists(path):
            os.remove(path)
            
    print("\n=== All parser unit tests passed! ===")

if __name__ == "__main__":
    main()
