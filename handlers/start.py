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
    #переделать: в бд заносить всё имя, для билета установить проверку длинны имени
    user = message.from_user
    full_name, username = user.full_name, user.username
    if not username: username = "-"
    if len(user.full_name.strip()) < 1: full_name = "Гость"
    elif len(user.full_name) > 26: full_name = user.full_name[:26] + "."
    
    await db_us.add_user(user.id, full_name, user.username)

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
