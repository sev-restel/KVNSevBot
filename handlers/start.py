from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
import random

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
    
    username = message.from_user.username
    
    await db_us.add_user(message.from_user.id, full_name, username)

    photo = await edit_ticket(full_name)

    await message.answer_photo(photo=photo, 
                               caption=f"""Билет №{random.randint(100000, 999999)} для @{username}

💫<b>Добро пожаловать на самый летний КВН в Новом Херсонесе!</b>

Сегодня, 28 июня, в День Молодёжи тебя ждёт:

🔥 Главный хит программы — наша КВН-локация с:
<blockquote>- Взрывной импровизацией
- Крутыми разминками от звёзд Севастопольской лиги
- Интерактивами, где ты сам станешь участником шоу</blockquote>

📍 Где?
Основной зал «Точки опоры» (здание Музея Античной Византии).
<i>Совет: ищи вход с противоположной стороны от КПП Восток!</i>

🎁 Фишка дня:
Голосуй жетонами за лучшую локацию — пусть КВН победит!

📌 Важно:
Регистрация по ссылке → https://rosmolodezh-event.timepad.ru/event/3407738/

Возьми с собой друзей — будет в 2 раза веселее!
<tg-spoiler>⏰ Ждём тебя с 19:20 у нашей сцены.
P.S. Этот билет — твой пропуск в эпицентр юмора!</tg-spoiler>

🫶 Севастопольская официальная лига КВН""",
                               reply_markup=menu)
