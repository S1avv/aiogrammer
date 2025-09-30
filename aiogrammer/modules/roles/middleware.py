try:
    from aiogram import BaseMiddleware
except Exception:  # fallback import path if required
    from aiogram.dispatcher.middlewares.base import BaseMiddleware  # type: ignore

from .permissions import RolesRegistry


class RBACMiddleware(BaseMiddleware):
    def __init__(self, registry: RolesRegistry) -> None:
        super().__init__()
        self.registry = registry

    async def __call__(self, handler, event, data):
        data["rbac"] = self.registry
        return await handler(event, data)