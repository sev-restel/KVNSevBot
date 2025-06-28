from aiogram.fsm.state import StatesGroup, State

class FeedBack(StatesGroup):
    text_msg = State()