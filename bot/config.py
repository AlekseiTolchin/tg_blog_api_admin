import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL', 'http://localhost:8000/api/posts/')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
