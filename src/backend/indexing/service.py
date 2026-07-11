import os
from typing import List, Dict, Any, Optional

class IndexingService:
    """
    Orchestrates document parsing, recursive text splitting, vector indexing,
    and document metadata status updates in SQLite.
    """
    def __init__(self, db_mgr, vector_mgr, parser_mgr, chunker):
        self.db_mgr = db_mgr
        self.vector_mgr = vector_mgr
        self.parser_mgr = parser_mgr
        self.chunker = chunker
