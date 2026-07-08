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
    txt_metadata = p_txt.get_metadata(txt_path)
    print(f"[+] Text Parsing verification:\n{txt_content.strip()}")
    print(f"[+] Text Metadata verification:\n{txt_metadata}")
    assert "UTF8 context" in txt_content
    assert txt_metadata["line_count"] == 2
    
    # 2. Verify PDF parsing via mocked Reader
    pdf_path = "tests/unified_doc.pdf"
    mock_pdf = MagicMock()
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Page content in PDF format."
    mock_pdf.pages = [mock_page]
    mock_pdf.metadata = {"/Title": "Mock PDF", "/Author": "Tester"}
    
    with patch("src.backend.parsers.pdf.PdfReader", return_value=mock_pdf):
        with open(pdf_path, "w") as f:
            f.write("")
        p_pdf = manager.get_parser(pdf_path)
        pdf_content = p_pdf.parse(pdf_path)
        pdf_metadata = p_pdf.get_metadata(pdf_path)
        print(f"[+] PDF Parsing verification:\n{pdf_content.strip()}")
        print(f"[+] PDF Metadata verification:\n{pdf_metadata}")
        assert "Page content" in pdf_content
        assert pdf_metadata["page_count"] == 1
        assert pdf_metadata["author"] == "Tester"

    # 3. Verify Word DOCX parsing via mocked Document
    docx_path = "tests/unified_doc.docx"
    mock_docx = MagicMock()
    p_mock = MagicMock()
    p_mock.text = "Docx paragraph content text."
    mock_docx.paragraphs = [p_mock]
    mock_docx.tables = []
    
    mock_props = MagicMock()
    mock_props.title = "Mock Word Document"
    mock_props.author = "Developer"
    mock_props.category = ""
    mock_props.comments = ""
    mock_props.created = None
    mock_props.modified = None
    mock_docx.core_properties = mock_props
    
    with patch("src.backend.parsers.docx.Document", return_value=mock_docx):
        with open(docx_path, "w") as f:
            f.write("")
        p_docx = manager.get_parser(docx_path)
        docx_content = p_docx.parse(docx_path)
        docx_metadata = p_docx.get_metadata(docx_path)
        print(f"[+] DOCX Parsing verification:\n{docx_content.strip()}")
        print(f"[+] DOCX Metadata verification:\n{docx_metadata}")
        assert "docx paragraph" in docx_content.lower()
        assert docx_metadata["title"] == "Mock Word Document"
        
    # Clean up test files
    for path in [txt_path, pdf_path, docx_path]:
        if os.path.exists(path):
            os.remove(path)
            
    # 4. Verify spreadsheet metadata parsing
    csv_path = "tests/unified_sheet.csv"
    mock_df = pd.DataFrame({"Col1": [1, 2], "Col2": ["A", "B"]})
    
    with patch("pandas.read_csv", return_value=mock_df):
        with open(csv_path, "w") as f:
            f.write("")
        p_excel = manager.get_parser(csv_path)
        excel_metadata = p_excel.get_metadata(csv_path)
        print(f"[+] Spreadsheet Metadata verification:\n{excel_metadata}")
        assert excel_metadata["file_type"] == "csv"
        
    if os.path.exists(csv_path):
        os.remove(csv_path)
        
    print("\n=== All unified verification checks passed successfully ===")

if __name__ == "__main__":
    main()
