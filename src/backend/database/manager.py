import os
import sqlite3
from typing import Optional

class DatabaseManager:
    """
    Manages SQLite database connections and handles schema initialization.
    Configured with WAL (Write-Ahead Logging) to allow concurrent reads and writes.
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
            conn.commit()
