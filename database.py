import sqlite3
import os
from datetime import datetime

DB_PATH = "database.db"

class ChatDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                created_at TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT,
                content TEXT,
                file_name TEXT,
                file_path TEXT,
                file_type TEXT,
                analysis_result TEXT,
                created_at TEXT,
                FOREIGN KEY(conversation_id) REFERENCES conversations(id)
            )
        """)

        self.conn.commit()

    def create_conversation(self, title):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (title, created_at)
            VALUES (?, ?)
        """, (title, datetime.now().isoformat()))
        self.conn.commit()
        return cursor.lastrowid

    def get_conversations(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM conversations ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

    def delete_conversation(self, conversation_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        self.conn.commit()

    def add_message(self, conversation_id, role, content,
                    file_name=None, file_path=None, file_type=None, analysis_result=None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO messages (
                conversation_id, role, content,
                file_name, file_path, file_type, analysis_result, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (conversation_id, role, content, file_name, file_path, file_type,
              analysis_result, datetime.now().isoformat()))
        self.conn.commit()

    def get_messages(self, conversation_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
        """, (conversation_id,))
        return [dict(row) for row in cursor.fetchall()]
