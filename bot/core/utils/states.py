from aiogram.fsm.state import StatesGroup, State


class AddResource(StatesGroup):
    """
        Class represents group of states when user wants to add resource
    """
    rss_url = State()
    is_rss_valid = State()


class GetNews(StatesGroup):
    """
        Class represents group of states when user wants to get news from resource(s)
    """
    all_or_separately = State()
    choose_resource = State()
    delta = State()
