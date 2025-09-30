# Roles/Permissions (RBAC) Module

Granular roles/permissions with a simple RBAC registry and middleware.

## Install into your project
1) Add module via CLI
```
aiogrammer add-module -m roles -p <your-project>
```

## Usage
### Initialize registry and middleware
```python
from modules.roles import RolesRegistry, RBACMiddleware, Permissions

rbac = RolesRegistry()

# Grant roles
rbac.grant_role(123456789, "admin")  # user gets full access via "*"
rbac.grant_role(987654321, "moderator")  # limited permissions

# Wire middleware
dp.message.middleware(RBACMiddleware(rbac))
```

### Check permissions in handlers
```python
from aiogram import Router
from modules.roles import Permissions

router = Router()

@router.message()
async def broadcast_cmd(message, rbac):
    if not rbac.has_permission(message.from_user.id, Permissions.BROADCAST_SEND):
        await message.answer("Access denied.")
        return
    await message.answer("You are allowed to broadcast.")
```

### Optional: decorator for permission gating
```python
from modules.roles import require_permissions, Permissions

@router.message()
@require_permissions(rbac, [Permissions.BROADCAST_SEND])
async def send_broadcast(message):
    await message.answer("Broadcasting...")
```

## API
- `RolesRegistry` — in-memory store of user roles and role permissions
  - `grant_role(user_id, role)` / `revoke_role(user_id, role)`
  - `roles_of(user_id) -> set[str]`
  - `set_role_permissions(role, permissions)`
  - `has_permission(user_id, permission) -> bool` (supports `"*"` wildcard)
- `RBACMiddleware` — injects `rbac` into handler `data`
- `Permissions` — common permission constants
- `require_permissions(rbac, permissions)` — handler decorator for quick gating

## Files
- `permissions.py` — core RBAC registry and helpers
- `middleware.py` — RBAC middleware
- `__init__.py` — exports `RolesRegistry`, `RBACMiddleware`, `Permissions`, `require_permissions`
- `module.yaml` — manifest