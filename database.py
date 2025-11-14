import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ChatDatabase:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'chatdelon_db')
        self.port = os.getenv('DB_PORT', 3306)
        self.init_database()
    
    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            # First connect without database to create it
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = conn.cursor()
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            ''')
            
            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    conversation_id INT,
                    role ENUM('user', 'assistant', 'system'),
                    content TEXT,
                    file_name VARCHAR(500),
                    file_path VARCHAR(500),
                    file_type VARCHAR(50),
                    analysis_result TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database tables initialized successfully!")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    def create_conversation(self, title="Obrolan Baru"):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO conversations (title) VALUES (%s)",
                (title,)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Database Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_conversations(self, limit=50):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM conversations ORDER BY updated_at DESC LIMIT %s",
                (limit,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Database Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def get_messages(self, conversation_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM messages WHERE conversation_id = %s ORDER BY created_at ASC",
                (conversation_id,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Database Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def add_message(self, conversation_id, role, content, file_name=None, file_path=None, file_type=None, analysis_result=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO messages 
                (conversation_id, role, content, file_name, file_path, file_type, analysis_result) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (conversation_id, role, content, file_name, file_path, file_type, analysis_result)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Database Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def delete_conversation(self, conversation_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM conversations WHERE id = %s", (conversation_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()