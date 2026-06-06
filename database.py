import sqlite3
import json
from datetime import datetime
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
                    session_file TEXT UNIQUE NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    group_name TEXT NOT NULL,
                    group_type TEXT DEFAULT 'group',
                    is_selected INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
                    UNIQUE(account_id, group_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    message_text TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    error_message TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS repeat_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    message_text TEXT NOT NULL,
                    accounts_json TEXT NOT NULL,
                    groups_json TEXT NOT NULL,
                    interval_seconds INTEGER NOT NULL,
                    repeat_count INTEGER,
                    rotation_mode TEXT DEFAULT 'sequential',
                    random_delay INTEGER DEFAULT 0,
                    delay_min INTEGER DEFAULT 1,
                    delay_max INTEGER DEFAULT 5,
                    is_active INTEGER DEFAULT 0,
                    current_repeat INTEGER DEFAULT 0,
                    current_account_index INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_executed TIMESTAMP,
                    paused_at TIMESTAMP
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
                    message TEXT,
                    error_message TEXT,
                    details_json TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def add_account(self, name, phone, session_file):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO accounts (name, phone, session_file) VALUES (?, ?, ?)', (name, phone, session_file))
            return cursor.lastrowid
    
    def get_account(self, account_id):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
            return cursor.fetchone()
    
    def get_all_accounts(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts ORDER BY created_at DESC')
            return cursor.fetchall()
    
    def update_account_login(self, account_id, user_id, first_name, last_name, username):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET user_id = ?, first_name = ?, last_name = ?, username = ?, last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id, first_name, last_name, username, account_id))
    
    def delete_account(self, account_id):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
    
    def toggle_account(self, account_id, is_active):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET is_active = ? WHERE id = ?', (is_active, account_id))
    
    def add_group(self, account_id, group_id, group_name, group_type='group'):
        with self.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO groups (account_id, group_id, group_name, group_type) VALUES (?, ?, ?, ?)', (account_id, group_id, group_name, group_type))
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
    
    def get_groups(self, account_id):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups WHERE account_id = ? ORDER BY group_name', (account_id,))
            return cursor.fetchall()
    
    def toggle_group(self, group_id, is_selected):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE groups SET is_selected = ? WHERE id = ?', (is_selected, group_id))
    
    def select_all_groups(self, account_id):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE groups SET is_selected = 1 WHERE account_id = ?', (account_id,))
    
    def deselect_all_groups(self, account_id):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE groups SET is_selected = 0 WHERE account_id = ?', (account_id,))
    
    def add_log(self, account_name, group_name, action, status, message, error_message=None, details=None):
        with self.get_db() as conn:
            cursor = conn.cursor()
            details_json = json.dumps(details) if details else None
            cursor.execute('INSERT INTO logs (account_name, group_name, action, status, message, error_message, details_json) VALUES (?, ?, ?, ?, ?, ?, ?)', (account_name, group_name, action, status, message, error_message, details_json))
    
    def get_logs(self, limit=500):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?', (limit,))
            return cursor.fetchall()
    
    def get_dashboard_stats(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM accounts WHERE is_active = 1')
            active_accounts = cursor.fetchone()['count']
            cursor.execute('SELECT COUNT(*) as count FROM accounts')
            total_accounts = cursor.fetchone()['count']
            cursor.execute('SELECT COUNT(*) as count FROM groups WHERE is_selected = 1')
            selected_groups = cursor.fetchone()['count']
            return {
                'total_accounts': total_accounts,
                'active_accounts': active_accounts,
                'selected_groups': selected_groups
            }

db = Database()
