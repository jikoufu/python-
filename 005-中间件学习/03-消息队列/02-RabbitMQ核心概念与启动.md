# RabbitMQ 核心概念与启动

## 1. 核心概念

| 概念 | 英文 | 作用 |
|------|------|------|
| 生产者 | Producer | 发送消息 |
| 消费者 | Consumer | 接收并处理消息 |
| 消息 | Message | 传递的数据 |
| 队列 | Queue | 存储消息 |
| 交换机 | Exchange | 接收消息并路由到队列 |
| 绑定 | Binding | Exchange 和 Queue 的路由关系 |
| 路由键 | Routing Key | 消息路由规则 |
| 虚拟主机 | Virtual Host | 逻辑隔离空间 |

## 2. Docker 启动 RabbitMQ

```bash
docker run -d ^
  --name rabbitmq ^
  -p 5672:5672 ^
  -p 15672:15672 ^
  -e RABBITMQ_DEFAULT_USER=admin ^
  -e RABBITMQ_DEFAULT_PASS=123456 ^
  rabbitmq:3-management
```

参数解释：

```text
-p 5672:5672：业务连接端口
-p 15672:15672：Web 管理后台端口
-e = environment，设置环境变量
rabbitmq:3-management：带管理后台的 RabbitMQ 镜像
```

管理后台：

```text
http://127.0.0.1:15672
```

账号：

```text
admin / 123456
```

## 3. 基本工作流程

```text
Producer -> Exchange -> Queue -> Consumer
```

说明：

1. 生产者不直接把消息发给队列。
2. 生产者先把消息发给 Exchange。
3. Exchange 根据 Binding 和 Routing Key 把消息路由到 Queue。
4. Consumer 从 Queue 中取消息处理。

## 4. 管理后台重点看什么

| 页面 | 关注内容 |
|------|----------|
| Overview | 总体连接数、队列数、消息速率 |
| Connections | 哪些应用连接了 RabbitMQ |
| Channels | 通道数量 |
| Exchanges | 交换机 |
| Queues | 队列、积压数量、消费速度 |
| Admin | 用户、权限、vhost |

测试排查时最常看 Queues：

- Ready：等待消费的消息数。
- Unacked：已经投递给消费者但还没 ACK 的消息数。
- Total：总消息数。

## 5. 常用排查命令

查看容器日志：

```bash
docker logs -f rabbitmq
```

进入容器：

```bash
docker exec -it rabbitmq bash
```

查看队列：

```bash
rabbitmqctl list_queues
```

查看连接：

```bash
rabbitmqctl list_connections
```

