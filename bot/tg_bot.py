import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from core.settings import settings
from core.handlers import user_commands


async def main():
    bot = Bot(settings.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp.include_routers(
        user_commands.router,
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
