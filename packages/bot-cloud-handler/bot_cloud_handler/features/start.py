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
from typing import override
from bot_cloud_handler.core.services.rate_limiting import RateLimiting
from bot_cloud_handler.setup import logger
from telebot import logger as bot_logger
from injector import inject
from telebot.types import Message
from telethon import TelegramClient
from telebot.async_telebot import AsyncTeleBot

from ._abstract_feature import AbstractFeature


class StartFeature(AbstractFeature):
    __handler_name__: str = "start"

    @inject
    def __init__(
        self,
        bot: AsyncTeleBot,
        mtproto_bot: TelegramClient,
        rate_limiting: RateLimiting,
    ) -> None:
        super().__init__(bot, mtproto_bot, rate_limiting)

    @override
    def _setup_handler(self) -> None:
        logger.debug(
            f"Wired start handler with [bot={self.bot}] and [mtproto_bot={self.mtproto_bot}]"  # noqa: E501
        )

        @self.bot.message_handler(commands=[self.__handler_name__])
        async def _(message: Message) -> None:
            await self(message)

    @override
    async def __call__(self, message: Message) -> None:
        bot_logger.debug(f'Processing "/start": {message}')

        chat_type = (
            message.reply_to_message.chat.type
            if message.reply_to_message is not None
            else message.chat.type
        )

        chat_id = message.chat.id

        await self.rate_limiting.delay_message(chat_type, chat_id)

        await self.mtproto_bot.send_message(
            chat_id,
            "Hi!",
        )  # sends hi!
