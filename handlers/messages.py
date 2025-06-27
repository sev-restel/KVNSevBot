from aiogram import Router
from aiogram.types import Message

router = Router()

#тригерится на мусор
@router.message()
async def echo(message: Message):
    await message.reply(
        "⚠️Не понял тебя, напиши команду заного⚠️\n"
    )