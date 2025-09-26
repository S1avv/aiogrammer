# Anti-spam Module

Simple anti-spam middleware limiting messages per user in a short time window.

## Install into your project
1) Add module via CLI
```
aiogrammer add-module -m antispam -p <your-project>
```
2) Wire middleware and router
- Import `AntiSpamMiddleware` and add it to Dispatcher.message.middleware

Example (conceptually):
- dp.message.middleware(AntiSpamMiddleware(limit=5, window_seconds=10))

3) Test
- Try sending messages rapidly to see limiter warning

## Files
- middleware.py — rate limiting core
- __init__.py — exports middleware
- module.yaml — manifest