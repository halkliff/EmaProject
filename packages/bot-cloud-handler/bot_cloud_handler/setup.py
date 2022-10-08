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
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from redis.asyncio import Redis
from dependency_injector import containers, providers
from typing import OrderedDict
from telethon import TelegramClient
from telebot.async_telebot import AsyncTeleBot
from telebot import logger as bot_logger, types, formatter

from bot_cloud_handler.core.services.rate_limiting import RateLimiting


logger = logging.getLogger("bot_cloud_handler")

__console_output = logging.StreamHandler(sys.stdout)
__console_output.setFormatter(formatter)

logger.addHandler(__console_output)

__API_HASH = None
__API_ID = None
__MASTER_BOT_TOKEN = None
__ENVIRONMENT = None
__REDIS_HOST = None
__REDIS_PORT = None
__REDIS_PASSWORD = None
__MONGODB_URI = None
# Delay in milliseconds between messages
__MESSAGE_DELAY = 33  # 30 messages per second
__MESSAGE_DELAY_USER = 500  # = 60s / 0.5s = 120 messages per minute
__MESSAGE_DELAY_GROUP = 3000  # = 60s / 3s = 20 messages per minute

try:
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()

    __API_HASH = getenv("API_HASH")
    __API_ID = getenv("API_ID")
    __MASTER_BOT_TOKEN = getenv("MASTER_BOT_TOKEN")
    __ENVIRONMENT = getenv("ENV")
    __REDIS_HOST = getenv("REDIS_HOST")
    __REDIS_PORT = getenv("REDIS_PORT")
    __REDIS_PASSWORD = getenv("REDIS_PASSWORD")
    __MONGODB_URI = getenv("MONGODB_URI")
    if (
        not __API_HASH
        or not __API_ID
        or not __MASTER_BOT_TOKEN
        or not __REDIS_HOST
        or not __REDIS_PORT
        or not __REDIS_PASSWORD
        or not __MONGODB_URI
    ):
        raise Exception("Missing environment variables")

    print(f"MongoDB URI: {__MONGODB_URI}")
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
        session=session if __ENVIRONMENT == "development" else f"/tmp/{session}",
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

    bot = AsyncTeleBot(bot_token, parse_mode="MarkdownV2")

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


_mongodb_client = AsyncIOMotorClient(__MONGODB_URI, serverSelectionTimeoutMS=5000)

asyncio.run(init_beanie(database=_mongodb_client.db_name, document_models=[]))

_redis_client = Redis(
    host=__REDIS_HOST,
    port=__REDIS_PORT,
    password=__REDIS_PASSWORD,
    db=0,
    decode_responses=True,
    ssl=True,
)


class InjectionContainer(containers.DeclarativeContainer):
    mongodb_client = providers.Object(_mongodb_client)
    redis_client = providers.Object(_redis_client)
    config = providers.Configuration()

    rate_limiting = providers.Singleton(
        RateLimiting, redis_client=redis_client, config=config
    )


mongodb_client = _mongodb_client
redis_client = _redis_client


def setup_features(bot_instance: AsyncTeleBot, telethon_bot_instance: TelegramClient):
    assert isinstance(
        bot_instance, AsyncTeleBot
    ), f"TeleBot bot is not an AsyncTelebot, but {type(bot_instance)}"  # noqa: E501
    assert isinstance(
        telethon_bot_instance, TelegramClient
    ), f"Telethon bot is not a TelegramClient, but {type(telethon_bot_instance)}"  # noqa: E501

    from . import features

    class SetupFeaturesContainer(InjectionContainer):
        bot = providers.Object(bot_instance)
        telethon_bot = providers.Object(telethon_bot_instance)

    di_container = SetupFeaturesContainer()
    di_container.config.from_dict(
        {
            "bot_token": bot_instance.token,
            "env": __ENVIRONMENT,
            "message_delay_user": __MESSAGE_DELAY_USER,
            "message_delay_group": __MESSAGE_DELAY_GROUP,
            "message_delay": __MESSAGE_DELAY,
        }
    )
    di_container.wire(
        modules=[
            __name__,
            *list(map(lambda f: f"{features.__name__}.{f}", features.__all__)),
        ]
    )

    for feature in features.__dict__.values():
        if callable(feature):
            feature()


__all__ = ["get_bot", "get_telethon_bot", "setup_features", "mongodb_client"]
