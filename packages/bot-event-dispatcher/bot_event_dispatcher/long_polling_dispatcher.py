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
from telebot.apihelper import get_updates, ApiException
import logging
import threading
import time
import traceback


__PROJECT_ID = None
__PUBSUB_TOPIC_ID = None
__PUBSUB_SUBSCRIPTION_ID = None
__PUSH_ENDPOINT = None
__ENVIRONMENT = None
__LOCAL_BOT_TOKEN = None

try:
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()

    __PROJECT_ID = getenv("PROJECT_ID")
    __PUBSUB_TOPIC_ID = getenv("PUBSUB_TOPIC_ID")
    __PUBSUB_SUBSCRIPTION_ID = getenv("PUBSUB_SUBSCRIPTION_ID")
    __PUSH_ENDPOINT = getenv("PUSH_ENDPOINT")
    __ENVIRONMENT = getenv("ENV")
    __LOCAL_BOT_TOKEN = getenv("LOCAL_BOT_TOKEN")
    if (
        not __PROJECT_ID
        or not __PUBSUB_TOPIC_ID
        or not __PUBSUB_SUBSCRIPTION_ID
        or not __PUSH_ENDPOINT
        or not __LOCAL_BOT_TOKEN
    ):
        raise Exception("Missing environment variables")
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(2)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(__PROJECT_ID, __PUBSUB_TOPIC_ID)

if __ENVIRONMENT == "development":
    logger.setLevel(logging.DEBUG)

logger.info("Starting bot event dispatcher")


def start() -> None:
    try:
        last_update_id = 0

        __stop_polling = threading.Event()
        logger.info("Started polling.")
        __stop_polling.clear()
        error_interval = 0.25
        interval = 0
        non_stop = True

        logger_level = logger.level

        while not __stop_polling.wait(interval):
            try:
                updates = get_updates(
                    token=__LOCAL_BOT_TOKEN,
                    offset=last_update_id + 1,
                    timeout=20,
                    long_polling_timeout=20,
                )

                if (len(updates) < 1):
                    continue

                for update in updates:
                    if update["update_id"] > last_update_id:
                        last_update_id = update["update_id"]

                data = json.dumps({
                    "bot_token": __LOCAL_BOT_TOKEN,
                    "updates": updates
                }).encode("utf-8")
                future = publisher.publish(topic=topic_path, data=data)

                logger.info(f"Published {future.result()} to {__PUBSUB_TOPIC_ID}")
                error_interval = 0.25
            except ApiException as e:
                if logger_level and logger_level >= logging.ERROR:
                    logger.error("Polling exception: %s", str(e))
                if logger_level and logger_level >= logging.DEBUG:
                    logger.error("Exception traceback:\n%s", traceback.format_exc())
                if not non_stop:
                    __stop_polling.set()
                    logger.info("Exception occurred. Stopping.")
                else:
                    logger.info(
                        "Waiting for {0} seconds until retry".format(error_interval)
                    )
                    time.sleep(error_interval)
                    error_interval *= 2
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received.")
                __stop_polling.set()
                sys.exit(1)
            except Exception as e:
                raise e
        logger.info("Stopped polling.")
    except BaseException as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    start()
