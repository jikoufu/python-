# Redis 分布式锁与 Session

## 1. 为什么需要分布式锁

单机应用可以用线程锁，但多个服务实例同时运行时，线程锁只能管住当前进程，管不住其他机器。

分布式锁用于控制多个服务实例同时操作同一资源。

典型场景：

- 防止重复下单。
- 防止库存超卖。
- 防止定时任务多实例重复执行。
- 防止同一订单被多个消费者同时处理。

## 2. 基础加锁命令

```bash
SET lock:order:1001 abc123 NX EX 10
```

解释：

```text
SET：设置 key
lock:order:1001：锁的 key
abc123：锁的唯一值
NX = not exists，key 不存在才设置
EX = expire seconds，设置秒级过期时间
10：10 秒后自动过期
```

## 3. 为什么 value 要唯一

如果不校验 value，可能误删别人的锁。

错误场景：

```text
线程 A 加锁成功，但业务执行超过锁过期时间。
锁自动过期后，线程 B 加锁成功。
线程 A 执行完后直接 DEL 锁，把线程 B 的锁删了。
```

所以释放锁时必须判断 value 是不是自己的。

## 4. Lua 脚本释放锁

```python
import uuid

import redis.asyncio as redis

client = redis.from_url("redis://127.0.0.1:6379/0", decode_responses=True)


async def acquire_lock(resource: str, ttl: int = 10) -> str | None:
    key = f"lock:{resource}"
    token = str(uuid.uuid4())
    ok = await client.set(key, token, nx=True, ex=ttl)
    return token if ok else None


async def release_lock(resource: str, token: str) -> int:
    key = f"lock:{resource}"
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    return await client.eval(script, 1, key, token)
```

## 5. 分布式锁风险

| 风险 | 说明 | 处理 |
|------|------|------|
| 锁过期太短 | 业务没执行完，锁已经释放 | 合理 TTL，必要时续期 |
| 锁过期太长 | 服务异常后长时间阻塞 | 设置可接受的超时时间 |
| 误删锁 | 删除了别人的锁 | value 唯一 + Lua 校验 |
| 重试风暴 | 抢不到锁一直重试 | 加随机退避 |
| 业务不幂等 | 重复执行产生脏数据 | 业务层幂等 |

面试表达：

```text
Redis 分布式锁不能只写 SETNX。
正确做法是 SET key value NX EX ttl，value 用唯一 token，释放时用 Lua 脚本判断 token 一致再删除。
同时要考虑锁超时、续期、重试和业务幂等。
```

## 6. Redis Session

传统登录态可以存服务内存，但多实例部署时会有问题：

```text
用户第一次请求打到服务 A，Session 存在 A。
第二次请求打到服务 B，B 没有 Session，用户被认为未登录。
```

解决：Session 存 Redis。

```text
session:token -> user_id / user_info
```

示例：

```bash
SET session:abc123 '{"user_id": 1, "username": "zhangsan"}' EX 7200
GET session:abc123
DEL session:abc123
```

## 7. Session 测试点

- 登录成功后 Redis 是否写入 session。
- session 是否有过期时间。
- 退出登录后 session 是否删除。
- 多实例服务是否都能识别同一 session。
- Redis 异常时登录态如何处理。
- session 是否存在泄露敏感信息。

