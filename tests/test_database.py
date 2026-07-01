import os
import sys

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.database.manager import DatabaseManager

def main():
    print("=== Testing Database Connection & CRUD ===")
    
    test_db_path = "data/test_db.db"
    
    # Ensure a fresh database for testing
    for suffix in ["", "-shm", "-wal"]:
        path = test_db_path + suffix
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
                
    # 1. Initialize DB Manager
    db = DatabaseManager(db_path=test_db_path)
    print("[+] Database schema created successfully.")
    
    # 2. Test Ingestion Tracking
    print("\nTesting document ingestion status tracking...")
    db.register_file("C:/files/doc.pdf", "sha256_mock_hash", 2048)
    record = db.get_file("C:/files/doc.pdf")
    print(f"Registered record: path={record['file_path']}, status={record['status']}")
    assert record["status"] == "pending"
    
    db.update_file_status("C:/files/doc.pdf", "indexed", chunk_count=12)
    record = db.get_file("C:/files/doc.pdf")
    print(f"Updated record: status={record['status']}, chunk_count={record['chunk_count']}")
    assert record["status"] == "indexed"
    assert record["chunk_count"] == 12

    # 3. Test Chat Sessions
    print("\nTesting chat conversations log...")
    session_id = db.create_chat_session(title="Database optimization query")
    session = db.get_chat_session(session_id)
    print(f"Created chat session: id={session['id'][:8]}..., title='{session['title']}'")
    
    # 4. Test Message Logging with Citations
    db.add_message(session_id, sender="user", content="Where was SQLite WAL discussed?")
    db.add_message(session_id, sender="assistant", content="SQLite WAL was discussed in database_guide.txt.", sources=[
        {"file_path": "database_guide.txt", "chunk_index": 2, "similarity": 0.95}
    ])
    
    messages = db.get_chat_messages(session_id)
    print("Retrieved conversation log:")
    for msg in messages:
        print(f"  [{msg['sender'].upper()}]: {msg['content']}")
        if msg["sources"]:
            print(f"    (Citations: {msg['sources']})")
            
    # Clean up test database files
    print("\nCleaning up test databases...")
    for suffix in ["", "-shm", "-wal"]:
        path = test_db_path + suffix
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
                
    print("=== Database test passed successfully! ===")

if __name__ == "__main__":
    main()
