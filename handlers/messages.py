from aiogram import Router
from aiogram.types import Message
from keyboard.reply import menu

router = Router()

#тригерится на мусор
@router.message()
async def echo(message: Message):
    await message.reply(
        "⚠️Не понял тебя, напиши команду заново⚠️\n",
        reply_markup=menu
    )