import asyncio

from aiogram import Bot, Dispatcher

from handlers import router
from src.config import TG_BOT_TOKEN
from utils import logger


async def main():
    bot = Bot(token=TG_BOT_TOKEN)
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    logger.info('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    logger.info('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot is disabled')
