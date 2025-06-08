import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
SYNC_DATABASE_URL = os.getenv('SYNC_DATABASE_URL')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))
