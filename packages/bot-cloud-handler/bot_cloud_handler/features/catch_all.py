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
from typing import Callable
from bot_cloud_handler.setup import logger
from telebot.types import Message
from telethon import TelegramClient
from telebot.async_telebot import AsyncTeleBot


def catchall(
    bot: AsyncTeleBot, telethon_bot: TelegramClient
) -> Callable[[Message], None]:
    @bot.message_handler(func=lambda _: True)
    async def handler(message: Message) -> None:
        logger.warning(
            f"Unexpected message from {message.from_user.id}: {message.text}",
        )
        await telethon_bot.send_message(
            message.from_user.id, "I am still under construction, try again later."
        )

    return handler
