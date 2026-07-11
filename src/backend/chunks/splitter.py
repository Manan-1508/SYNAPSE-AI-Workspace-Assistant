import re
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
        """Splits input text into semantic chunks recursively, filtering out empty values."""
        raw_chunks = self._recursive_split(text, self.separators)
        # Strip and filter empty chunks
        return [c.strip() for c in raw_chunks if c.strip()]

    def _get_overlap_prefix(self, text: str) -> str:
        """Extracts a suffix from the text that fits within the chunk_overlap size limit."""
        if not text or self.chunk_overlap <= 0:
            return ""
        # Slice characters from the end of the text
        return text[-self.chunk_overlap:]

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
        
        # Use lookbehind assertions for sentence boundary splitting to retain punctuation
        if separator in [". ", "? ", "! "]:
            escaped_sep = re.escape(separator.strip())
            pattern = rf"(?<={escaped_sep})\s+"
            splits = re.split(pattern, text)
        else:
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
            elif len(current_chunk) + len(split) + (len(separator) if separator not in [". ", "? ", "! "] else 1) <= self.chunk_size:
                # Add back space separator for sentence endings, otherwise standard separator
                sep_to_add = " " if separator in [". ", "? ", "! "] else separator
                current_chunk += (sep_to_add if current_chunk else "") + split
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # Start new chunk with overlap suffix from the previous chunk
                overlap_prefix = self._get_overlap_prefix(current_chunk)
                sep_to_add = " " if separator in [". ", "? ", "! "] else separator
                if overlap_prefix:
                    current_chunk = overlap_prefix + (sep_to_add if not overlap_prefix.endswith(sep_to_add) else "") + split
                else:
                    current_chunk = split
                
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
