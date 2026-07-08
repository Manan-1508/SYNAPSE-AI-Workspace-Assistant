# SYNAPSE Document Parsing Architecture

The ingestion pipeline maps diverse file formats into compact plaintext representations using modular parser adapters.

## Core Components
- `BaseParser`: An abstract interface enforcing standard boundaries (`parse` and `get_metadata`).
- `TextParser`: Standard flat text reader supporting UTF-8 and CP1252 auto-encodings.
- `PDFParser`: Page-by-page reader integrating `pypdf` with page break tags.
- `DocxParser`: Layout compiler formatting paragraphs and nested tables into clean Markdown formats.
- `ExcelParser`: Workbook reader converting tables to compact token-friendly CSV blocks.
- `ParserManager`: Central factory coordinating mappings and text fallback handlers.
