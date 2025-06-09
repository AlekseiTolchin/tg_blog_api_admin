from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction

import src.bot.keyboards as kb
from src.bot.utils import fetch_from_api, logger, format_post_date
from src.config import API_URL

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action=ChatAction.TYPING)
    await message.answer('Здравствуйте! Введите команду /posts для получения списка постов')


@router.message(Command('posts'))
async def cmd_help(message: Message):
    try:
        posts = await fetch_from_api(API_URL)
        if not posts:
            await message.answer('Пока нет ни одного поста.')
            return

        keyboard = await kb.create_posts_keyboard(posts)
        await message.answer('Выберите пост для чтения:', reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Ошибка при получении постов: {e}')
        await message.answer('Произошла ошибка при получении списка постов. Попробуйте позже.')


@router.callback_query(F.data.startswith('post_'))
async def process_post(callback: CallbackQuery):
    post_id = callback.data.split('_')[1]
    try:
        post = await fetch_from_api(f'{API_URL}{post_id}')
        created_at = format_post_date(post['created_at'])
        message_text = (
            f"{post['text']}\n\n"
            f'Дата создания: {created_at}'
        )
        await callback.message.answer(message_text)
    except Exception as e:
        logger.error(f'Ошибка при получении поста {post_id}: {e}')
        await callback.message.answer(
            f'Не удалось получить пост. Ошибка: {str(e)}'
        )
    await callback.answer()
