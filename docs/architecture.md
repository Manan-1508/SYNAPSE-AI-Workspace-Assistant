# SYNAPSE Document Ingestion & Search Architecture

The ingestion pipeline maps diverse file formats into compact plaintext representations using modular parser adapters, chunks them semantically, and stores their vector embeddings locally.

## Core Components
- `BaseParser`: An abstract interface enforcing standard boundaries (`parse` and `get_metadata`).
- `TextParser`: Standard flat text reader supporting UTF-8 and CP1252 auto-encodings.
- `PDFParser`: Page-by-page reader integrating `pypdf` with page break tags.
- `DocxParser`: Layout compiler formatting paragraphs and nested tables into clean Markdown formats.
- `ExcelParser`: Workbook reader converting tables to compact token-friendly CSV blocks.
- `ParserManager`: Central factory coordinating mappings and text fallback handlers.
- `SemanticChunker`: Recursive semantic text splitter hierarchically targeting paragraphs, sentence delimiters, and word spacing boundaries while retaining sentence punctuations.
- `VectorStoreManager`: ChromaDB client wrapper initializing local persistent stores with cosine distance spaces and sentence-transformers model lazy loaders.
- `IndexingService`: Incremental data indexing service mapping directory walk crawls to parallel SQLite register checks and vector storage additions.
