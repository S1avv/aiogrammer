import asyncio
import json
from typing import Iterable, Tuple, Optional


async def publish_text_messages(amqp_url: str, queue_name: str, messages: Iterable[Tuple[int, str]], *, durable: bool = True) -> int:
    try:
        from aio_pika import connect_robust, Message, DeliveryMode
    except Exception as e:
        raise RuntimeError("aio-pika is required for RabbitMQ broadcasting. Install with: pip install aio-pika") from e

    connection = await connect_robust(amqp_url)
    try:
        channel = await connection.channel()
        await channel.declare_queue(queue_name, durable=durable)

        count = 0
        for user_id, text in messages:
            payload = json.dumps({"user_id": user_id, "text": text})
            msg = Message(payload.encode("utf-8"), delivery_mode=DeliveryMode.PERSISTENT)
            await channel.default_exchange.publish(msg, routing_key=queue_name)
            count += 1
        return count
    finally:
        await connection.close()


async def run_worker(bot, amqp_url: str, queue_name: str, *, prefetch: int = 100, delay: float = 0.0, silent: bool = False, on_error: Optional[callable] = None) -> None:
    try:
        from aio_pika import connect_robust
    except Exception as e:
        raise RuntimeError("aio-pika is required for RabbitMQ broadcasting. Install with: pip install aio-pika") from e

    connection = await connect_robust(amqp_url)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=prefetch)
        queue = await channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(requeue=False):
                    try:
                        payload = json.loads(message.body.decode("utf-8"))
                        user_id = int(payload["user_id"])  # type: ignore
                        text = str(payload["text"])       # type: ignore
                        await bot.send_message(user_id, text, disable_notification=silent)
                        if delay:
                            await asyncio.sleep(delay)
                    except Exception as err:
                        if on_error:
                            try:
                                on_error(err, message.body)
                            except Exception:
                                pass
                        continue