import time
from collections import defaultdict, deque
from typing import Deque, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, window_seconds: int = 10):

        self.limit = limit
        self.window = window_seconds
        self.user_buckets: Dict[int, Deque[float]] = defaultdict(deque)

    async def __call__(self, handler, event: TelegramObject, data):
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            now = time.monotonic()

            bucket = self.user_buckets[user_id]

            while bucket and now - bucket[0] > self.window:
                bucket.popleft()

            if len(bucket) >= self.limit:
                try:
                    await event.answer("Slow down, please. Anti-spam protection is active.")
                except Exception:
                    pass
                return
            bucket.append(now)
        return await handler(event, data)