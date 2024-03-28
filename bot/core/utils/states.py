from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    rss_link = State()
    is_rss_valid = State()