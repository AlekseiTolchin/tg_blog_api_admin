import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import router
from src.config import TG_BOT_TOKEN


async def main():
    load_dotenv()
    bot = Bot(token=TG_BOT_TOKEN)
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
