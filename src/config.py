import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
