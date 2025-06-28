from datetime import datetime, time
from data.database import DB_Users as db
import asyncio

async def scheduled_mailing(bot):    
    while True:
        now = datetime.now().time()
        target_time_1 = time(17, 00)  # 17:00
        target_time_2 = time(18, 00)  # 18:00
        target_time_3 = time(19, 00)  # 19:00

        if now.hour == target_time_1.hour and now.minute == target_time_1.minute:
                await send_wave(bot, wave_one)
                await asyncio.sleep(60)  # avoid repeat

        elif now.hour == target_time_2.hour and now.minute == target_time_2.minute:
            await send_wave(bot, wave_two)
            await asyncio.sleep(60)

        elif now.hour == target_time_3.hour and now.minute == target_time_3.minute:
            await send_wave(bot, wave_three)
            await asyncio.sleep(60)
            
        await asyncio.sleep(10)


async def send_wave(bot, wave_func):
    users = await db.get_all_users()
    for user_id in users:
        try:
            await bot.send_message(user_id[0], await wave_func(user_id[1]))
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"[send_wave] Ошибка при отправке пользователю {user_id[0]}: {e}")


async def wave_one(name):
    text = f"""🔥 КВН-атмосфера уже на подходе! 🔥

Привет, {name}!

Осталось всего 2 часа до самого летнего КВН в Новом Херсонесе! ⏳

📍 Не забудь: Начало в 19:20

Место: Основной зал "Точки опоры" (Музей Античной Византии, вход с обратной стороны от КПП Восток)

Твой именной билет (в этом чате)

🎁 Совет: приходи немного раньше - сможешь первым проголосовать за нашу локацию жетонами!

До встречи в эпицентре юмора! 😉

#ДеньМолодёжиНХ #КВН_НовыйХерсонес"""

    return text


async def wave_two(name):
    text = f"""🚨 Стартуем уже через час! 🚨

{name}, ты готов к взрыву эмоций? 💥

Через 60 минут начинается наш КВН-блок в рамках Дня Молодёжи!

📌 Что взять с собой:
- Хорошее настроение
- Пару друзей (чем больше - тем веселее)
- Твой именной билет

📍 Как найти: ищи здание Музея Античной Византии, наш зал - "Точка опоры".

Не пропусти самое яркое событие лета!☀️ """

    return text

async def wave_three(name):
    text = f"""🎤 ПОЕХАЛИ! Ты с нами? 🎤

{name}, мы ЖДЁМ тебя прямо сейчас в Основном зале "Точки опоры"!

🔥 Сейчас стартует:
- Импровизационный баттл
- КВН-разминки со звёздами лиги
- Вкусные шутки и море драйва

Твой именной билет даёт тебе +100 к харизме сегодня! 😎

📍 Точка сбора: Музей Античной Византии (обойди здание с обратной стороны от КПП Восток).

Не опоздай на самое жаркое шоу лета! 🌊"""

    return text