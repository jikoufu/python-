# SQL 基础与表设计

## 1. SQL 分类

| 分类 | 作用 | 示例 |
|------|------|------|
| DDL | 定义结构 | `CREATE TABLE`、`ALTER TABLE`、`DROP TABLE` |
| DML | 操作数据 | `INSERT`、`UPDATE`、`DELETE` |
| DQL | 查询数据 | `SELECT` |
| DCL | 权限控制 | `GRANT`、`REVOKE` |
| TCL | 事务控制 | `COMMIT`、`ROLLBACK` |

面试里通常不会这么死问，但你要知道 SQL 不只是 `SELECT`。

## 2. 建表模板

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username),
    UNIQUE KEY uk_email (email),
    KEY idx_status_created_at (status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

字段设计建议：

- 主键一般用 `BIGINT UNSIGNED AUTO_INCREMENT`。
- 金额不要用 `FLOAT`，用 `DECIMAL` 或整数分。
- 状态字段可以用 `TINYINT`，但要在文档里说明枚举含义。
- 时间字段建议保留 `created_at`、`updated_at`。
- 字符集用 `utf8mb4`。

## 3. CRUD

新增：

```sql
INSERT INTO users (username, email, password_hash)
VALUES ('zhangsan', 'zhangsan@example.com', 'hash_value');
```

查询：

```sql
SELECT id, username, email, status
FROM users
WHERE id = 1;
```

更新：

```sql
UPDATE users
SET status = 0
WHERE id = 1;
```

删除：

```sql
DELETE FROM users
WHERE id = 1;
```

真实项目中，很多业务会使用软删除：

```sql
ALTER TABLE users ADD COLUMN deleted_at DATETIME NULL;

UPDATE users
SET deleted_at = NOW()
WHERE id = 1;
```

## 4. 分页查询

普通分页：

```sql
SELECT id, username, email
FROM users
WHERE status = 1
ORDER BY id DESC
LIMIT 20 OFFSET 0;
```

深分页性能会变差，例如：

```sql
LIMIT 20 OFFSET 100000;
```

原因是 MySQL 仍然要扫描并丢弃前面大量数据。

更好的方式是游标分页：

```sql
SELECT id, username, email
FROM users
WHERE status = 1
  AND id < 100000
ORDER BY id DESC
LIMIT 20;
```

## 5. 关联查询

订单表：

```sql
CREATE TABLE orders (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    order_no VARCHAR(64) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_order_no (order_no),
    KEY idx_user_id_created_at (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

查询用户订单：

```sql
SELECT u.id, u.username, o.order_no, o.amount, o.status
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.id = 1
ORDER BY o.created_at DESC;
```

## 6. 表设计考虑维度

设计一张表时，从这些方面考虑：

| 维度 | 要问的问题 |
|------|------------|
| 业务实体 | 这张表表示什么对象？用户、订单、商品、日志？ |
| 主键 | 用自增 ID、雪花 ID，还是业务唯一键？ |
| 唯一性 | 哪些字段不能重复？手机号、订单号、邮箱？ |
| 查询模式 | 高频查询条件是什么？按用户查、按状态查、按时间查？ |
| 数据量 | 是万级、百万级，还是亿级？ |
| 变更频率 | 是频繁写入，还是读多写少？ |
| 历史保留 | 是否需要软删除、审计字段、操作记录？ |
| 扩展性 | 后续是否可能分库分表？ |

## 7. 必须掌握的表设计原则

- 不要把多个值塞进一个字段，例如 `tag_ids = "1,2,3"`。
- 不要把经常查询的字段设计得过长。
- 唯一约束交给数据库保证，不要只靠代码判断。
- 读多写少的字段可以适当加索引，写多的表要控制索引数量。
- 表名、字段名要稳定清晰，不要用拼音缩写。

