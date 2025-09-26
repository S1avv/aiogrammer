# Pagination Module

Inline pagination helpers and demo with various navigation extras.

## Install into your project
1) Add module via CLI
```
aiogrammer add-module -m pagination -p <your-project>
```
2) Wire router
- Import and include `router` in your Dispatcher

3) Try demo
- Send `/pagination_demo` to see paginated list with buttons:
  - ⏮️ First, ◀️ Prev, ▶️ Next, ⏭️ Last
  - 🔄 Refresh, 🎲 Random

## API
- utils.paginate_keyboard(page, total_pages, prefix="pg", extra_buttons=None) -> InlineKeyboardMarkup
- utils.chunks(seq, size) -> list of chunks
- utils.clamp(x, lo, hi) -> int

## Files
- handlers.py — demo handlers and callbacks
- utils.py — keyboard builder and helpers
- __init__.py — exports router and utils
- module.yaml — manifest