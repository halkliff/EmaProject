from bot_cloud_handler.bot_setup import bot, telethon_bot as tb, logger
from telebot.types import Message


@bot.message_handler(func=lambda _: True)
async def catchall(message: Message) -> None:
    logger.warning(
        f"Unexpected message from {message.from_user.id}: {message.text}",
    )
    await tb.send_message(
        message.from_user.id, "I am still under construction, try again later."
    )
