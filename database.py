import sqlite3
import json
from config import Config
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_db()
    
    @contextmanager
    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    user_id INTEGER UNIQUE,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    group_name TEXT NOT NULL,
                    is_selected INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
                    UNIQUE(account_id, group_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    account_name TEXT,
                    group_name TEXT,
                    action TEXT,
                    status TEXT,
                    message TEXT
                )
            ''')
            
            conn.commit()
    
    def add_account(self, name, phone, user_id, first_name='', last_name='', username=''):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO accounts (name, phone, user_id, first_name, last_name, username) VALUES (?, ?, ?, ?, ?, ?)',
                (name, phone, user_id, first_name, last_name, username)
            )
            return cursor.lastrowid
    
    def get_all_accounts(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_account(self, account_id):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
    
    def add_group(self, account_id, group_id, group_name):
        with self.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO groups (account_id, group_id, group_name) VALUES (?, ?, ?)',
                    (account_id, group_id, group_name)
                )
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
    
    def get_groups(self, account_id):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups WHERE account_id = ? ORDER BY group_name', (account_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def toggle_group(self, group_id, is_selected):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE groups SET is_selected = ? WHERE id = ?', (is_selected, group_id))
    
    def add_log(self, account_name, group_name, action, status, message):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO logs (account_name, group_name, action, status, message) VALUES (?, ?, ?, ?, ?)',
                (account_name, group_name, action, status, message)
            )
    
    def get_logs(self, limit=100):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?', (limit,))
            return [dict(row) for row in cursor.fetchall()]

db = Database()
