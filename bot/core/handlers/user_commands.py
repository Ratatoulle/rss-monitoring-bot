from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from monitoring import fetch_data
from database import DBHelper
from ..utils import Form
from ..keyboards import reply

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=reply.main)


@router.message(Command("add_resource"))
async def add_resource(message: Message, state: FSMContext):
    await state.set_state(Form.rss_link)
    await message.answer("Введите ссылку на источник:")


@router.message(Form.rss_link)
async def form_rss_link(message: Message, state: FSMContext):
    await state.update_data(rss_link=message.text)
    await state.set_state(Form.is_rss_valid)
    await message.answer("Проверяем источник...")
    data = fetch_data(message.text)
    if not data:
        await message.answer("Невозможно прочитать источник")
    else:
        helper = DBHelper()
        helper.add_rss_item(RSSItem())


@router.message(Command("get_news_1h"))
async def get_news_1h(message: Message):
    await message.answer("Введите ссылку на источник:")


@router.message(Command("get_news_24h"))
async def get_news_24h(message: Message):
    await message.answer("Введите ссылку на источник:")


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Нажмите добавить источник и отправьте ссылку на RSS-источник для получения новостей.")
