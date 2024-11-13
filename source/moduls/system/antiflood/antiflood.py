# -*- coding: utf8 -*-
from typing import Any, Awaitable, Callable, Dict
from datetime import datetime, timedelta

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = 2) -> None:
        self.limit = TTLCache(maxsize=10000, ttl=time_limit)
        self.time_limit = time_limit

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        current_time = datetime.now()
        if event.chat.id in self.limit:
            expire_time = self.limit[event.chat.id]
            remaining_time = (expire_time - current_time).total_seconds()
            if remaining_time > 0:
                await event.reply(
                    f"Пожалуйста, подождите {remaining_time:.1f} секунд!"
                )
                return

        self.limit[event.chat.id] = current_time + timedelta(seconds=self.time_limit)
        return await handler(event, data)