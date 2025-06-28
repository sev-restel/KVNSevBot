from aiogram import Router, F
from aiogram.types import Message, FSInputFile, BufferedInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from PIL import Image, ImageDraw, ImageFont
import io

from keyboard.reply import menu
from keyboard.inline import cancel
from data.database import DB_Users as db_us
from utils.states import FeedBack
from bot import bot


router = Router()

@router.callback_query(F.data == "cancel")
async def cancel_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")  # Убираем часики у кнопки
    await callback.message.edit_text(
        "Действие отменено❌",
        reply_markup=None  # Убираем inline-клавиатуру
    )
    await callback.message.answer(
        "🏠Выберите действие из меню:",
        reply_markup=menu  # Отправляем новое меню
    )
    await state.clear()
    

@router.message(F.text == "⚠️Обратная связь")
async def feedback(message: Message, state: FSMContext):
    await state.set_state(FeedBack.text_msg)
    
    #обновление данных юзера
    full_name = (message.from_user.first_name or "") + " " + (message.from_user.last_name or "")
    full_name = full_name.strip()
    if len(full_name) <= 0: full_name = "Гость"
    if len(full_name) > 26: full_name = full_name[:27] + "."
    
    username = message.from_user.username
    
    await db_us.add_user(message.from_user.id, full_name, username)
    
    # #отправка картинки
    # img = Image.open("data/photo/map.png").convert("RGB")
    # buffer = io.BytesIO()
    # img.save(buffer, format="JPEG")
    # buffer.seek(0)

    # photo = BufferedInputFile(buffer.read(), filename="ticket.jpg")
    
    # await message.answer_photo(photo=photo, caption=f"Напиши и отправь сообщение с обратной связью (можешь не беспокоиться, всё анонимно:) )",
    #                            reply_markup=cancel)
    await message.answer(f"Отправь сообщение с обратной связью \n(можешь не беспокоиться, всё анонимно<tg-spoiler>, наверное))</tg-spoiler>)",
                         reply_markup=cancel)

@router.message(FeedBack.text_msg, F.text)
async def text_msg(message: Message, state: FSMContext):
    await state.update_data(text_msg=message.text)
    
    data = await state.get_data()
    await state.clear()
    
    #ПОТОМ ЗАМЕНИТЬ НА НОРМАЛЬНЫЙ ГЕТ ИЗ БАЗЫ ДАННЫХ
    admin_id = 1620144806
    
    try:
        await bot.send_message(admin_id, f"Пользователь: {message.from_user.first_name or "Гость"}, id: @{message.from_user.username}\n\n<blockquote>{data["text_msg"]}</blockquote>")
        await message.reply("Сообщение успешно отправлено успешно✅\n\nСпасибо что помогаете нам стать лучше!",
                        reply_markup=menu)
    except:
        await message.reply("Что-то пошло не так, попробуй позже‼️",
                        reply_markup=menu)