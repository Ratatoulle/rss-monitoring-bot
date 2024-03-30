from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# available_resources = {
#     "Правительство Челябинской области": "https://pravmin.gov74.ru/prav/rss/news.htm",
#     "РБК": "http://static.feed.rbc.ru/rbc/logical/footer/news.rss",
#     "Коммерсантъ": "https://www.kommersant.ru/RSS/main.xml",
#     "Ura.ru": "https://ura.news/rss",
#     "Доступ": "https://dostup1.ru/rss/",
#     "Российская газета": "https://www.rg.ru/xml/index.xml",
# }


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
    resize_keyboard=True,  # адаптировать размер клавиатуры
    one_time_keyboard=True,  # скрыть клавиатуру после первого использования
    input_field_placeholder="Выберите действие из меню"
)

resource = ReplyKeyboardMarkup(
    keyboard=[
        [
            # KeyboardButton(text=key, url=value) for key, value in available_resources.items()
        ]
    ],
    resize_keyboard=True,  # адаптировать размер клавиатуры
    one_time_keyboard=True,  # скрыть клавиатуру после первого использования
    input_field_placeholder="Выберите действие из меню"
)