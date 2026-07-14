from typing import List, Dict, Any, Optional

class BasePromptTemplate:
    """
    Base prompt layout formatter.
    """
    def format(self, **kwargs) -> str:
        raise NotImplementedError

class ContextPromptTemplate(BasePromptTemplate):
    """
    Formats context chunks and user query into a clean prompt string for RAG ingestion.
    """
    def __init__(self, template: Optional[str] = None):
        self.template = template or (
            "You are a helpful coding assistant named SYNAPSE.\n"
            "Use the following pieces of context to answer the user request. "
            "If you don't know the answer, say so.\n\n"
            "=== CONTEXT START ===\n"
            "{context}\n"
            "=== CONTEXT END ===\n\n"
            "User Request: {query}\n"
            "Response:"
        )

    def format(self, query: str, chunks: List[str]) -> str:
        context_str = "\n---\n".join(chunks)
        return self.template.format(context=context_str, query=query)

class GuidelinesPromptTemplate(BasePromptTemplate):
    """
    Formats system instructions injecting custom workspace guidelines.
    """
    def __init__(self, template: Optional[str] = None):
        self.template = template or (
            "You are a workspace assistant named SYNAPSE.\n"
            "Enforce the following guidelines during interaction:\n"
            "{guidelines}\n"
            "Focus on assisting the user with workspace directories."
        )

    def format(self, guidelines: List[str]) -> str:
        guidelines_str = "\n".join(f"- {g}" for g in guidelines)
        return self.template.format(guidelines=guidelines_str)
