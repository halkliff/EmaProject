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
import asyncio
from typing import Any
from os import getenv
import functions_framework
import logging
from dotenv import load_dotenv
from telebot import logger
from flask import Request, make_response, Response
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
def bot_event_dispatcher(request: Request) -> tuple[dict[str, Any] | Response, int]:
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
