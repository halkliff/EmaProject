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
import logging
from typing import OrderedDict
from telethon import TelegramClient
from telebot.async_telebot import AsyncTeleBot
from telebot import logger as bot_logger, types, formatter


logger = logging.getLogger("bot_cloud_handler")

__console_output = logging.StreamHandler(sys.stdout)
__console_output.setFormatter(formatter)

logger.addHandler(__console_output)

__API_HASH = None
__API_ID = None
__MASTER_BOT_TOKEN = None
__ENVIRONMENT = None

try:
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()

    __API_HASH = getenv("API_HASH")
    __API_ID = getenv("API_ID")
    __MASTER_BOT_TOKEN = getenv("MASTER_BOT_TOKEN")
    __ENVIRONMENT = getenv("ENV")
    if not __API_HASH or not __API_ID or not __MASTER_BOT_TOKEN:
        raise Exception("Missing environment variables")
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(2)

__CACHE_MAX_SIZE = 16

__TELETHON_INSTANCES_CACHE: OrderedDict[str, TelegramClient] = OrderedDict()

__BOT_INSTANCES_CACHE: OrderedDict[str, AsyncTeleBot] = OrderedDict()


async def get_telethon_bot(bot_token: str | None = None) -> TelegramClient:
    if not bot_token:
        bot_token = __MASTER_BOT_TOKEN
    session = bot_token.split(":")[0]
    bot = __TELETHON_INSTANCES_CACHE.get(session)
    if bot is not None:
        __TELETHON_INSTANCES_CACHE.move_to_end(session)
        return bot
    bot = TelegramClient(
        session=session
        if __ENVIRONMENT == "development"
        else f"/tmp/ema-sessions/{session}",
        api_id=__API_ID,
        api_hash=__API_HASH,
        receive_updates=False,
        base_logger=bot_logger,
        catch_up=False,
    )
    bot = await bot.start(bot_token=bot_token)
    __TELETHON_INSTANCES_CACHE[session] = bot

    if len(__TELETHON_INSTANCES_CACHE) > __CACHE_MAX_SIZE:
        __TELETHON_INSTANCES_CACHE.popitem(last=False)

    return bot


async def get_bot(bot_token: str | None = None) -> AsyncTeleBot:
    if not bot_token:
        bot_token = __MASTER_BOT_TOKEN
    session = bot_token.split(":")[0]
    bot = __BOT_INSTANCES_CACHE.get(session)
    if bot is not None:
        __BOT_INSTANCES_CACHE.move_to_end(session)
        return bot

    bot = AsyncTeleBot(bot_token, parse_mode="MARKDOWN")

    async def update_listener(messages: list[types.Message]):
        for message in messages:
            if message.content_type == "text":
                logger.debug(
                    f'[DEBUG_MESSAGES] [BOT="{bot_token}"] {message.chat.first_name if message.chat.type == "private" else message.chat.title}: {message.text}',  # noqa: E501
                )

    bot.set_update_listener(update_listener)

    __BOT_INSTANCES_CACHE[session] = bot

    if len(__BOT_INSTANCES_CACHE) > __CACHE_MAX_SIZE:
        __BOT_INSTANCES_CACHE.popitem(last=False)

    await bot.get_me()

    return bot


def setup_features(bot: AsyncTeleBot, telethon_bot: TelegramClient):
    assert isinstance(
        bot, AsyncTeleBot
    ), f"TeleBot bot is not an AsyncTelebot, but {type(bot)}"  # noqa: E501
    assert isinstance(
        telethon_bot, TelegramClient
    ), f"Telethon bot is not a TelegramClient, but {type(telethon_bot)}"  # noqa: E501
    from . import features

    for feature in features.__dict__.values():
        if callable(feature):
            feature(bot=bot, telethon_bot=telethon_bot)


__all__ = ["get_bot", "get_telethon_bot", "setup_features"]
