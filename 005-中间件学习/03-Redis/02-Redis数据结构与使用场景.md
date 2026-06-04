# Redis 数据结构与使用场景

## 1. String 字符串

String 是最常用的数据结构，可以存字符串、数字、JSON。

### 常用命令

```bash
SET user:1 "zhangsan"
GET user:1
DEL user:1

SET user:token abc123 EX 3600   # 设置值并指定 3600 秒过期
SETNX lock:order 1              # key 不存在才设置

INCR page:view                  # 自增 1
INCRBY page:view 10             # 自增 10
DECR stock:1001                 # 自减 1
```

### 使用场景

- 缓存用户信息。
- 接口访问计数。
- 商品库存扣减。
- 分布式锁基础命令。
- Token / 验证码缓存。

## 2. Hash 哈希

Hash 适合存对象字段。

### 常用命令

```bash
HSET user:1 name zhangsan age 20 email a@example.com
HGET user:1 name
HGETALL user:1
HDEL user:1 email
HINCRBY user:1 age 1
```

### 使用场景

- 用户对象。
- 商品对象。
- 配置项。

注意：Hash 很适合对象缓存，但字段太多或 value 太大也会形成大 key。

## 3. List 列表

List 是有序列表，可以从左侧或右侧插入/弹出。

### 常用命令

```bash
LPUSH tasks task1
LPUSH tasks task2
RPOP tasks

BRPOP tasks 30       # 阻塞等待 30 秒
LRANGE tasks 0 9     # 查看前 10 条
```

### 使用场景

- 简单任务队列。
- 最新消息列表。
- 操作日志队列。

注意：如果要做可靠消息队列，优先 RabbitMQ、Kafka 或 Redis Stream，不建议只靠 List。

## 4. Set 集合

Set 是无序不重复集合。

### 常用命令

```bash
SADD user:1:tags python ai test
SMEMBERS user:1:tags
SISMEMBER user:1:tags python

SINTER user:1:tags user:2:tags   # 交集
SUNION user:1:tags user:2:tags   # 并集
SDIFF user:1:tags user:2:tags    # 差集
```

### 使用场景

- 标签去重。
- 用户关注集合。
- 共同关注。
- 黑名单。

## 5. ZSet 有序集合

ZSet 是带分数的有序集合。

### 常用命令

```bash
ZADD leaderboard 100 zhangsan
ZADD leaderboard 200 lisi
ZREVRANGE leaderboard 0 9 WITHSCORES
ZRANK leaderboard zhangsan
ZINCRBY leaderboard 10 zhangsan
```

### 使用场景

- 排行榜。
- 热门文章。
- 延迟任务。
- 按分数排序的数据。

## 6. Stream 流

Stream 是 Redis 中更接近消息队列的数据结构。

### 常用命令

```bash
XADD order_stream * order_id 1001 user_id 1
XREAD COUNT 10 STREAMS order_stream 0

XGROUP CREATE order_stream group1 0 MKSTREAM
XREADGROUP GROUP group1 consumer1 COUNT 10 STREAMS order_stream >
XACK order_stream group1 message_id
```

### 使用场景

- 轻量消息队列。
- 事件日志。
- 异步任务流。

面试表达：

```text
Redis Stream 可以做轻量消息队列，支持消费者组和 ACK。
但如果系统对消息可靠性、重试、死信、路由模型要求较高，我会优先考虑 RabbitMQ 或 Kafka。
```

## 7. 结构选择总结

| 需求 | 推荐结构 |
|------|----------|
| 缓存单个值 | String |
| 缓存对象 | Hash 或 String(JSON) |
| 简单队列 | List |
| 去重集合 | Set |
| 排行榜 | ZSet |
| 延迟任务 | ZSet |
| 消息流 | Stream |

