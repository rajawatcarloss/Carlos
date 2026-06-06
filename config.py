import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', True)
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'telegram_manager.db')
    SESSIONS_PATH = os.getenv('SESSIONS_PATH', 'sessions')
    API_ID = int(os.getenv('API_ID', '0'))
    API_HASH = os.getenv('API_HASH', '')
    MAX_ACCOUNTS = 10
    MAX_GROUPS = 100
    DEFAULT_DELAY = 1
    
    if not os.path.exists(SESSIONS_PATH):
        os.makedirs(SESSIONS_PATH)
