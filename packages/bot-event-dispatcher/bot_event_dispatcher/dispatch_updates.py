try:
    import ujson as json
except ImportError:
    import json
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


async def dispatch_updates(bot_token: str, updates: list):
    logger.debug(f"Dispatching updates for bot {bot_token}: {updates}")
    data = json.dumps({"bot_token": bot_token, "updates": updates}).encode("utf-8")
    future = publisher.publish(
        topic=topic_path, data=data
    )

    logger.info(f"Published {future.result()} to {__PUBSUB_TOPIC_ID}")
