from aiogram.fsm.state import StatesGroup, State


class AddResource(StatesGroup):
    rss_url = State()
    is_rss_valid = State()


class GetNews(StatesGroup):
    is_separately = State()
    choose_resource = State()
