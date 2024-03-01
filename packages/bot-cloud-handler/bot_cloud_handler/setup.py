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
from motor.core import AgnosticClient
from beanie import init_beanie
import aiohttp
from redis.asyncio import Redis
from injector import Injector, Module, inject, singleton, provider
from typing import OrderedDict, Callable, Any, Optional
from collections.abc import Coroutine
from telethon import TelegramClient
from telebot.async_telebot import AsyncTeleBot
from telebot import types, formatter

from .config import CONFIG, Config
from bot_cloud_handler.core.services.rate_limiting import RateLimiting


logger = logging.getLogger("bot_cloud_handler")

__console_output = logging.StreamHandler(sys.stdout)
__console_output.setFormatter(formatter)

logger.addHandler(__console_output)
__CACHE_MAX_SIZE = 16

__MTPROTO_INSTANCES_CACHE: OrderedDict[str, TelegramClient] = OrderedDict()

__BOT_INSTANCES_CACHE: OrderedDict[str, AsyncTeleBot] = OrderedDict()


def get_mtproto_bot(
    config: Config,
) -> Callable[[Optional[str]], Coroutine[Any, Any, TelegramClient]]:
    async def _get_mtproto_bot(bot_token: Optional[str] = None) -> TelegramClient:
        if not bot_token:
            bot_token = config.master_bot_token
        session_name = bot_token.split(":")[0]
        bot = __MTPROTO_INSTANCES_CACHE.get(session_name)
        if bot is not None:
            __MTPROTO_INSTANCES_CACHE.move_to_end(session_name)
            return bot
        bot = await TelegramClient(
            session=(
                session_name if config.env.value == "dev" else f"/tmp/{session_name}"
            ),
            api_id=config.telegram_api.api_id,
            api_hash=config.telegram_api.api_hash,
            receive_updates=False,
        ).start(bot_token=bot_token)
        __MTPROTO_INSTANCES_CACHE[session_name] = bot

        if len(__MTPROTO_INSTANCES_CACHE) > __CACHE_MAX_SIZE:
            __MTPROTO_INSTANCES_CACHE.popitem(last=False)

        return bot

    return _get_mtproto_bot


def get_bot(
    config: Config,
) -> Callable[[Optional[str]], Coroutine[Any, Any, AsyncTeleBot]]:
    async def _get_bot(bot_token: Optional[str] = None) -> AsyncTeleBot:
        if not bot_token:
            bot_token = config.master_bot_token
        session = bot_token.split(":")[0]
        bot = __BOT_INSTANCES_CACHE.get(session)
        if bot is not None:
            __BOT_INSTANCES_CACHE.move_to_end(session)
            return bot

        bot = AsyncTeleBot(bot_token, parse_mode="MarkdownV2")

        async def update_listener(messages: list[types.Message]) -> None:
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

    return _get_bot


class GlobalInjectionModule(Module):
    @singleton
    @provider
    def provide_config(self) -> Config:
        return CONFIG

    @singleton
    @provider
    def provide_redis_client(self, config: Config) -> Redis:
        return Redis(
            host=config.redis.host,
            port=config.redis.port,
            password=config.redis.password,
            db=0,
            decode_responses=True,
            ssl=True,
        )

    @singleton
    @provider
    def provide_mongodb_client(self, config: Config) -> AgnosticClient:
        client: AgnosticClient = AsyncIOMotorClient(
            host=config.mongo_uri, serverSelectionTimeoutMS=5000
        )

        asyncio.run(init_beanie(database=client.db_name, document_models=[]))

        return client

    @provider
    def provide_http_client(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()


def setup_features(
    bot_instance: AsyncTeleBot, mtproto_bot_instance: TelegramClient
) -> None:
    assert isinstance(
        bot_instance, AsyncTeleBot
    ), f"TeleBot bot is not an AsyncTelebot, but {type(bot_instance)}"  # noqa: E501
    assert isinstance(
        mtproto_bot_instance, TelegramClient
    ), f"mtproto bot is not a TelegramClient, but {type(mtproto_bot_instance)}"  # noqa: E501

    from . import features

    class SetupBotsInjectionModule(Module):
        @singleton
        @provider
        def provide_bot(self) -> AsyncTeleBot:
            return bot_instance

        @singleton
        @provider
        def provide_mtproto_bot(self) -> TelegramClient:
            return mtproto_bot_instance

    class SetupRateLimitingInjectionModule(Module):
        @singleton
        @provider
        @inject
        def provide_rate_limiting(
            self, redis_client: Redis, config: Config, bot: AsyncTeleBot
        ) -> RateLimiting:
            return RateLimiting(redis_client=redis_client, config=config, bot=bot)

    injector = Injector(
        [
            GlobalInjectionModule(),
            SetupBotsInjectionModule(),
            SetupRateLimitingInjectionModule(),
        ]
    )

    for feature in features.__dict__.values():
        if callable(feature):
            injector.get(feature)


__all__ = ["get_bot", "get_mtproto_bot", "setup_features"]
