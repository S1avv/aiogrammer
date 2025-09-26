from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from typing import Set

from .keyboards import admin_menu_keyboard
from .config import ADMIN_IDS

router = Router(name="admin")


@router.message(F.text == "/admin")
async def admin_entry(message: Message) -> None:
    if message.from_user is None or message.from_user.id not in ADMIN_IDS:
        await message.answer("Access denied.")
        return
    await message.answer("Admin panel:", reply_markup=admin_menu_keyboard())


@router.callback_query(F.data.startswith("admin:"))
async def admin_menu(callback: CallbackQuery) -> None:
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("Access denied.", show_alert=True)
        return
    section = callback.data.split(":", 1)[1]
    await callback.message.edit_text(f"Selected: {section}", reply_markup=admin_menu_keyboard())
    await callback.answer()