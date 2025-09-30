from __future__ import annotations

from typing import Dict, Set, Iterable


class Permissions:
    ADMIN_ACCESS = "admin.access"
    BROADCAST_SEND = "broadcast.send"
    USERS_BAN = "users.ban"
    USERS_VIEW = "users.view"


class RolesRegistry:
    def __init__(self, role_permissions: Dict[str, Set[str]] | None = None) -> None:
        self.role_permissions: Dict[str, Set[str]] = role_permissions or {
            "admin": {"*"},
            "moderator": {Permissions.BROADCAST_SEND, Permissions.USERS_BAN, Permissions.USERS_VIEW},
            "user": set(),
        }
        self.user_roles: Dict[int, Set[str]] = {}

    def grant_role(self, user_id: int, role: str) -> None:
        roles = self.user_roles.setdefault(user_id, set())
        roles.add(role)

    def revoke_role(self, user_id: int, role: str) -> None:
        roles = self.user_roles.get(user_id)
        if roles:
            roles.discard(role)

    def roles_of(self, user_id: int) -> Set[str]:
        return set(self.user_roles.get(user_id, set()))

    def set_role_permissions(self, role: str, permissions: Iterable[str]) -> None:
        self.role_permissions[role] = set(permissions)

    def has_permission(self, user_id: int, permission: str) -> bool:
        roles = self.user_roles.get(user_id, set())
        for role in roles:
            perms = self.role_permissions.get(role, set())
            if "*" in perms or permission in perms:
                return True
        return False


def has_permission(registry: RolesRegistry, user_id: int, permission: str) -> bool:
    return registry.has_permission(user_id, permission)


def require_permissions(registry: RolesRegistry, required: Iterable[str]):
    def decorator(handler):
        async def wrapped(event, *args, **kwargs):
            user = getattr(event, "from_user", None)
            uid = getattr(user, "id", None)
            if uid is None or not all(registry.has_permission(uid, p) for p in required):
                try:
                    if hasattr(event, "answer"):
                        await event.answer("Access denied.")
                except Exception:
                    pass
                return
            return await handler(event, *args, **kwargs)

        return wrapped

    return decorator