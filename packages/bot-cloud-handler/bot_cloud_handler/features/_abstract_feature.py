
from abc import ABC, abstractmethod
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telethon import TelegramClient
from bot_cloud_handler.core.services.rate_limiting import RateLimiting


class AbstractFeature(ABC):
    __handler_name__: str

    def __init__(
        self,
        /,
        bot: AsyncTeleBot,
        mtproto_bot: TelegramClient,
        rate_limiting: RateLimiting,
    ):
        self.bot = bot
        self.mtproto_bot = mtproto_bot
        self.rate_limiting = rate_limiting
        self._setup_handler()

    @abstractmethod
    def _setup_handler(self) -> None: ...

    @abstractmethod
    async def __call__(self, message: Message) -> None: ...
