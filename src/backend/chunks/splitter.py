from typing import List

class SemanticChunker:
    """
    Splits text into chunks of defined sizes with configured overlap.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """Splits input text into fixed-size chunks by character length limits."""
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            # Squeeze chunk to defined size
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Slide step forward without overlap for now
            start = end
            
        return chunks
