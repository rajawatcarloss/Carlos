import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'telegram-manager-secret-key-2024')
    DEBUG = True
    DATABASE_PATH = 'telegram_manager.db'
    SESSIONS_PATH = 'sessions'
    API_ID = int(os.getenv('API_ID', '12345'))  # Get from https://my.telegram.org
    API_HASH = os.getenv('API_HASH', 'your_hash_here')  # Get from https://my.telegram.org
    
    if not os.path.exists(SESSIONS_PATH):
        os.makedirs(SESSIONS_PATH)
