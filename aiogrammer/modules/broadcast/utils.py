import asyncio
from typing import Iterable, Dict, Any


async def broadcast_text(bot, user_ids: Iterable[int], text: str, *, batch_size: int = 30, delay: float = 0.05, silent: bool = False) -> Dict[str, Any]:
    totals: Dict[str, Any] = {"sent": 0, "failed": 0, "errors": []}
    ids = list(user_ids)
    for i in range(0, len(ids), batch_size):
        batch = ids[i:i + batch_size]
        tasks = [bot.send_message(uid, text, disable_notification=silent) for uid in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                totals["failed"] += 1
                totals["errors"].append(str(r))
            else:
                totals["sent"] += 1
        if delay:
            await asyncio.sleep(delay)
    return totals


class Broadcaster:
    def __init__(self, bot) -> None:
        self.bot = bot

    async def text(self, user_ids: Iterable[int], text: str, *, batch_size: int = 30, delay: float = 0.05, silent: bool = False) -> Dict[str, Any]:
        return await broadcast_text(self.bot, user_ids, text, batch_size=batch_size, delay=delay, silent=silent)