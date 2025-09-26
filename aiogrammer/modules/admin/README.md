# Admin Module

Admin panel with access control and a basic inline menu.

## Install into your project
1) Add module via CLI
```
aiogrammer add-module -m admin -p <your-project>
```
2) Wire router in your app (example)
- Import and include router in your Dispatcher
- Configure admin IDs in `modules/admin/config.py`

3) Use
- Send `/admin` — opens admin menu (Dashboard, Users, Settings, Anti-spam)

## Files
- handlers.py — handlers with access check
- keyboards.py — inline keyboard factory
- config.py — ADMIN_IDS configuration
- __init__.py — exports router
- module.yaml — manifest