import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_NAMAE = os.getenv('DB_NAMME')

engine = create_async_engine(f'sqlite+aiosqlite:///{DB_NAMAE}.db')
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
