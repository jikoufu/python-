# Redis 基础与安装启动

## 1. Redis 是什么

Redis 是基于内存的 NoSQL 数据库，常用于缓存、计数器、排行榜、分布式锁、Session、简单消息队列。

核心特点：

- 数据主要放在内存里，读写快。
- 支持多种数据结构。
- 单线程执行命令，避免复杂锁竞争。
- 支持持久化，可以把数据保存到磁盘。
- 支持过期时间，适合做缓存。

## 2. Redis 解决什么问题

| 场景 | 说明 |
|------|------|
| 缓存 | 减少数据库查询压力 |
| Session | 保存登录态 |
| 分布式锁 | 控制多个服务同时操作同一资源 |
| 计数器 | 浏览量、点赞数、接口访问次数 |
| 排行榜 | 使用 ZSet |
| 限流 | 按 IP 或用户统计访问次数 |
| 简单队列 | 使用 List 或 Stream |

## 3. Docker 启动 Redis

```bash
docker run -d ^
  --name redis ^
  -p 6379:6379 ^
  -v redis_data:/data ^
  redis:7-alpine redis-server --appendonly yes
```

参数解释：

```text
-d = detached，后台运行
--name redis：容器名叫 redis
-p = publish，端口映射，宿主机 6379 -> 容器 6379
-v = volume，把数据挂载到 redis_data
--appendonly yes：开启 AOF 持久化
```

进入 Redis 命令行：

```bash
docker exec -it redis redis-cli
```

测试：

```bash
PING
```

返回：

```text
PONG
```

## 4. 常用基础命令

```bash
SET name zhangsan          # 设置 key
GET name                   # 获取 key
DEL name                   # 删除 key
EXISTS name                # 判断 key 是否存在
EXPIRE name 60             # 设置 60 秒过期
TTL name                   # 查看剩余过期时间
KEYS user:*                # 查 key，生产环境慎用
SCAN 0 MATCH user:* COUNT 100  # 分批扫描 key，生产更推荐
```

## 5. Redis 为什么快

面试回答要点：

```text
Redis 快主要因为数据在内存里，命令执行是单线程模型，避免了多线程锁竞争，同时网络层使用 I/O 多路复用。
但 Redis 不是所有操作都快，大 key、慢命令、阻塞操作仍然会导致性能问题。
```

## 6. 测试开发关注点

测试 Redis 不只是看能不能 `GET/SET`，还要关注：

- 缓存是否正确命中。
- 缓存过期后是否能重建。
- 数据库更新后缓存是否删除。
- 热点 key 失效时是否会压垮数据库。
- Redis 挂掉时接口是否有降级策略。
- 分布式锁是否会误删、死锁、超时。

