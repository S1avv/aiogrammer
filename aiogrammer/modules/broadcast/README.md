# Broadcast Module

Helpers for mass messaging to users with batching and error handling.

## Install into your project
1) Add module via CLI
```
aiogrammer add-module -m broadcast -p <your-project>
```

## Usage
### Basic text broadcast
```python
from modules.broadcast import broadcast_text

user_ids = [123, 456, 789]
result = await broadcast_text(bot, user_ids, "Hello!")
print(result)  # {"sent": N, "failed": M, "errors": [..]}
```

### Using Broadcaster class
```python
from modules.broadcast import Broadcaster

bc = Broadcaster(bot)
await bc.text([123, 456], "Update available!", batch_size=50, delay=0.02, silent=True)
```

### Gate sending with roles or admin
- Combine with `modules.roles` (permission `broadcast.send`) or your own admin check.
```python
from modules.roles import Permissions

if not rbac.has_permission(message.from_user.id, Permissions.BROADCAST_SEND):
    await message.answer("Access denied.")
    return
await broadcast_text(bot, audience_ids, message.text)
```

## RabbitMQ (recommended for large-scale)
- Install RabbitMQ server and Python client: `pip install aio-pika`
- Enqueue tasks and run a worker to consume and send via bot.

### Enqueue messages
```python
from modules.broadcast import publish_text_messages

amqp_url = "amqp://guest:guest@localhost/"
queue_name = "broadcast_texts"
count = await publish_text_messages(amqp_url, queue_name, [(123, "Hello"), (456, "News!")])
print(f"Enqueued: {count}")
```

### Run worker
```python
from modules.broadcast import run_worker

await run_worker(bot, amqp_url="amqp://guest:guest@localhost/", queue_name="broadcast_texts", prefetch=200, delay=0.01, silent=True)
```

## API
- `broadcast_text(bot, user_ids, text, *, batch_size=30, delay=0.05, silent=False) -> dict`
- `Broadcaster.text(user_ids, text, *, batch_size=30, delay=0.05, silent=False) -> dict`
- `publish_text_messages(amqp_url, queue_name, messages[, durable=True]) -> int`
- `run_worker(bot, amqp_url, queue_name[, prefetch, delay, silent, on_error]) -> None`

## Files
- `utils.py` — batching and error handling helpers
- `__init__.py` — exports helpers
- `rabbitmq.py` — RabbitMQ enqueue and worker helpers (aio-pika)
- `module.yaml` — manifest