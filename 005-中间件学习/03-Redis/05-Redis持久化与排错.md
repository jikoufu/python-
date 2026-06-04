# Redis 持久化与排错

## 1. Redis 持久化

Redis 数据在内存中，如果不开启持久化，服务重启后数据可能丢失。

常见持久化方式：

| 方式 | 全称 | 说明 |
|------|------|------|
| RDB | Redis Database Backup | 定期生成快照 |
| AOF | Append Only File | 记录每次写命令 |

## 2. RDB

RDB 是快照持久化。

优点：

- 文件紧凑。
- 恢复速度快。
- 适合备份。

缺点：

- 两次快照之间的数据可能丢失。

## 3. AOF

AOF 会把写命令追加到文件。

优点：

- 数据更完整。
- 丢失数据更少。

缺点：

- 文件通常比 RDB 大。
- 恢复速度可能慢一些。

常见策略：

```text
appendfsync always：每次写入都刷盘，最安全但最慢
appendfsync everysec：每秒刷盘，常用
appendfsync no：交给操作系统决定，性能好但风险高
```

## 4. 大 key 排查

大 key 是指 value 很大，或集合元素很多的 key。

风险：

- 读写慢。
- 删除阻塞。
- 网络传输大。
- 集群分片不均。

排查命令：

```bash
redis-cli --bigkeys
```

也可以分批扫描：

```bash
SCAN 0 COUNT 100
TYPE key_name
MEMORY USAGE key_name
```

## 5. 慢命令排查

查看慢日志：

```bash
SLOWLOG GET 10
```

常见慢操作：

- `KEYS *`
- 一次性 `HGETALL` 大 hash。
- 一次性 `LRANGE` 大 list。
- 删除大 key。

生产环境建议：

- 用 `SCAN` 替代 `KEYS`。
- 大集合分页读取。
- 大 key 拆分。
- 删除大 key 使用异步删除 `UNLINK`。

## 6. 缓存命中率低

可能原因：

- key 设计不稳定。
- TTL 太短。
- 业务读写模式不适合缓存。
- 缓存被频繁删除。
- 数据热点不明显。

排查方向：

```text
看缓存命中率 -> 看 key 过期策略 -> 看业务访问模式 -> 看是否频繁删除缓存
```

## 7. Redis 连接数过高

可能原因：

- 应用没有使用连接池。
- 请求量过高。
- 连接泄漏。
- 多个服务实例同时连接。

查看：

```bash
INFO clients
```

## 8. 测试开发排错模板

```text
如果接口慢且涉及 Redis，我会先确认 Redis 是否可连接，再看命中率、慢日志、大 key、连接数和网络延迟。
如果是数据不一致，会检查更新 DB 后是否删除缓存、缓存 TTL 是否合理、是否存在并发重建缓存的问题。
```

