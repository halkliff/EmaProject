#
# Copyright (C) Halk-lai Liff <halkliff@pm.me> &
# Werberth Lins <werberth.lins@gmail.com>, 2022-present
#
# Distributed under Apache v2.0(2004) License, found at the root tree of
# this source, by the name of LICENSE
# You can also find a copy of this license at GNU's site, as it follows
# <https://www.apache.org/licenses/LICENSE-2.0>
#
# THIS SOFTWARE IS PRESENTED AS-IS, WITHOUT ANY WARRANTY, OR LIABILITY FROM ITS AUTHORS
# EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
# IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
# ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
# IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
# WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
# THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
# GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
# USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
# DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
# PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
# EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGES.
#
import sys
import signal
import logging
import asyncio
from dotenv import load_dotenv
from bot_cloud_handler.setup import (
    get_bot,
    get_telethon_bot,
    logger,
    bot_logger,
    setup_features,
)
from bot_cloud_handler import features
from telebot.async_telebot import AsyncTeleBot
from telethon import TelegramClient

load_dotenv()

async_loop = asyncio.new_event_loop()
asyncio.set_event_loop(async_loop)


async def main(bot: AsyncTeleBot, tb: TelegramClient):
    await bot.get_me()  # Ensures the bot API is ready
    await tb.get_me()  # First call to ensure the client is ready
    await bot.delete_webhook(
        drop_pending_updates=False
    )  # Ensures that the polling will work
    await bot.remove_webhook()
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

    bot_logger.info("Starting bot")

    bot = async_loop.run_until_complete(get_bot())
    telethon_bot = async_loop.run_until_complete(get_telethon_bot())

    def stop():
        bot_logger.warn("Stopping bot")
        async_loop.run_until_complete(telethon_bot.log_out())
        sys.exit(0)

    signal.signal(
        signal.SIGTERM,
        lambda signum, frame: stop(),
    )

    try:
        setup_features(bot, telethon_bot)
        async_loop.run_until_complete(main(bot, telethon_bot))
    except KeyboardInterrupt:
        stop()


__all__ = ["start", "features"]

if __name__ == "__main__":
    start()
