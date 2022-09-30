import sys
import logging
from dotenv import load_dotenv
from telethon import TelegramClient
from telebot.async_telebot import AsyncTeleBot
from telebot import logger as bot_logger, types, formatter


load_dotenv()

logger = logging.getLogger("bot_cloud_handler")

__console_output = logging.StreamHandler(sys.stdout)
__console_output.setFormatter(formatter)

logger.addHandler(__console_output)


__API_HASH = None
__API_ID = None
__BOT_TOKEN = None

try:
    from os import getenv

    __API_HASH = getenv("API_HASH")
    __API_ID = getenv("API_ID")
    __BOT_TOKEN = getenv("BOT_TOKEN")
    if not __API_HASH or not __API_ID or not __BOT_TOKEN:
        raise Exception("Missing environment variables")
except Exception as e:
    import sys

    print(e, file=sys.stderr)

telethon_bot = TelegramClient(
    "bot", __API_ID, __API_HASH, receive_updates=False, base_logger=bot_logger
).start(bot_token=__BOT_TOKEN)

bot = AsyncTeleBot(__BOT_TOKEN, parse_mode="MARKDOWN")


async def update_listener(messages: list[types.Message]):
    for message in messages:
        if message.content_type == "text":
            logger.debug(
                f"[DEBUG_MESSAGES] {message.chat.first_name if message.chat.type == 'private' else message.chat.title}: {message.text}",  # noqa: E501
            )


bot.set_update_listener(update_listener)

__all__ = ["bot", "telethon_bot"]
