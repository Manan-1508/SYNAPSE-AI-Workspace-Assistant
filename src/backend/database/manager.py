import os
import sqlite3
import json
import uuid
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """
    Manages SQLite database connections and handles schema initialization.
    Configured with WAL (Write-Ahead Logging) to allow concurrent reads and writes.
    Provides complete CRUD operations for document tracking and chat logs.
    """

    def __init__(self, db_path: str = "data/synapse.db"):
        self.db_path = db_path
        # Ensure database directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Helper to create a configured connection to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Configure database pragmas for concurrency and speed
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def _init_db(self):
        """Creates the database tables if they do not already exist."""
        with self._get_connection() as conn:
            # Files table to track document indexing states
            conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_size_bytes INTEGER NOT NULL,
                    chunk_count INTEGER DEFAULT 0,
                    status TEXT NOT NULL, -- 'pending', 'indexing', 'indexed', 'failed'
                    error_message TEXT,
                    last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Chat sessions table to organize separate conversation threads
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Chat messages table to store conversations and citations logs
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    sender TEXT NOT NULL, -- 'user', 'assistant'
                    content TEXT NOT NULL,
                    sources TEXT, -- JSON array of file/chunk citations references
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
                );
            """)

            # Create index for session ID lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id 
                ON chat_messages(session_id);
            """)
            conn.commit()

    # --- FILE CRUD OPERATIONS ---

    def register_file(self, file_path: str, file_hash: str, file_size: int) -> int:
        """Inserts or updates a file registry entry, resetting status to pending."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO files (file_path, file_hash, file_size_bytes, status, error_message, last_indexed)
                VALUES (?, ?, ?, 'pending', NULL, CURRENT_TIMESTAMP)
                ON CONFLICT(file_path) DO UPDATE SET
                    file_hash = excluded.file_hash,
                    file_size_bytes = excluded.file_size_bytes,
                    status = 'pending',
                    error_message = NULL,
                    last_indexed = CURRENT_TIMESTAMP;
            """, (file_path, file_hash, file_size))
            conn.commit()
            return cursor.lastrowid

    def update_file_status(self, file_path: str, status: str, chunk_count: int = 0, error_message: Optional[str] = None):
        """Updates the status and logs any compilation error message."""
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE files
                SET status = ?, chunk_count = ?, error_message = ?, last_indexed = CURRENT_TIMESTAMP
                WHERE file_path = ?;
            """, (status, chunk_count, error_message, file_path))
            conn.commit()

    def get_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single file record by path."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM files WHERE file_path = ?;", (file_path,)).fetchone()
            return dict(row) if row else None

    def list_files(self) -> List[Dict[str, Any]]:
        """Lists all files in the registry."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM files ORDER BY last_indexed DESC;").fetchall()
            return [dict(r) for r in rows]

    def remove_file(self, file_path: str):
        """Deletes a file entry from the registry."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM files WHERE file_path = ?;", (file_path,))
            conn.commit()

    # --- CHAT SESSION CRUD OPERATIONS ---

    def create_chat_session(self, session_id: Optional[str] = None, title: str = "New Chat") -> str:
        """Creates a new conversation thread."""
        s_id = session_id or str(uuid.uuid4())
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO chat_sessions (id, title, created_at)
                VALUES (?, ?, CURRENT_TIMESTAMP);
            """, (s_id, title))
            conn.commit()
        return s_id

    def list_chat_sessions(self) -> List[Dict[str, Any]]:
        """Lists all active chat sessions."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM chat_sessions ORDER BY created_at DESC;").fetchall()
            return [dict(r) for r in rows]

    def get_chat_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves details of a single chat session."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM chat_sessions WHERE id = ?;", (session_id,)).fetchone()
            return dict(row) if row else None

    def delete_chat_session(self, session_id: str):
        """Deletes a chat session, cascading deletes to its messages."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM chat_sessions WHERE id = ?;", (session_id,))
            conn.commit()

    # --- CHAT MESSAGES CRUD OPERATIONS ---

    def add_message(self, session_id: str, sender: str, content: str, sources: Optional[List[Dict[str, Any]]] = None) -> int:
        """Appends a new message in a session log."""
        sources_str = json.dumps(sources) if sources else None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_messages (session_id, sender, content, sources, created_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP);
            """, (session_id, sender, content, sources_str))
            conn.commit()
            return cursor.lastrowid

    def get_chat_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves messages for a session in chronological order."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM chat_messages 
                WHERE session_id = ? 
                ORDER BY created_at ASC;
            """, (session_id,)).fetchall()
            
            result = []
            for r in rows:
                msg = dict(r)
                if msg["sources"]:
                    try:
                        msg["sources"] = json.loads(msg["sources"])
                    except json.JSONDecodeError:
                        msg["sources"] = []
                else:
                    msg["sources"] = []
                result.append(msg)
            return result
