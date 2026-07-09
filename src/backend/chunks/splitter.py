from typing import List

class SemanticChunker:
    """
    Splits text into chunks of defined sizes with configured overlap.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """Splits input text into chunks, using a sliding window to incorporate character overlap."""
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Slide step forward, stepping back by overlap characters
            start = end - self.chunk_overlap
            
            # Guard conditions to prevent infinite loops on boundary errors
            if self.chunk_overlap >= self.chunk_size:
                start = end
            if end >= text_len:
                break
                
        return chunks
