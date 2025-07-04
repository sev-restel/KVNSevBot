from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from math import ceil
from datetime import datetime
from keyboard.inline import (adm_inl_panel, adm_inl_cancel, adm_inl_approveNotif)
from data.database import DB_Notification
from utils.states import Notif
from utils.help_func import valid_date, generate_id
from handlers.spam import send_notif
from config import bot

router = Router()

error_text_start = "⚠️Error: неверный формат сообщения.\n\n"
error_text_date = "⚠️Error: неверный формат даты.\n\n"
date_text = f"Отправь в чат новым сообщением <b>дату</b> рассылки в формате {datetime.now().replace(second=0, microsecond=0)} (год-месяц-день часы:минуты) или \"<b>-</b>\" если хочешь отправить уведомление моментально:"
text_text = "Отправь в чат новым сообщением <b>текст</b> рассылки (с форматированием):"
photo_text = "Если к уведомлению нужно прикрепить <b>фото</b> то отправь его <b>новым сообщением</b>, либо \"<b>-</b>\" если не нужно:"
date_text_edit = f"Отправь в чат новую <b>дату</b> рассылки в формате {datetime.now().replace(second=0, microsecond=0)} (год-месяц-день часы:минуты) или \"<b>-</b>\" если хочешь отправить уведомление моментально:"
text_text_edit = "Введи новый <b>текст</b> уведомления:"
photo_text_edit = "Отправь новое <b>фото</b>, либо \"<b>-</b>\" если не нужно:"

@router.callback_query(F.data.startswith("list_notif"))
async def list_notification(callback: CallbackQuery):
    await callback.answer("")

    #oпределяем страницу
    parts = callback.data.split(":")
    page = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 0
    per_page = 3

    notif_list = await DB_Notification.get_all_notification() # id_notif, text, date, is_active, photo
    total = len(notif_list)
    pages = ceil(total / per_page)

    if total == 0:
        await callback.message.edit_text("⚠️Уведомлений пока нет.", 
                                         reply_markup=adm_inl_panel)
        return

    #слайс текущей страницы
    start = page * per_page
    end = start + per_page
    current_page_items = notif_list[start:end]

    output = f"<b>📋 Уведомления ({total} шт.) — Страница {page + 1}/{pages}</b>\n\n"
    for notif in current_page_items:
        output += (
            f"🆔 <code>{notif[0]}</code>\n"
            f"🗓️ <i>{notif[2]}</i>\n"
            f"📎 Фото: {'✅' if notif[4] else '❌'}\n"
            f"☑️ Активно: {"✅" if notif[3] == 1 else "❌"}\n"
            f"🔹 {notif[1][:150]}{'...' if len(notif[1]) > 150 else ''}\n\n"
        )

    #кнопки пагинации #.adjust(2, *[1] * 2) - полезность
    keyboard = InlineKeyboardBuilder()
    if page > 0:
        keyboard.button(text="◀️ Назад", callback_data=f"list_notif:{page - 1}")
    if end < total:
        keyboard.button(text="Вперёд ▶️", callback_data=f"list_notif:{page + 1}")
    keyboard.button(text="✏️ Редакт./Просмотр", callback_data="adm_cancel")
    keyboard.button(text="🔙 Назад в меню", callback_data="adm_cancel")
    keyboard.adjust(2)

    await callback.message.edit_text(output, reply_markup=keyboard.as_markup())


