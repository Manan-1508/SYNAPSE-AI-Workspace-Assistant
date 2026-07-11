from typing import List

class SemanticChunker:
    """
    Splits text into chunks of defined sizes with configured overlap.
    Supports recursive splitting on paragraphs, sentences, and words to maintain semantic coherence.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Define hierarchical separators from largest (paragraphs) to smallest (characters)
        self.separators = ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        """Splits input text into semantic chunks recursively."""
        return self._recursive_split(text, self.separators)

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        """Recursively splits text based on hierarchical delimiters."""
        text = text.strip()
        if not text:
            return []
            
        if len(text) <= self.chunk_size:
            return [text]
            
        if not separators:
            # Fallback to fixed-size slicing if no separators remain
            chunks = []
            for i in range(0, len(text), self.chunk_size):
                chunks.append(text[i:i + self.chunk_size])
            return chunks
            
        separator = separators[0]
        splits = text.split(separator)
        
        chunks = []
        current_chunk = ""
        
        for split in splits:
            if not split.strip():
                continue
            
            if len(split) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                # Recursively split large segments with the next separator
                chunks.extend(self._recursive_split(split, separators[1:]))
            elif len(current_chunk) + len(split) + len(separator) <= self.chunk_size:
                current_chunk += (separator if current_chunk else "") + split
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = split
                
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
