import logging
from dotenv import load_dotenv
from bot_cloud_handler.bot_setup import bot, telethon_bot, logger, bot_logger
from bot_cloud_handler import features

load_dotenv()


async def main():
    await bot.get_me()  # Ensures the bot API is ready
    await telethon_bot.get_me()  # First call to ensure the client is ready
    await bot.infinity_polling()


def start():
    from os import getenv
    global environment
    environment = getenv("ENV")
    if environment == "production":
        logger.setLevel(logging.INFO)
        bot_logger.setLevel(logging.INFO)
    elif environment == "development":
        logger.setLevel(logging.DEBUG)
        bot_logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
        bot_logger.setLevel(logging.ERROR)
    bot_logger.log(logging.INFO, "Starting bot")
    telethon_bot.loop.run_until_complete(main())


__all__ = ["start", "features"]

if __name__ == "__main__":
    start()
