# Python 集成 RabbitMQ 与测试点

## 1. 安装依赖

```powershell
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m pip install aio-pika
```

`aio-pika` 是 Python 异步 RabbitMQ 客户端，适合 FastAPI 项目。

## 2. 生产者示例

```python
import json

import aio_pika


async def send_order_created(order_id: int, user_id: int):
    connection = await aio_pika.connect_robust(
        "amqp://admin:123456@127.0.0.1/"
    )

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "order.events",
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        message_body = {
            "event": "order.created",
            "order_id": order_id,
            "user_id": user_id,
        }

        message = aio_pika.Message(
            body=json.dumps(message_body).encode("utf-8"),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await exchange.publish(message, routing_key="order.created")
```

## 3. 消费者示例

```python
import json

import aio_pika


async def consume_order_created():
    connection = await aio_pika.connect_robust(
        "amqp://admin:123456@127.0.0.1/"
    )

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    exchange = await channel.declare_exchange(
        "order.events",
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )

    queue = await channel.declare_queue(
        "order.created.queue",
        durable=True,
    )

    await queue.bind(exchange, routing_key="order.created")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode("utf-8"))
                await handle_order_created(data)
```

## 4. 消费者为什么要设置 prefetch

```python
await channel.set_qos(prefetch_count=10)
```

含义：一个消费者最多同时拿 10 条未确认消息。

作用：

- 防止一个消费者一次拿太多消息。
- 让消息更均匀地分发给多个消费者。
- 避免消费者处理不过来导致大量 Unacked。

## 5. FastAPI 中常见用法

接口里不要直接执行耗时任务，而是发消息：

```python
from fastapi import FastAPI

app = FastAPI()


@app.post("/orders")
async def create_order():
    order = await create_order_in_mysql()
    await send_order_created(order.id, order.user_id)
    return {"order_id": order.id}
```

后台消费者异步处理：

```text
订单创建 -> 发 MQ -> 消费者扣库存 / 发通知 / 写日志
```

## 6. 自动化测试关注点

### 6.1 接口是否发出消息

步骤：

1. 调用创建订单接口。
2. 到 RabbitMQ 队列中检查是否产生消息。
3. 校验消息字段是否正确。

### 6.2 消费者是否正确处理

步骤：

1. 手动往队列发送测试消息。
2. 启动消费者。
3. 校验数据库状态是否变化。
4. 校验消息是否 ACK。

### 6.3 消费失败是否进入死信队列

步骤：

1. 构造非法消息。
2. 消费者处理失败。
3. 检查消息是否进入 DLQ。
4. 检查日志是否记录错误原因。

### 6.4 重复消费是否幂等

步骤：

1. 发送两条相同业务 ID 的消息。
2. 校验业务结果只执行一次。
3. 例如库存只扣一次，通知只发一次。

## 7. 面试表达

```text
我在测试 MQ 场景时，不只验证接口返回，还会验证消息是否正确投递、队列是否积压、消费者是否 ACK、失败消息是否进死信队列，以及重复消息是否幂等。
这类测试要覆盖生产者、MQ、消费者和下游落库结果。
```

