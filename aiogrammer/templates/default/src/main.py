import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.config import settings
from src.logger import setup_logging


async def on_startup() -> None:
    setup_logging()
    logging.getLogger(__name__).info("Bot is starting...")


async def on_shutdown(dp: Dispatcher) -> None:
    logging.getLogger(__name__).info("Bot is shutting down...")
    await dp.storage.close()


async def start_handler(message: Message) -> None:
    await message.answer("Hello! ✨")


async def main() -> None:
    await on_startup()

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start_handler, CommandStart())

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        with suppress(Exception):
            await bot.session.close()
        await on_shutdown(dp)


if __name__ == "__main__":
    asyncio.run(main())