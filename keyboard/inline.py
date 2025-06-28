from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌Отменить", callback_data="cancel")]
])
