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
try:
    import ujson as json
except ImportError:
    import json  # type: ignore[no-redef]
import asyncio
import signal
from typing import Optional
from types import FrameType
from base64 import b64decode
import functions_framework
from cloudevents.http import CloudEvent
import logging
from telebot.types import Update
from telebot import logger as bot_logger

from bot_cloud_handler.config import CONFIG, Env
from bot_cloud_handler.setup import (
    get_bot,
    get_mtproto_bot,
    logger,
    setup_features,
)


match CONFIG.env:
    case Env.DEV:
        logger.setLevel(logging.DEBUG)
        bot_logger.setLevel(logging.DEBUG)
    case Env.PROD:
        logger.setLevel(logging.INFO)
        bot_logger.setLevel(logging.INFO)
    case _:
        logger.setLevel(logging.ERROR)
        bot_logger.setLevel(logging.ERROR)


__HANDLED_BOTS: set[str] = set()
__HANDLED_BOTS.add(CONFIG.master_bot_token)

bot_logger.info("Starting bot")

async_loop = asyncio.get_event_loop()
async_loop.run_until_complete(get_bot(CONFIG)(None))
async_loop.run_until_complete(get_mtproto_bot(CONFIG)(None))


@functions_framework.cloud_event
def bot_cloud_handler(event: CloudEvent) -> None:
    logger.debug(f"Received event: {event}")

    event_data = json.loads(b64decode(event.data["message"]["data"]).decode("utf-8"))

    logger.debug(f"Event data: {event_data}")

    if type(event_data["bot_token"]) is str:
        bot_token = event_data["bot_token"]
        __HANDLED_BOTS.add(bot_token)
    else:
        bot_token = None

    bot = async_loop.run_until_complete(get_bot(CONFIG)(bot_token))
    mtproto_bot = async_loop.run_until_complete(get_mtproto_bot(CONFIG)(bot_token))

    raw_updates = event_data["updates"]
    if raw_updates is None or (
        type(raw_updates) is not list and type(raw_updates) is not dict
    ):
        logger.warn(
            f"Skipping invalid updates[type={type(raw_updates)}]: {raw_updates}"
        )
        return

    setup_features(bot, mtproto_bot)

    updates = []

    if type(raw_updates) is list:
        for raw_update in raw_updates:
            updates.append(Update.de_json(raw_update))
    elif type(raw_updates) is dict:
        updates.append(Update.de_json(raw_updates))

    async_loop.run_until_complete(bot.process_new_updates(updates))
    return


__all__ = ["bot_cloud_handler"]


def _stop_mtproto_bot(bot_token: str) -> None:
    mtproto_bot = async_loop.run_until_complete(get_mtproto_bot(CONFIG)(bot_token))
    async_loop.run_until_complete(mtproto_bot.log_out())
    return


def stop(s: int, _: Optional[FrameType]) -> None:
    import sys

    bot_logger.warn("Stopping bot")
    for token in __HANDLED_BOTS:
        _stop_mtproto_bot(token)
    sys.exit(s)


for sig_num in [signal.SIGTERM, signal.SIGINT]:
    try:
        signal.signal(sig_num, stop)
    except (OSError, RuntimeError):
        pass
