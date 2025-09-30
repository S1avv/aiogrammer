import asyncio
import os
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv


async def start_handler(message: Message) -> None:
    await message.answer("Hello from multibot! ✨")


async def run_bot(token: str) -> None:
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        with suppress(Exception):
            await bot.session.close()


async def main() -> None:
    load_dotenv()

    raw = os.getenv("BOT_TOKENS", "").strip()
    tokens: list[str]

    if not raw:
        token = os.getenv("BOT_TOKEN")
        if not token:
            raise RuntimeError("BOT_TOKENS or BOT_TOKEN must be set. Provide comma-separated tokens in BOT_TOKENS or a single BOT_TOKEN.")
        tokens = [token]
    else:
        tokens = [t.strip() for t in raw.split(",") if t.strip()]
        if not tokens:
            raise RuntimeError("BOT_TOKENS is empty. Provide comma-separated tokens.")

    await asyncio.gather(*(run_bot(t) for t in tokens))


if __name__ == "__main__":
    asyncio.run(main())