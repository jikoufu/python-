# Exchange 路由模型

RabbitMQ 的消息路由由 Exchange 决定。重点掌握 Direct、Fanout、Topic。

## 1. Direct Exchange

Direct 按 routing key 完全匹配。

```text
消息 routing_key = order.created
队列 binding_key = order.created
匹配成功，消息进入队列
```

适用场景：

- 点对点任务。
- 明确类型的业务事件。
- 订单创建、订单取消、支付成功。

## 2. Fanout Exchange

Fanout 是广播模式，不看 routing key，发给所有绑定队列。

适用场景：

- 系统通知。
- 广播事件。
- 一条消息多个服务都要处理。

例子：

```text
订单创建事件：
- 库存服务消费
- 优惠券服务消费
- 通知服务消费
- 日志服务消费
```

## 3. Topic Exchange

Topic 支持通配符匹配 routing key。

规则：

```text
* 匹配一个单词
# 匹配零个或多个单词
```

例子：

```text
routing_key = order.created
binding_key = order.*       可以匹配
binding_key = order.#       可以匹配
binding_key = *.created     可以匹配
binding_key = pay.*         不匹配
```

适用场景：

- 按业务类型分类路由。
- 多种事件统一管理。
- 日志按级别、模块路由。

## 4. Headers Exchange

Headers 按消息头匹配，实际项目中使用较少。

## 5. 路由模型对比

| Exchange | 路由方式 | 典型场景 |
|----------|----------|----------|
| Direct | routing key 完全匹配 | 明确任务类型 |
| Fanout | 广播给所有队列 | 通知、广播 |
| Topic | routing key 通配符 | 分类事件 |
| Headers | 消息头匹配 | 少用 |

## 6. 面试回答模板

```text
RabbitMQ 的生产者一般把消息发送到 Exchange，Exchange 根据绑定关系把消息路由到队列。
Direct 是 routing key 精确匹配，Fanout 是广播，Topic 支持通配符匹配。
实际业务中订单事件可以用 Topic，例如 order.created、order.paid、order.cancelled。
```

