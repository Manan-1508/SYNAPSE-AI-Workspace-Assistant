from typing import List

class SemanticChunker:
    """
    Splits text into chunks of defined sizes with configured overlap.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """Splits input text into chunk list."""
        return []
