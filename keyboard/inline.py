from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌Отменить", callback_data="cancel")]
])


#админские клавиатуры:
adm_inl_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧑‍💼Cписок админов", callback_data="list_admins")],
    [InlineKeyboardButton(text="⚙️Управление уведомлениями", callback_data="notification")],
])

adm_inl_deladm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧹Удалить админа", callback_data="del_admin"),
     InlineKeyboardButton(text="↩️Назад в меню", callback_data="adm_cancel")]
])

adm_inl_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌Отмена", callback_data="adm_cancel")]
])

adm_inl_notifMain = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📋Список уведомлений", callback_data="list_notif")],
    [InlineKeyboardButton(text="➕Добавить новое", callback_data="add_notif")]
])

adm_inl_approveNotif = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅Подтвердить", callback_data="approve_notif"),
     InlineKeyboardButton(text="✏️Изменить текст", callback_data="edit_notif_text")],
    [InlineKeyboardButton(text="📅Изменить дату", callback_data="edit_notif_date"),
     InlineKeyboardButton(text="🖼️Изменить фото", callback_data="edit_notif_photo")],
    [InlineKeyboardButton(text="❌Отменить", callback_data="adm_cancel")]
])
