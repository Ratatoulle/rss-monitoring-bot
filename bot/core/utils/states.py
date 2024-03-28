from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    rss_link = State()
