from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from monitoring import fetch_data
from database import DBHelper
from models import RSSItem, User, Resource, Subscription
from ..keyboards import reply
from ..utils import states

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    new_user = User(id=message.from_user.id, name=message.from_user.full_name)
    helper = DBHelper()
    helper.add_user(new_user)
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=reply.main)


@router.message(Command("add_resource"))
async def add_resource(message: Message, state: FSMContext):
    await state.set_state(states.Form.rss_url)
    await message.answer("Введите ссылку на источник:")


@router.message(states.Form.rss_url)
async def form_rss_url(message: Message, state: FSMContext):
    rss_url = message.text
    await state.update_data(rss_url=rss_url)
    await state.set_state(states.Form.is_rss_valid)
    await message.answer("Проверяем источник...")
    data = fetch_data(rss_url)
    if not data:
        await message.answer("Невозможно прочитать источник.")
        await state.clear()
    else:
        helper = DBHelper()
        if helper.get_resource(rss_url):
            await message.answer("Такой источник уже есть в базе.")
            await state.clear()
        else:
            resource = Resource(url=rss_url)
            helper.add_resource(resource)
            current_user = helper.get_user(user_id=message.from_user.id)
            subscription = Subscription(user=current_user, resource=resource)
            helper.add_subscription(subscription)
            await message.answer("Источник успешно добавлен!")


@router.message(Command("get_news_1h"))
async def get_news_1h(message: Message):
    helper = DBHelper()
    for item in


@router.message(Command("get_news_24h"))
async def get_news_24h(message: Message):
    await message.answer("Введите ссылку на источник:")


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Нажмите добавить источник и отправьте ссылку на RSS-источник для получения новостей.")
