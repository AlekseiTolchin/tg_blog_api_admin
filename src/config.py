import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL', 'http://localhost:8000/api/posts/')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///posts.db')
SYNC_DATABASE_URL = os.getenv('SYNC_DATABASE_URL', 'sqlite:///posts.db')
