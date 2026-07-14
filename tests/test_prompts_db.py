import os
import sys

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.llm.prompts import ContextPromptTemplate, GuidelinesPromptTemplate
from src.backend.database.manager import DatabaseManager

def main():
    print("=== Testing Prompt Templates ===")
    
    # 1. Verify ContextPromptTemplate formatting
    c_template = ContextPromptTemplate()
    c_output = c_template.format(
        query="Explain HNSW space configurations.",
        chunks=["ChromaDB collection uses HNSW.", "Distance metric is set to cosine."]
    )
    print("Context Prompt Output:")
    print(c_output)
    assert "HNSW" in c_output
    assert "cosine" in c_output
    assert "Explain HNSW" in c_output
    
    # 2. Verify GuidelinesPromptTemplate formatting
    g_template = GuidelinesPromptTemplate()
    g_output = g_template.format(
        guidelines=["Always reply in Python.", "Format code blocks."]
    )
    print("\nGuidelines Prompt Output:")
    print(g_output)
    assert "Always reply in Python." in g_output
    
    print("\n=== Testing Database Manager Chat History CRUD ===")
    test_db = "data/test_history.db"
    
    # Ensure fresh state
    for path in [test_db, test_db + "-shm", test_db + "-wal"]:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
            
    db = DatabaseManager(db_path=test_db)
    
    try:
        # Create chat session
        session_id = db.create_chat_session(title="Workspace Ingestion Chat")
        print(f"[+] Created session ID: {session_id}")
        
        # Verify listing
        sessions = db.list_chat_sessions()
        assert len(sessions) == 1
        assert sessions[0]["id"] == session_id
        
        # Log chat messages
        msg_id1 = db.add_message(
            session_id=session_id, 
            sender="user", 
            content="Can we parse multi-tab Excel files?"
        )
        msg_id2 = db.add_message(
            session_id=session_id, 
            sender="assistant", 
            content="Yes, using sheet-by-sheet pandas readers.",
            sources=[{"file_path": "excel.py", "chunk_index": 0}]
        )
        
        # Fetch messages and verify ordering
        messages = db.get_chat_messages(session_id)
        print("Logged messages:")
        for msg in messages:
            print(f"  {msg['sender']}: {msg['content']} (citations={msg['sources']})")
            
        assert len(messages) == 2
        assert messages[0]["sender"] == "user"
        assert messages[1]["sender"] == "assistant"
        assert messages[1]["sources"][0]["file_path"] == "excel.py"
        
        # Delete session and verify cascading deletion
        db.delete_chat_session(session_id)
        assert len(db.list_chat_sessions()) == 0
        
        # Fetching messages on deleted session should return empty
        assert len(db.get_chat_messages(session_id)) == 0
        print("[+] Session deletion cascades messages cleanly.")
        
    finally:
        # Clean up database files
        for path in [test_db, test_db + "-shm", test_db + "-wal"]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
                
    print("[+] Prompt templates and SQLite chat history tests passed successfully.")

if __name__ == "__main__":
    main()
