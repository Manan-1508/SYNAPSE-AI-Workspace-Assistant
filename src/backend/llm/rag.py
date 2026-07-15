from typing import List, Dict, Any, Optional
from src.backend.database.manager import DatabaseManager
from src.backend.embeddings.vector_store import VectorStoreManager
from src.backend.llm.base import BaseLLMClient
from src.backend.llm.compiler import ChatHistoryCompiler
from src.backend.llm.prompts import ContextPromptTemplate

class RagOrchestrator:
    """
    Coordinates semantic vector search, chat conversation history, 
    RAG prompt formatting, and LLM text generation.
    """
    def __init__(self, 
                 db_mgr: DatabaseManager, 
                 vector_mgr: VectorStoreManager, 
                 llm_client: BaseLLMClient,
                 history_limit: int = 4000):
        self.db_mgr = db_mgr
        self.vector_mgr = vector_mgr
        self.llm_client = llm_client
        self.compiler = ChatHistoryCompiler(max_history_tokens=history_limit)
        self.prompt_template = ContextPromptTemplate()

    def generate_chat_response(self, 
                               session_id: str, 
                               query: str, 
                               search_limit: int = 3, 
                               file_path: Optional[str] = None) -> Dict[str, Any]:
        """Runs RAG pipeline flow: retrieves context chunks, formats prompt, queries LLM, logs to SQLite."""
        # 1. Fetch semantic context chunks from Vector Store
        matches = self.vector_mgr.search(query=query, limit=search_limit, file_path=file_path)
        chunks = [m["text"] for m in matches]
        sources = [m["metadata"] for m in matches]
        
        # 2. Add User Message to SQLite database logs
        self.db_mgr.add_message(session_id=session_id, sender="user", content=query)
        
        # 3. Retrieve and compile chronological chat history
        db_messages = self.db_mgr.get_chat_messages(session_id)
        # Exclude the latest user message to handle it separately in prompt template
        history = self.compiler.compile(db_messages[:-1])
        
        # 4. Construct context prompt inserting search chunks
        formatted_prompt = self.prompt_template.format(query=query, chunks=chunks)
        
        # 5. Execute text completion request
        response_text = self.llm_client.generate_response(
            prompt=formatted_prompt,
            system_instruction="You are SYNAPSE, a local RAG assistant."
        )
        
        # 6. Add Assistant Response to SQLite with sources list citations
        self.db_mgr.add_message(
            session_id=session_id,
            sender="assistant",
            content=response_text,
            sources=sources
        )
        
        return {
            "response": response_text,
            "sources": sources
        }
