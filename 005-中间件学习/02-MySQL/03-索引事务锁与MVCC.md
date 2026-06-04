# 索引、事务、锁与 MVCC

这是 MySQL 面试和实际排错的核心章节。

## 1. 索引是什么

索引是为了加快查询的数据结构。MySQL InnoDB 常用 B+Tree 索引。

可以简单理解为：

```text
没有索引：从第一行扫到最后一行
有索引：先通过树结构定位，再回表或直接返回数据
```

## 2. 常见索引类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 主键索引 | 唯一且非空 | `PRIMARY KEY(id)` |
| 唯一索引 | 字段不能重复 | `UNIQUE KEY uk_email(email)` |
| 普通索引 | 加速查询 | `KEY idx_status(status)` |
| 联合索引 | 多字段组合索引 | `KEY idx_user_status(user_id, status)` |
| 覆盖索引 | 查询字段都在索引里 | 不需要回表 |

## 3. 联合索引最左前缀

假设有索引：

```sql
KEY idx_user_status_created (user_id, status, created_at)
```

能用上索引：

```sql
WHERE user_id = 1

WHERE user_id = 1 AND status = 1

WHERE user_id = 1 AND status = 1 AND created_at > '2026-01-01'
```

不一定能完整用上索引：

```sql
WHERE status = 1

WHERE created_at > '2026-01-01'
```

原因：联合索引按从左到右的顺序组织数据，不能跳过最左边字段。

## 4. 索引失效场景

常见索引失效：

```sql
-- 对索引列使用函数
WHERE DATE(created_at) = '2026-06-04'

-- 左模糊匹配
WHERE username LIKE '%san'

-- 隐式类型转换
WHERE phone = 13800138000

-- OR 两边不是都有索引
WHERE username = 'a' OR email = 'b'

-- 不符合联合索引最左前缀
WHERE status = 1
```

改法示例：

```sql
-- 不推荐
WHERE DATE(created_at) = '2026-06-04'

-- 推荐
WHERE created_at >= '2026-06-04 00:00:00'
  AND created_at <  '2026-06-05 00:00:00'
```

## 5. EXPLAIN 怎么看

```sql
EXPLAIN
SELECT id, username
FROM users
WHERE email = 'a@example.com';
```

重点看：

| 字段 | 含义 | 判断 |
|------|------|------|
| type | 访问类型 | `const`、`ref`、`range` 较好，`ALL` 较差 |
| key | 实际使用的索引 | NULL 表示没用索引 |
| rows | 预估扫描行数 | 越少越好 |
| Extra | 额外信息 | `Using filesort`、`Using temporary` 要关注 |

面试回答模板：

```text
我会先用 EXPLAIN 看 SQL 的 type、key、rows、Extra。
如果是全表扫描，就检查 WHERE 条件是否有合适索引，是否存在函数、隐式转换、左模糊、联合索引顺序不合理。
如果 rows 很大，还要结合业务确认是否需要分页、覆盖索引或拆分查询。
```

## 6. 事务 ACID

| 特性 | 解释 |
|------|------|
| 原子性 Atomicity | 一个事务中的操作要么都成功，要么都失败 |
| 一致性 Consistency | 事务执行前后数据满足业务规则 |
| 隔离性 Isolation | 并发事务之间互相隔离 |
| 持久性 Durability | 提交后的数据不会因为宕机丢失 |

示例：

```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
```

失败时：

```sql
ROLLBACK;
```

## 7. 隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|----------|------|------------|------|
| READ UNCOMMITTED | 可能 | 可能 | 可能 |
| READ COMMITTED | 不会 | 可能 | 可能 |
| REPEATABLE READ | 不会 | 不会 | InnoDB 大多可避免 |
| SERIALIZABLE | 不会 | 不会 | 不会 |

MySQL InnoDB 默认是 `REPEATABLE READ`。

查看隔离级别：

```sql
SELECT @@transaction_isolation;
```

## 8. MVCC 是什么

MVCC 是多版本并发控制。它让读操作不用总是等待写锁，提高并发能力。

核心理解：

```text
写数据时生成新版本。
读数据时根据 Read View 判断当前事务能看到哪个版本。
这样普通 SELECT 可以读快照，不必阻塞正在写入的事务。
```

面试回答模板：

```text
MVCC 通过多版本数据和 Read View 实现一致性读，解决读写并发冲突。
在 InnoDB 中，普通 SELECT 通常是快照读，UPDATE/DELETE/SELECT FOR UPDATE 是当前读。
```

## 9. 锁

| 锁类型 | 说明 |
|--------|------|
| 表锁 | 锁整张表，并发低 |
| 行锁 | 锁具体行，并发高 |
| 间隙锁 Gap Lock | 锁索引区间，防止幻读 |
| 临键锁 Next-Key Lock | 行锁 + 间隙锁 |

注意：InnoDB 的行锁是基于索引实现的。如果 SQL 没有走索引，可能锁住更多数据。

## 10. 死锁怎么处理

死锁常见原因：

- 多个事务更新相同资源，但加锁顺序不一致。
- 事务太大，持锁时间太长。
- 没有合适索引，导致锁范围扩大。

处理方式：

- 保持固定的资源访问顺序。
- 缩短事务时间。
- 给查询条件加合适索引。
- 出现死锁后业务层做重试。

面试回答模板：

```text
我会先看死锁日志，确认两个事务分别持有什么锁、等待什么锁。
然后检查 SQL 是否走索引、事务是否过大、多个流程是否存在加锁顺序不一致。
修复上通常是补索引、缩短事务、统一更新顺序，并在业务层增加有限次数重试。
```

