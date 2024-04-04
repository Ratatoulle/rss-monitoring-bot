from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

separate_or_all = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Все"),
            KeyboardButton(text="Отдельный источник")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
"""
    Keyboard with choice how user wants to display news
"""


def list_user_subscriptions(subscriptions: list):
    """
        Keyboard used to display user subscriptions in buttons
    """
    builder = ReplyKeyboardBuilder()
    [builder.button(text=subscription.resource_url) for subscription in subscriptions]
    builder.adjust(*[1] * len(subscriptions))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
