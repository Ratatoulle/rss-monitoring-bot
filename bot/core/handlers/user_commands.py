from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
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


@router.message(Command("get_news_1h"))
async def get_news_1h(message: Message):
    await message.answer("Введите ссылку на источник:")


@router.message(Command("get_news_24h"))
async def get_news_24h(message: Message):
    await message.answer("Введите ссылку на источник:")


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Нажмите добавить источник и отправьте ссылку на RSS-источник для получения новостей.")
