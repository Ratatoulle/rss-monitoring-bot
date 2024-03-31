from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить источник"),
        ],
        [
            KeyboardButton(text="Получить новости за последний час"),
            KeyboardButton(text="Получить новости за последние сутки"),
        ],
        [
            KeyboardButton(text="Помощь"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню"
)

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


def list_user_subscriptions(subscriptions: list):
    builder = ReplyKeyboardBuilder()
    [builder.button(text=subscription.resource_url) for subscription in subscriptions]
    builder.adjust(*[1] * len(subscriptions))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
