from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from monitoring.monitoring import fetch_data
from database.database import DBHelper
from database.models import User, Resource, Subscription
from aiogram.utils.markdown import hbold, hitalic
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import datetime
from ..keyboards import reply
from ..utils import states

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    """
        /start command handler
    """
    new_user = User(id=message.from_user.id, name=message.from_user.full_name)
    helper = DBHelper()
    if helper.get_user(user_id=message.from_user.id):
        await message.answer(f"Нет необходимости в регистрации, вы уже в базе данных.")
    else:
        helper.add_user(new_user)
        await message.answer(f"Привет, {message.from_user.full_name}!"
                             f"Запись о тебе успешно занесена в базу данных.")


@router.message(Command("add_resource"))
async def add_resource(message: Message, state: FSMContext):
    """
        /add_resource command handler
    """
    await state.set_state(states.AddResource.rss_url)
    await message.answer("Введите ссылку на источник")


@router.message(states.AddResource.rss_url)
async def get_rss_url(message: Message, state: FSMContext):
    """
        Method for handling state, when user sends URL of RSS resource
    """
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


async def get_news_common(message: Message, state: FSMContext):
    """
        Method for asking user how he wants the news to be displayed: all or separately.
        Common means for both (get_news_1h and get_news_24h) commands
    """
    await state.set_state(states.GetNews.all_or_separately)
    await message.answer("Вывести новости из всех источников или из отдельного?", reply_markup=reply.separate_or_all)


@router.message(states.GetNews.all_or_separately, F.text.casefold() == "отдельный источник")
async def separate_resource(message: Message, state: FSMContext):
    """
        Method for handling state, when user chooses separate resource option for displaying news
    """
    await state.set_state(states.GetNews.choose_resource)
    helper = DBHelper()
    subscriptions = list(helper.get_user_subscriptions(user_id=message.from_user.id))
    if not subscriptions:
        await message.answer("Вы не подписаны ни на один источник.")
    else:
        await message.answer("Выберите источник", reply_markup=reply.list_user_subscriptions(subscriptions))


@router.message(states.GetNews.choose_resource)
async def choose_resource(message: Message, state: FSMContext):
    """
        Method for handling state, when user specifies resource for displaying news
    """
    data = await state.get_data()
    await state.clear()
    helper = DBHelper()
    resource = helper.get_resource(message.text)
    if not resource:
        await message.answer("Невозможно прочитать источник.")
        await state.clear()
    rss_items = helper.get_rss_items(resource=resource, delta=data["delta"])
    if rss_items:
        for item in rss_items:
            await message.answer(f"{hbold(item.title)}\n"
                                 f"{hitalic(item.pub_date)}\n"
                                 f"{item.description if item.description else 'Нет описания'}\n"
                                 f"{item.link}\n",
                                 reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
                                 )
    else:
        await message.answer(f"Нет новостей для {resource.url} :(",
                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))


@router.message(states.GetNews.all_or_separately, F.text.casefold() == "все")
async def all_resources(message: Message, state: FSMContext):
    """
        Method for handling state, when user chooses all resources for displaying news
    """
    helper = DBHelper()
    data = await state.get_data()
    await state.clear()
    user_id = message.from_user.id
    current_user = helper.get_user(user_id=user_id)
    for subscription in current_user.subscriptions:
        rss_items = helper.get_rss_items(subscription.resource, delta=data["delta"])
        if rss_items:
            for item in rss_items:
                await message.answer(f"{hbold(item.title)}\n"
                                     f"{hitalic(item.pub_date)}\n"
                                     f"{item.description if item.description else 'Нет описания'}\n"
                                     f"{item.link}\n",
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
                                     )
        else:
            await message.answer(f"Нет новостей для {subscription.resource.url} :(",
                                 reply_markup=ReplyKeyboardRemove(remove_keyboard=True))


@router.message(Command("get_news_1h"))
async def get_news_1h(message: Message, state: FSMContext):
    """
        /get_news_1h command handler
    """
    await state.update_data(delta=datetime.timedelta(hours=1))
    await get_news_common(message=message, state=state)


@router.message(Command("get_news_24h"))
async def get_news_24h(message: Message, state: FSMContext):
    """
        /get_news_24h command handler
    """
    await state.update_data(delta=datetime.timedelta(hours=24))
    await get_news_common(message=message, state=state)


@router.message(Command("help"))
async def get_help(message: Message):
    """
        /help command handler
    """
    await message.answer("Нажмите добавить источник и отправьте ссылку на RSS-источник для получения новостей.")
