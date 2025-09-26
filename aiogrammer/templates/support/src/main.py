import asyncio
import logging
from contextlib import suppress
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.state import TicketForm

from src.config import settings
from src.logger import setup_logging

def support_keyboard() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(text="Contact support", callback_data="support:start")
    return kb


async def on_startup() -> None:
    setup_logging()
    logging.getLogger(__name__).info("Support bot is starting...")


async def on_shutdown(dp: Dispatcher) -> None:
    logging.getLogger(__name__).info("Support bot is shutting down...")
    await dp.storage.close()


async def start_handler(message: Message) -> None:
    await message.answer(
        "Hello! I can help you contact our support team.\n"
        "Press the button below to start a brief ticket form.",
        reply_markup=support_keyboard().as_markup(),
    )


async def support_start(query: CallbackQuery, state) -> None:
    await query.message.edit_text("Please, enter a short topic for your issue (one line).")
    await state.set_state(TicketForm.topic)


async def ticket_topic(message: Message, state) -> None:
    await state.update_data(topic=message.text.strip())
    await message.answer("Got it. Now describe the problem in more detail.")
    await state.set_state(TicketForm.description)


async def ticket_description(message: Message, state, bot: Bot) -> None:
    data = await state.get_data()
    topic = data.get("topic")
    description = message.text or "(no text)"

    text = (
        "New support ticket:\n"
        f"Topic: {topic}\n"
        f"From: @{message.from_user.username or message.from_user.id}\n"
        f"Chat: {message.chat.id}\n\n"
        f"Description:\n{description}"
    )

    try:
        await bot.send_message(settings.SUPPORT_CHAT_ID, text)
        await message.answer("Thanks! Your ticket has been sent to our support team.")
    except Exception as e:
        logging.getLogger(__name__).exception("Failed to forward a ticket")
        await message.answer("Sorry, something went wrong while sending your ticket. Please try later.")

    await state.clear()


async def main() -> None:
    await on_startup()

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start_handler, CommandStart())
    dp.callback_query.register(support_start, F.data == "support:start")
    dp.message.register(ticket_topic, TicketForm.topic, F.text)
    dp.message.register(ticket_description, TicketForm.description, F.text)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        with suppress(Exception):
            await bot.session.close()
        await on_shutdown(dp)


if __name__ == "__main__":
    asyncio.run(main())