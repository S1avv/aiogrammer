from __future__ import annotations

import random
from typing import List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from .utils import paginate_keyboard, clamp

router = Router(name="pagination")


DEMO_ITEMS: List[str] = [f"Item #{i+1}" for i in range(42)]


@router.message(Command("pagination_demo"))
async def pagination_demo(message: Message):
    page = 1
    total_pages = max(1, (len(DEMO_ITEMS) + 4) // 5)
    kb = paginate_keyboard(page, total_pages, prefix="pg", extra_buttons=[
        InlineKeyboardButton(text="🔄 Refresh", callback_data="pg:refresh"),
        InlineKeyboardButton(text="🎲 Random", callback_data="pg:random"),
    ])
    start = (page - 1) * 5
    end = start + 5
    text = "Demo pagination\n\n" + "\n".join(DEMO_ITEMS[start:end])
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.startswith("pg:"))
async def pagination_callbacks(callback: CallbackQuery):
    data = callback.data.split(":", 1)[1]

    # Get current page from message text "x/y" label
    # Fallback assume 1/1
    label = callback.message.reply_markup.inline_keyboard[0][2].text if callback.message.reply_markup else "1/1"
    try:
        page, total = map(int, label.split("/"))
    except Exception:
        page, total = 1, 1

    if data == "noop":
        await callback.answer()
        return
    if data == "refresh":
        await callback.answer("Refreshed")
    elif data == "random":
        await callback.answer("Random page")
        page = random.randint(1, total)
    elif data == "first":
        page = 1
    elif data == "prev":
        page = clamp(page - 1, 1, total)
    elif data == "next":
        page = clamp(page + 1, 1, total)
    elif data == "last":
        page = total

    start = (page - 1) * 5
    end = start + 5
    text = "Demo pagination\n\n" + "\n".join(DEMO_ITEMS[start:end])
    kb = paginate_keyboard(page, total, prefix="pg", extra_buttons=[
        InlineKeyboardButton(text="🔄 Refresh", callback_data="pg:refresh"),
        InlineKeyboardButton(text="🎲 Random", callback_data="pg:random"),
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()