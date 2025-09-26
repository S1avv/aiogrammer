from typing import Iterable, List, Sequence
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))


def chunks(seq: Sequence, size: int) -> List[Sequence]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


def paginate_keyboard(
    page: int,
    total_pages: int,
    prefix: str = "pg",
    extra_buttons: Iterable[InlineKeyboardButton] | None = None,
) -> InlineKeyboardMarkup:
    page = clamp(page, 1, max(1, total_pages))
    buttons = []

    # prev/next + first/last
    nav_row = []
    nav_row.append(InlineKeyboardButton(text="⏮️", callback_data=f"{prefix}:first"))
    nav_row.append(InlineKeyboardButton(text="◀️", callback_data=f"{prefix}:prev"))
    nav_row.append(InlineKeyboardButton(text=f"{page}/{total_pages or 1}", callback_data=f"{prefix}:noop"))
    nav_row.append(InlineKeyboardButton(text="▶️", callback_data=f"{prefix}:next"))
    nav_row.append(InlineKeyboardButton(text="⏭️", callback_data=f"{prefix}:last"))
    buttons.append(nav_row)

    # extras (e.g., random, refresh)
    if extra_buttons:
        buttons.append(list(extra_buttons))

    return InlineKeyboardMarkup(inline_keyboard=buttons)