from aiogram.fsm.state import StatesGroup, State

class FeedBack(StatesGroup):
    text_msg = State()


class Admin(StatesGroup):
    # source_name = State()
    # front_name = State()
    # bio = State()
    # next = State()
    
    num_del_admin = State()
    next_del_adm = State()

class Notif(StatesGroup):
    notif_text = State()
    notif_date = State()
    notif_photo = State()
    notif_preview = State()
    edit_text = State()
    edit_date = State()
    edit_photo = State()