from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config
from keyboard.inline import (adm_inl_panel, adm_inl_cancel, adm_inl_deladm, adm_inl_notifMain)
from data.database import DB_Users
from utils.states import Admin

router = Router()

#отмена действия
@router.callback_query(F.data == "adm_cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.edit_text("⚠️Действие отменено\n\nПанель администратора:", 
                         reply_markup=adm_inl_panel)
    await state.clear()


#список админов
@router.callback_query(F.data == "list_admins")
async def list_admins(callback: CallbackQuery):
    await callback.answer("")
    data = await DB_Users.admins_list()
    text = '\n'.join((f"{data.index(adm)+1}. Name: <i>{adm[1]}</i>, UserName: <i>{adm[2]}</i>, ID: <i>{adm[0]}</i>" for adm in data))
    
    await callback.message.edit_text("<b>Список админов:</b>\n\n" + text,
                                     reply_markup=adm_inl_deladm)


#удаление админа
@router.callback_query(F.data == "del_admin")
async def del_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.set_state(Admin.num_del_admin)
    
    data = await DB_Users.admins_list()
    text = '\n'.join((f"{data.index(adm)+1}. Name: <i>{adm[1]}</i>, UserName: <i>{adm[2]}</i>, ID: <i>{adm[0]}</i>" for adm in data))
    
    await callback.message.edit_text(text + "\n\n<b>🤖Отправь номер админа которого нужно удалить:</b>", 
                                     reply_markup=adm_inl_cancel)

@router.message(Admin.num_del_admin, F.text)
async def del_admin_num(message: Message, state: FSMContext):
    await state.update_data(num_del_admin=message.text)
    data = await state.get_data()
    await state.clear()
    builder = InlineKeyboardBuilder()
    
    try:
        adm_data = await DB_Users.admins_list()
        adm = adm_data[int(data["num_del_admin"])-1]
        builder.button(
            text="❌Удалить", 
            callback_data=f"delete_admin:{adm[0]}"
        )
        builder.button(
            text="✅Отмена", 
            callback_data="adm_cancel"
        )
        builder.adjust(2)
        await message.reply(f"<b>Ты хочешь удалить:</b>\n\nИмя: <i>{adm[1]}</i>, юз: <i>{adm[2]}</i>, id: <i>{int(adm[0])}</i>",
                            reply_markup=builder.as_markup())
    except Exception as e:
        # print(e)
        await message.reply("Что-то пошло не так, попробуй заного‼️\n\nПанель администратора:",
                        reply_markup=adm_inl_panel)

@router.callback_query(F.data.startswith("delete_admin:"))
async def delete_admin_end(callback: CallbackQuery):
    await callback.answer()
    parts = callback.data.split(":")
    tg_id = int(parts[1])
    
    user = await DB_Users.select_admin(tg_id)
    name, username = user[1], (user[2] if user[2] else "—")

    if tg_id == int(config.admin_id.get_secret_value()):
        await callback.message.edit_text("Нельзя удалить главного администратора‼️\n\nПанель администратора:",
                        reply_markup=adm_inl_panel)
        return 0

    try:
        await DB_Users.delete_admin(tg_id)
        await callback.message.edit_text(f"✅ Пользователь {name} (@{username}) был уволен с должности администратора.\n\nПанель администратора:",
                                         reply_markup=adm_inl_panel)
    except:
        await callback.message.edit_text("Что-то пошло не так, попробуй заного‼️\n\nПанель администратора:",
                        reply_markup=adm_inl_panel)


#уведомления
@router.callback_query(F.data == "notification")
async def notification(callback: CallbackQuery):
    await callback.answer("")
    
    await callback.message.edit_text("<b>Выбери вариант из меню:</b>\n\n",
                                     reply_markup=adm_inl_notifMain)