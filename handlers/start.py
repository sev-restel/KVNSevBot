from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from data.database import DB_Users as db_us
from handlers.send_photo import edit_ticket
from keyboard.reply import menu

router = Router()

#приветственное сообщение
@router.message(CommandStart())
async def start_command(message: Message):
    full_name = (message.from_user.first_name or "") + " " + (message.from_user.last_name or "")
    full_name = full_name.strip()
    if len(full_name) <= 1: full_name = "Гость"
    if len(full_name) > 26: full_name = full_name[:27] + "."
    
    await db_us.add_user(message.from_user.id, full_name)

    # await message.answer("""начальное сообщение с инфой""")

    photo = await edit_ticket(full_name)

    await message.answer_photo(photo=photo, caption=f"Вот ваш билет, {full_name}! \n*дальше инфа какая-то вводная*",
                               reply_markup=menu)
