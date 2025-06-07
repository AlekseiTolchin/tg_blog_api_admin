from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_posts_keyboard(posts):
    keyboard = InlineKeyboardBuilder()
    for post in posts:
        keyboard.add(InlineKeyboardButton(text=post['title'], callback_data=f"post_{post['id']}"))
    return keyboard.adjust(1).as_markup()
