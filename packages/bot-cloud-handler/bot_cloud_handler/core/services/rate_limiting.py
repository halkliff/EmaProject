from typing import Tuple
from time import time_ns
import asyncio
from dependency_injector.wiring import Provide
from redis.asyncio import Redis


class RateLimiting:
    def __init__(
        self,
        redis_client: Redis = Provide["redis_client"],
        config: dict = Provide["config"],
    ):
        self.redis_client = redis_client
        self.config = config

    async def should_delay_message(
        self, /, chat_type: str, chat_id: str
    ) -> Tuple[bool, int]:
        """
        Check if a message should be delayed.
        :param chat_type: The chat type.
        :param config: The config.
        :param last_sent_at: The last sent message timestamp.
        :return: A tuple of (should_delay, delay).
        """

        bot_token = self.config["bot_token"]

        last_sent_at = await self.redis_client.get(
            f"bot:{bot_token}:updates:last_sent_at"
        )

        last_sent_at_chat = await self.redis_client.get(
            f"bot:{bot_token}:updates:chats:{chat_id}:last_sent_at"
        )

        now = int(time_ns() / 1e6)  # convert to milliseconds

        delay = self.get_delay(chat_type, self.config)

        try:
            global_delta = now - int(last_sent_at)
        except (ValueError, TypeError):
            global_delta = float("inf")

        try:
            chat_delta = now - int(last_sent_at_chat)
        except (ValueError, TypeError):
            chat_delta = float("inf")

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

        bot_token = self.config["bot_token"]

        chat_delay = self.get_delay(chat_type, self.config)

        now = int(time_ns() / 1e6)  # convert to milliseconds

        should_delay, delay = await self.should_delay_message(
            chat_type=chat_type, chat_id=chat_id
        )

        if should_delay:
            await asyncio.sleep(delay)

        await self.redis_client.set(
            f"bot:{bot_token}:updates:last_sent_at",
            now,
            px=int(self.config["message_delay"]),
            nx=True,
        )

        await self.redis_client.set(
            f"bot:{bot_token}:updates:chats:{chat_id}:last_sent_at",
            int(now),
            px=chat_delay,
            nx=True,
        )

    @staticmethod
    def get_delay(chat_type: str, config: dict) -> int:
        """
        Get the delay for a chat type.
        :param chat_type: The chat type.
        :param config: The config.
        :return: The delay.
        """

        delay_type: str

        match (chat_type):
            case "private":
                delay_type = "delay_user"
            case _:
                delay_type = "delay_group"

        return config[f"message_{delay_type}"]
