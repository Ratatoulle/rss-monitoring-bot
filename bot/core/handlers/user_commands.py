from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from monitoring import fetch_data
from database import DBHelper
from models import RSSItem, User, Resource, Subscription
from aiogram.utils.markdown import hbold, hitalic
import datetime
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
    await state.set_state(states.AddResource.rss_url)
    await message.answer("Введите ссылку на источник:")


@router.message(states.AddResource.rss_url)
async def form_rss_url(message: Message, state: FSMContext):
    rss_url = message.text
    await state.update_data(rss_url=rss_url)
    await state.set_state(states.AddResource.is_rss_valid)
    await message.answer("Проверяем источник...")
    data = fetch_data(rss_url)
    if not data:
        await message.answer("Невозможно прочитать источник.")
        await state.clear()
    else:
        helper = DBHelper()
        current_user = helper.get_user(user_id=message.from_user.id)
        resource = helper.get_resource(url=rss_url)
        if not resource:
            resource = Resource(url=rss_url)
            helper.add_resource(resource)
            await message.answer("Источник добавлен в базу.")
        subscription = Subscription(user=current_user, resource=resource)
        helper.add_subscription(subscription)
        await state.clear()
        await message.answer("Подписка на источник успешно оформлена!")


@router.message(Command("get_news_1h"))
async def get_news_1h(message: Message):
    helper = DBHelper()
    user_id = message.from_user.id
    current_user = helper.get_user(user_id=user_id)
    for subscription in current_user.subscriptions:
        for item in helper.get_rss_items(subscription.resource):
            await message.answer(f"{hbold(item.title)}\n"
                                 f"{item.pub_date}\n"
                                 f"{item.description if item.description else 'Нет описания'}\n"
                                 f"{item.link}\n"
                                 )


@router.message(Command("get_news_24h"))
async def get_news_24h(message: Message):
    helper = DBHelper()
    user_id = message.from_user.id
    current_user = helper.get_user(user_id=user_id)
    for subscription in current_user.subscriptions:
        for item in helper.get_rss_items(subscription.resource, delta=datetime.timedelta(hours=24)):
            await message.answer(f"{hbold(item.title)}\n"
                                 f"{hitalic(item.pub_date)}\n"
                                 f"{item.description if item.description else 'Нет описания'}\n"
                                 f"{item.link}"
                                 )


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Нажмите добавить источник и отправьте ссылку на RSS-источник для получения новостей.")
