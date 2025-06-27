from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍Локация"),
            KeyboardButton(text="🎟️Билет")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие из меню...",
    selective=True
)

rmk = ReplyKeyboardRemove()