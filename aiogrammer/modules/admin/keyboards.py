from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Dashboard", callback_data="admin:dashboard")],
        [InlineKeyboardButton(text="Users", callback_data="admin:users")],
        [InlineKeyboardButton(text="Settings", callback_data="admin:settings")],
    ])