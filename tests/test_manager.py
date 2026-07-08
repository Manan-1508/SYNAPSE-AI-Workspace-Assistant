import os
import sys

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.parsers.manager import ParserManager
from src.backend.parsers.text import TextParser
from src.backend.parsers.pdf import PDFParser
from src.backend.parsers.docx import DocxParser
from src.backend.parsers.excel import ExcelParser

def main():
    print("=== Testing ParserManager Factory ===")
    
    manager = ParserManager()
    
    # 1. Verify standard file extensions map to correct parser classes
    assert isinstance(manager.get_parser("doc.txt"), TextParser)
    assert isinstance(manager.get_parser("doc.md"), TextParser)
    assert isinstance(manager.get_parser("doc.pdf"), PDFParser)
    assert isinstance(manager.get_parser("doc.docx"), DocxParser)
    assert isinstance(manager.get_parser("doc.xlsx"), ExcelParser)
    assert isinstance(manager.get_parser("doc.csv"), ExcelParser)
    
    # 2. Verify fallback logic for unhandled extensions (defaults to TextParser)
    assert isinstance(manager.get_parser("doc.unsupported_ext"), TextParser)
    
    # 3. Verify native support check flags
    assert manager.is_supported("doc.pdf") is True
    assert manager.is_supported("doc.unsupported_ext") is False
    
    print("[+] ParserManager extension checks passed successfully.")

if __name__ == "__main__":
    main()
