from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import bot
from config_reader import config
from data.database import DB_Users
from keyboard.reply import menu
from keyboard.inline import adm_inl_panel

router = Router()
MAIN_ADMIN_ID = config.admin_id.get_secret_value()
APPROVE_ADMIN = "approve_adm"
REJECT_ADMIN = "reject_adm"

@router.message(Command("admin"))
async def request_admin_access(message: Message):
    user = message.from_user
    
    if await DB_Users.is_admin(user.id):
        await message.answer("Панель администратора:",
                      reply_markup=adm_inl_panel)
        return 0
    
    if not(await DB_Users.select_cell(user.id, "us_name")) and user.username:
        DB_Users.update_cell(user.id, "us_name", user.username)
    
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✅Одобрить", 
        callback_data=f"{APPROVE_ADMIN}:{user.id}"
    )
    builder.button(
        text="❌Отклонить", 
        callback_data=f"{REJECT_ADMIN}:{user.id}"
    )
    builder.adjust(2)

    text = (
        f"‼️Новый запрос на администрировение:\n\n"
        f"Имя: {user.full_name}\n"
        f"Username: @{user.username if user.username else '—'}\n"
        f"TG ID: {user.id}"
    )
    
    photos = await bot.get_user_profile_photos(user.id, limit=1)
    if photos.total_count > 0:
        photo = photos.photos[0][0].file_id  #первое фото в профиле
        await bot.send_photo(
            chat_id=MAIN_ADMIN_ID,
            photo=photo,
            caption=text,
            reply_markup=builder.as_markup()
        )
    else:
        await bot.send_message(
            chat_id=MAIN_ADMIN_ID,
            text=text,
            reply_markup=builder.as_markup()
        )

    await message.answer("🤖Заявка на получение прав администратора отправлена, подожди пока её рассмотрят")


@router.callback_query(F.data.startswith(APPROVE_ADMIN))
async def approve_admin(callback: CallbackQuery):
    parts = callback.data.split(":")
    tg_id = int(parts[1])
    
    user = await DB_Users.select_user(tg_id)
    name, username = user[1], (user[2] if user[2] else "—")

    await DB_Users.add_admin(tg_id, name, f"{username}")
    
    if callback.message.photo:
        await callback.bot.edit_message_caption(chat_id=callback.message.chat.id,
                                                message_id=callback.message.message_id,
                                                caption=f"✅ Пользователь {name} (@{username}) был добавлен как админ.",
                                                reply_markup=None)
    else:
        await callback.message.edit_text(
            text=f"✅ Пользователь <b>{name}</b> (@{username}) был добавлен как админ.",
            reply_markup=None
        )
    
    await callback.bot.send_message(
        chat_id=tg_id,
        text="✅Твоя заявка на администратора была одобрена\n\n<i>Чтобы открыть панель администратора пропиши /admin</i>"
    )
    await callback.answer()

@router.callback_query(F.data.startswith(REJECT_ADMIN))
async def reject_admin(callback: CallbackQuery):
    await callback.answer()
    parts = callback.data.split(":")
    tg_id = int(parts[1])
    
    user = await DB_Users.select_user(tg_id)
    name, username = user[1], (user[2] if user[2] else "—")
    
    if callback.message.photo:
        await callback.bot.edit_message_caption(chat_id=callback.message.chat.id,
                                                message_id=callback.message.message_id,
                                                caption=f"❌Заявка от {name} (@{username if username else '—'}) на получение статуса администратора отклонена",
                                                reply_markup=None)
    else:
        await callback.message.edit_text(
            text=f"❌Заявка от {name} (@{username if username else '—'}) на получение статуса администратора отклонена",
            reply_markup=None
        )

    await callback.bot.send_message(
        chat_id=tg_id,
        text="❌Заявка на получение администратора была отклонена"
    )