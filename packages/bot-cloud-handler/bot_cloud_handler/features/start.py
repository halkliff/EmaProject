from bot_cloud_handler.bot_setup import bot, telethon_bot as tb, logger
from telebot.types import Message


@bot.message_handler(commands=["start"])
async def start(message: Message) -> None:
    logger.debug(f"Processing \"/start\": {message}")
    chat_id = message.chat.id
    await tb.send_message(chat_id, "Hi!")  # sends hi!
