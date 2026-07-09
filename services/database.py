import sqlite3
from datetime import datetime
from utils.config import DATABASE_URL

def init_db():
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                joined_at TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                user_id INTEGER PRIMARY KEY,
                font TEXT DEFAULT 'Arial',
                opacity INTEGER DEFAULT 50,
                color TEXT DEFAULT 'White',
                position TEXT DEFAULT 'Bottom Right',
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action_type TEXT,
                filename TEXT,
                timestamp TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()

def add_user(user_id: int, username: str):
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, joined_at) VALUES (?, ?, ?)",
                       (user_id, username, datetime.utcnow().isoformat()))
        cursor.execute("INSERT OR IGNORE INTO settings (user_id) VALUES (?)", (user_id,))
        conn.commit()

def get_settings(user_id: int):
    with sqlite3.connect(DATABASE_URL) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            add_user(user_id, None)
            cursor.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
        return dict(row)

def update_setting(user_id: int, key: str, value: str):
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE settings SET {key} = ? WHERE user_id = ?", (value, user_id))
        conn.commit()

def log_history(user_id: int, action_type: str, filename: str):
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (user_id, action_type, filename, timestamp) VALUES (?, ?, ?, ?)",
                       (user_id, action_type, filename, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

def get_history(user_id: int, limit: int = 10):
    with sqlite3.connect(DATABASE_URL) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT action_type, filename, timestamp FROM history WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]
