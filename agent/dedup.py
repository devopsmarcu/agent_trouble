import hashlib
import sqlite3
import os
from datetime import datetime

# Path definition
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "metadata.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash_content TEXT UNIQUE,
            query TEXT,
            answer TEXT,
            source TEXT,
            reliability TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB when module is imported
init_db()

def generate_hash(query: str, answer: str) -> str:
    content = f"{str(query).strip().lower()}|{str(answer).strip().lower()}"
    return hashlib.sha256(content.encode()).hexdigest()

def is_duplicate(query: str, answer: str) -> bool:
    content_hash = generate_hash(query, answer)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT 1 FROM knowledge WHERE hash_content = ?", (content_hash,))
    row = c.fetchone()
    conn.close()
    return row is not None

def save_metadata(query: str, answer: str, source: str) -> bool:
    content_hash = generate_hash(query, answer)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO knowledge (hash_content, query, answer, source, reliability)
            VALUES (?, ?, ?, ?, ?)
        ''', (content_hash, query, answer, source, 'Alta'))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