#добавить новое уведомление
@router.callback_query(F.data == "add_notif")
async def add_notif(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.set_state(Notif.notif_text)
    
    await callback.message.edit_text(f"{text_text}", 
                                     reply_markup=adm_inl_cancel)


@router.message(Notif.notif_text, F.text)
async def add_notif_text(message: Message, state: FSMContext):
    await state.update_data(notif_text = message.html_text)
    await state.set_state(Notif.notif_date)
    
    await message.answer(f"{date_text}", 
                                     reply_markup=adm_inl_cancel)


@router.message(Notif.notif_text, ~F.text)
async def not_add_notif_text(message: Message):
    await message.answer(f"{error_text_start}{text_text}", 
                                     reply_markup=adm_inl_cancel)


@router.message(Notif.notif_date, F.text)
async def add_notif_data(message: Message, state: FSMContext):
    date = message.text
    if date.strip() == "-":
        date = "0000-00-00 00:00"
    elif not(await valid_date(date)):
        await message.reply(f"{error_text_date}{date_text}", 
                                     reply_markup=adm_inl_cancel)
        return
    
    await state.update_data(notif_date = date)
    await state.set_state(Notif.notif_photo)

    await message.answer(f"{photo_text}", 
                                     reply_markup=adm_inl_cancel)


@router.message(Notif.notif_date, ~F.text)
async def add_notif_data(message: Message):
    await message.reply(f"{error_text_start}{date_text}", 
                        reply_markup=adm_inl_cancel)


@router.message(Notif.notif_photo)
async def add_notif_photo(message: Message, state: FSMContext):
    try:
        if message.text and message.text.strip() == "-":
            await state.update_data(notif_photo = None)
        elif message.photo:
            await state.update_data(notif_photo = message.photo[-1].file_id)
        else:
            raise ValueError("Неверный формат")
    except Exception as e:
        await message.reply(f"{error_text_start}{photo_text}", 
                                     reply_markup=adm_inl_cancel)
        return
    
    await state.set_state(Notif.notif_preview)
    
    #предпросмотр сообщения
    await preview_notification(message, state)


#обработка кнопок меню в превью

@router.callback_query(F.data == "approve_notif")
async def approve_notification(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    
    data = await state.get_data()
    await state.clear()

    try:
        for _ in range(10):
            new_id = await generate_id()
            if not await DB_Notification.is_id_exists(new_id):
                break
        else:
            raise ValueError("Не удалось сгенерировать уникальный ID за 10 попыток")
        
        dop_text = ""
        
        if data["notif_date"] == "0000-00-00 00:00":
            await DB_Notification.add_notification(new_id, data["notif_text"], data["notif_date"], False, data["notif_photo"])
            
            valid_data_spam = [0, data["notif_text"], data["notif_date"], 0, data["notif_photo"]]
            await send_notif(bot, valid_data_spam)
            
            dop_text = " и было отослано <b>всем пользователям</b>"
        else:
            await DB_Notification.add_notification(new_id, data["notif_text"], data["notif_date"], True, data["notif_photo"])
        
        await callback.message.edit_text(f"✅Уведомление сохранено{dop_text}\n\nПанель администратора:", 
                            reply_markup=adm_inl_panel)
    except Exception as e:
        await callback.message.edit_text("❌Уведомление <b>не</b> сохранено, попробуй еще раз\n\nПанель администратора:", 
                                         reply_markup=adm_inl_panel)
        await callback.message.answer(f"⚠️Error: {e}")


@router.callback_query(F.data == "edit_notif_text")
async def edit_notif_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.set_state(Notif.edit_text)
    await callback.message.edit_text(f"{text_text_edit}", 
                                     reply_markup=adm_inl_cancel)


@router.message(Notif.edit_text, F.text)
async def save_new_text(message: Message, state: FSMContext):
    await state.update_data(notif_text=message.html_text)
    await message.answer("✅Текст обновлен.")
    await preview_notification(message, state)

@router.message(Notif.edit_text, ~F.text)
async def not_save_new_text(message: Message):
    await message.answer(f"{error_text_start}{text_text_edit}")


@router.callback_query(F.data == "edit_notif_date")
async def edit_notif_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.set_state(Notif.edit_date)
    await callback.message.edit_text(f"{date_text_edit}", 
                                     reply_markup=adm_inl_cancel)


@router.message(Notif.edit_date, F.text)
async def save_new_date(message: Message, state: FSMContext):
    if not await valid_date(message.text):
        await message.answer(f"{error_text_date}{date_text_edit}", 
                             reply_markup=adm_inl_cancel)
        return
    await state.update_data(notif_date=message.text)
    await message.answer("✅Дата обновлена.")
    await preview_notification(message, state)


@router.message(Notif.edit_date, ~F.text)
async def not_save_new_date(message: Message):
    await message.answer(f"{error_text_start}{date_text_edit}", 
                         reply_markup=adm_inl_cancel)


@router.callback_query(F.data == "edit_notif_photo")
async def edit_notif_photo(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Notif.edit_photo)
    await callback.message.edit_text(f"{photo_text_edit}", 
                                     reply_markup=adm_inl_cancel)


@router.message(Notif.edit_photo)
async def save_new_photo(message: Message, state: FSMContext):
    try:
        if message.text and message.text.strip() == "-":
            await state.update_data(notif_photo=None)
        elif message.photo:
            await state.update_data(notif_photo=message.photo[-1].file_id)
        else:
            raise ValueError("Неверный формат")
    except:
        await message.reply(f"{error_text_start}{photo_text_edit}", reply_markup=adm_inl_cancel)
        return
    await message.answer("✅Фото обновлено.")
    await preview_notification(message, state)

    
async def preview_notification(message_or_callback, state: FSMContext):
    data = await state.get_data()
    await state.set_state(Notif.notif_preview)

    if data["notif_photo"]:
        await message_or_callback.answer_photo(photo=data["notif_photo"], 
                                               caption=data["notif_text"])
    else:
        await message_or_callback.answer(data["notif_text"])

    await message_or_callback.answer(f"Это сообщение будет отправлено в \n<i>{"моментально" if data['notif_date'] == "0000-00-00 00:00" else data['notif_date']}</i>\n\nВсё верно?",
                                     reply_markup=adm_inl_approveNotif)
