import os
import sys
import pandas as pd
from unittest.mock import MagicMock, patch

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.parsers.manager import ParserManager

def main():
    print("=== Running Unified Document Parsers Verification ===")
    manager = ParserManager()
    
    # 1. Verify parsing of plain text and markdown files
    txt_path = "tests/unified_text.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("Line 1: UTF8 context content.\nLine 2: Semantic verification check.")
        
    p_txt = manager.get_parser(txt_path)
    txt_content = p_txt.parse(txt_path)
    print(f"[+] Text Parsing verification:\n{txt_content.strip()}")
    assert "UTF8 context" in txt_content
    
    # 2. Verify PDF parsing via mocked Reader
    pdf_path = "tests/unified_doc.pdf"
    mock_pdf = MagicMock()
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Page content in PDF format."
    mock_pdf.pages = [mock_page]
    mock_pdf.metadata = {"/Title": "Mock PDF"}
    
    with patch("src.backend.parsers.pdf.PdfReader", return_value=mock_pdf):
        with open(pdf_path, "w") as f:
            f.write("")
        p_pdf = manager.get_parser(pdf_path)
        pdf_content = p_pdf.parse(pdf_path)
        print(f"[+] PDF Parsing verification:\n{pdf_content.strip()}")
        assert "Page content" in pdf_content

    # 3. Verify Word DOCX parsing via mocked Document
    docx_path = "tests/unified_doc.docx"
    mock_docx = MagicMock()
    p_mock = MagicMock()
    p_mock.text = "Docx paragraph content text."
    mock_docx.paragraphs = [p_mock]
    mock_docx.tables = []
    mock_docx.core_properties = MagicMock()
    
    with patch("src.backend.parsers.docx.Document", return_value=mock_docx):
        with open(docx_path, "w") as f:
            f.write("")
        p_docx = manager.get_parser(docx_path)
        docx_content = p_docx.parse(docx_path)
        print(f"[+] DOCX Parsing verification:\n{docx_content.strip()}")
        assert "docx paragraph" in docx_content.lower()
        
    # Clean up test files
    for path in [txt_path, pdf_path, docx_path]:
        if os.path.exists(path):
            os.remove(path)
