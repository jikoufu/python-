# 03 消息队列（Kafka 为主，RabbitMQ 对比）

> **测开面试定位**：消息队列以 **Kafka** 为主线学习（分区/副本/消费组模型最有代表性，学透一个其他触类旁通），核心考点是消息「不丢、不重、不乱序」。
> 本目录当前保留了 **RabbitMQ** 的完整资料作为**对比参考**（路由模型、死信队列等概念 RabbitMQ 讲得更直观）。Kafka 专项文档待补充。
> 面试主线和必考题见上层 [学习路径.md 阶段3](../学习路径.md)。

---

RabbitMQ 是常见消息队列中间件，重点掌握异步解耦、削峰填谷、可靠投递、重复消费、死信队列和消息积压排查。

## 推荐学习顺序

1. [01-消息队列基础.md](</D:/PycharmProjects/python后端学习/005-中间件学习/05-RabbitMQ/01-消息队列基础.md>)
2. [02-RabbitMQ核心概念与启动.md](</D:/PycharmProjects/python后端学习/005-中间件学习/05-RabbitMQ/02-RabbitMQ核心概念与启动.md>)
3. [03-Exchange路由模型.md](</D:/PycharmProjects/python后端学习/005-中间件学习/05-RabbitMQ/03-Exchange路由模型.md>)
4. [04-消息可靠性与死信队列.md](</D:/PycharmProjects/python后端学习/005-中间件学习/05-RabbitMQ/04-消息可靠性与死信队列.md>)
5. [05-Python集成与测试点.md](</D:/PycharmProjects/python后端学习/005-中间件学习/05-RabbitMQ/05-Python集成与测试点.md>)

## 学完后你应该能做到

- 能解释 MQ 解决什么问题。
- 能启动 RabbitMQ 并进入管理后台。
- 能理解 Producer、Consumer、Exchange、Queue、Binding。
- 能区分 Direct、Fanout、Topic Exchange。
- 能解释消息丢失、重复消费、消息积压怎么处理。
- 能用 Python 发送和消费消息。
- 能从测试角度设计 MQ 场景测试。

