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
from typing import Tuple
from time import time_ns
import asyncio
from injector import inject
from bot_cloud_handler.config import Config
from telebot.async_telebot import AsyncTeleBot
from redis.asyncio import Redis


class RateLimiting:
    @inject
    def __init__(self, redis_client: Redis, config: Config, bot: AsyncTeleBot):
        self.redis_client = redis_client
        self.config = config
        self.bot = bot

    async def should_delay_message(
        self, /, chat_type: str, chat_id: int
    ) -> Tuple[bool, int]:
        """
        Check if a message should be delayed.
        :param chat_type: The chat type.
        :param config: The config.
        :param last_sent_at: The last sent message timestamp.
        :return: A tuple of (should_delay, delay).
        """

        last_sent_at = await self.redis_client.get(
            f"bot:{self.bot.token}:updates:last_sent_at"
        )

        last_sent_at_chat = await self.redis_client.get(
            f"bot:{self.bot.token}:updates:chats:{chat_id}:last_sent_at"
        )

        now = int(time_ns() / 1e6)  # convert to milliseconds

        delay = self._get_delay(chat_type)

        try:
            global_delta = now - int(last_sent_at)
        except (ValueError, TypeError):
            global_delta = float("inf")  # type: ignore[assignment]
            # It doesn't matter here because infinity is beyond floats and ints

        try:
            chat_delta = now - int(last_sent_at_chat)
        except (ValueError, TypeError):
            chat_delta = float("inf")  # type: ignore[assignment]

        if chat_delta < global_delta < delay:
            return True, delay - chat_delta

        elif global_delta < delay:
            return True, delay - global_delta

        return False, 0

    async def delay_message(self, chat_type: str, chat_id: int) -> None:
        """
        Delay a message.
        :param chat_type: The chat type.
        :param chat_id: The chat id.
        """

        chat_delay = self._get_delay(chat_type)

        now = int(time_ns() / 1e6)  # convert to milliseconds

        should_delay, delay = await self.should_delay_message(
            chat_type=chat_type, chat_id=chat_id
        )

        if should_delay:
            await asyncio.sleep(delay)

        await self.redis_client.set(
            f"bot:{self.bot.token}:updates:last_sent_at",
            now,
            px=int(self.config.redis.message_delay),
            nx=True,
        )

        await self.redis_client.set(
            f"bot:{self.bot.token}:updates:chats:{chat_id}:last_sent_at",
            int(now),
            px=chat_delay,
            nx=True,
        )

    def _get_delay(self, chat_type: str) -> int:
        """
        Get the delay for a chat type.
        :param chat_type: The chat type.
        :param config: The config.
        :return: The delay.
        """

        match (chat_type):
            case "private":
                return self.config.redis.message_delay_user
            case _:
                return self.config.redis.message_delay_group
