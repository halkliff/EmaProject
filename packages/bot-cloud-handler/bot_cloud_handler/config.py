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
from enum import StrEnum
from os import getenv
from icecream import ic
from typing import Literal, final, overload, Optional
from dataclasses import dataclass


class Env(StrEnum):
    DEV = "dev"
    PROD = "prod"


@dataclass(frozen=True)
@final
class RedisConfig:
    host: str
    port: int
    password: str | None

    # delays
    message_delay = 33  # 30 messages per second
    message_delay_user = 500  # = 60s / 0.5s = 120 messages per minute
    message_delay_group = 3000  # = 60s / 3s = 20 messages per minute


@dataclass(frozen=True)
@final
class TelegramAPIConfig:
    api_hash: str
    api_id: str


@dataclass(frozen=True)
class Config:
    telegram_api: TelegramAPIConfig
    master_bot_token: str
    env: Env

    redis: RedisConfig
    mongo_uri: str


CONFIG: Config


@overload
def get_env_var(key: str) -> str | None: ...


@overload
def get_env_var(key: str, *, default: str) -> str: ...


@overload
def get_env_var(
    key: str, *, default: Optional[str], allow_none: Optional[Literal[True]]
) -> str | None: ...


@overload
def get_env_var(
    key: str, *, default: Optional[str], allow_none: Literal[False]
) -> str: ...


def get_env_var(
    key: str, *, default: Optional[str] = None, allow_none: Optional[bool] = True
) -> str | None:
    value = getenv(key, default)
    if value is None and not allow_none:
        raise ValueError(f"Missing required environment variable {key}")
    return value


@overload
def get_number_env_var(key: str) -> int | None: ...


@overload
def get_number_env_var(key: str, *, default: int) -> int: ...


@overload
def get_number_env_var(
    key: str, *, default: Optional[int], allow_none: Optional[Literal[True]]
) -> int | None: ...


@overload
def get_number_env_var(
    key: str, *, default: Optional[int], allow_none: Literal[False]
) -> int: ...


def get_number_env_var(
    key: str,
    *,
    default: Optional[int] = None,
    allow_none: Optional[True | False] = True,
) -> int | None:
    value = get_env_var(
        key,
        default=str(default) if default is not None else None,
        allow_none=allow_none,
    )
    if value is not None:
        return int(value)

    return None


Truthy = ("true", True, "1", "yes", "y", "t", "on", "ok")


@overload
def get_bool_env_var(key: str) -> bool | None: ...


@overload
def get_bool_env_var(key: str, *, default: bool) -> bool: ...


@overload
def get_bool_env_var(
    key: str, *, default: Optional[bool], allow_none: Optional[Literal[True]]
) -> bool | None: ...


@overload
def get_bool_env_var(
    key: str, *, default: Optional[bool], allow_none: Literal[False]
) -> bool: ...


def get_bool_env_var(
    key: str,
    *,
    default: Optional[bool] = None,
    allow_none: Optional[True | False] = False,
) -> bool | None:
    default_val = str(default).lower() if default is not None else None

    value = get_env_var(
        key,
        default=default_val,
        allow_none=allow_none,
    )

    if value is not None:
        return value.lower() in Truthy

    return None


try:
    from dotenv import load_dotenv

    load_dotenv(override=True)

    telegram_api = TelegramAPIConfig(
        api_hash=get_env_var("API_HASH", default=None, allow_none=False),
        api_id=get_env_var("API_ID", default=None, allow_none=False),
    )

    redis = RedisConfig(
        host=get_env_var("REDIS_HOST", default=None, allow_none=False),
        port=get_number_env_var("REDIS_PORT", default=None, allow_none=False),
        password=get_env_var("REDIS_PASSWORD", default=None, allow_none=False),
    )

    env: Env
    match get_env_var("ENV", default="dev").lower():
        case Env.DEV.value:
            env = Env.DEV
        case Env.PROD.value:
            env = Env.PROD

    CONFIG = Config(
        telegram_api=telegram_api,
        master_bot_token=get_env_var(
            "MASTER_BOT_TOKEN", default=None, allow_none=False
        ),
        env=env,
        redis=redis,
        mongo_uri=get_env_var("MONGODB_URI", default=None, allow_none=False),
    )
except Exception as e:
    ic(e, file=sys.stderr)
    sys.exit(2)
