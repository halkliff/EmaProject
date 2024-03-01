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
import sys
from google.cloud import pubsub_v1
from telebot import logger
import logging


__PROJECT_ID = None
__PUBSUB_TOPIC_ID = None
__ENVIRONMENT = None

try:
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()

    __PROJECT_ID = getenv("PROJECT_ID")
    __PUBSUB_TOPIC_ID = getenv("PUBSUB_TOPIC_ID")
    __ENVIRONMENT = getenv("ENV")
    if not __PROJECT_ID or not __PUBSUB_TOPIC_ID:
        raise Exception("Missing environment variables")
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(2)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(__PROJECT_ID, __PUBSUB_TOPIC_ID)

if __ENVIRONMENT == "development":
    logger.setLevel(logging.DEBUG)


async def dispatch_updates(bot_token: str, updates: list) -> None:
    logger.debug(f"Dispatching updates for bot {bot_token}: {updates}")
    data = json.dumps({"bot_token": bot_token, "updates": updates}).encode("utf-8")
    future = publisher.publish(
        topic=topic_path, data=data
    )

    logger.info(f"Published {future.result()} to {__PUBSUB_TOPIC_ID}")
