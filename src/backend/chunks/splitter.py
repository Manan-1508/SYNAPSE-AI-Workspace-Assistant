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
