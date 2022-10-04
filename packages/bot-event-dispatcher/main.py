import asyncio
from os import getenv
import functions_framework
import logging
from dotenv import load_dotenv
from telebot import logger
from flask import Request, make_response
from bot_event_dispatcher.dispatch_updates import dispatch_updates
import re


load_dotenv()

environment = getenv("ENV")
__WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")

if environment == "production":
    logger.setLevel(logging.INFO)
elif environment == "development":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

__TOKEN_PATH_REGEX = re.compile(r"^\/bot\/(\d{5,}:.+)$")


@functions_framework.http
def bot_event_dispatcher(request: Request):
    logger.debug(f"Received request: {request}")
    if request.method != "POST":
        logger.warn(f"Invalid request method {request.method}")
        return {
            "ok": False,
            "error_code": 405,
            "description": "Method Not Allowed",
        }, 405

    if request.headers.get("Content-Type") != "application/json":
        logger.warn(
            f"Request with invalid content type {request.headers.get('Content-Type')}"
        )
        return {
            "ok": False,
            "error_code": 415,
            "description": "Unsupported Media Type",
        }, 415

    path = __TOKEN_PATH_REGEX.match(request.path)

    if not path:
        logger.warn(f"Invalid request path {request.path}")
        return {
            "ok": False,
            "error_code": 400,
            "description": "Bad Request: Missing Token. Use /bot/<token> as path.",
        }, 400

    token = path.group(1)

    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != __WEBHOOK_SECRET:
        logger.warn(
            f"Invalid webhook secret token (X-Telegram-Bot-Api-Secret-Token={request.headers.get('X-Telegram-Bot-Api-Secret-Token')})"  # noqa: E501
        )
        return {
            "ok": False,
            "error_code": 403,
            "description": "Forbidden",
        }, 403

    asyncio.run(dispatch_updates(token, request.get_json()))

    response = make_response()

    response.headers.set("Access-Control-Allow-Origin", "api.telegram.org")
    response.headers.remove("Content-Type")

    return response, 204


__all__ = ["bot_event_dispatcher"]
