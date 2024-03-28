from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv


@dataclass
class Bot:
    token: str
    admin_id: int


@dataclass
class Settings:
    bot: Bot


def get_settings():
    load_dotenv()

    return Settings(
        bot=Bot(
            token=getenv("BOT_TOKEN"),
            admin_id=int(getenv("ADMIN_ID")),
        )
    )


settings = get_settings()
