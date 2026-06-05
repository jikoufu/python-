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

## 1.1 关键字一句话记忆（看多了就记住）

每个关键字只回答一个问题，记住它"负责啥"就够了：

| 关键字 | 一句话 | 回答的问题 |
|--------|--------|-----------|
| `select` | 要哪些列 | 返回什么 |
| `from` | 从哪张表 | 数据在哪 |
| `where` | 筛哪些行 | 要满足什么条件 |
| `order by` | 怎么排序 | `desc`降序 / `asc`升序 |
| `limit` | 取几条 | 限制数量（分页） |
| `offset` | 从第几条开始 | 跳过前面多少条 |
| `join ... on` | 连哪张表、靠什么连 | 多表关联 |
| `group by` | 按什么分组 | 分组统计时用 |
| `insert into ... values` | 往哪插、插什么 | 新增数据 |
| `update ... set` | 改哪张表、改成什么 | 修改数据 |
| `delete from` | 从哪张表删 | 删除数据 |

> 一条标准查询的"句式"永远是这个顺序：
> `select 列 from 表 where 条件 order by 排序 limit 数量`
> 把它当成一句话的固定语序：**选什么 → 从哪 → 筛哪些 → 怎么排 → 要几条**。

## 2. 建表模板

```sql
create table users (                              -- create table 表名 (...)：新建一张表
    id bigint unsigned not null auto_increment,   -- bigint大整数; unsigned无负数; not null不可空; auto_increment自动+1
    username varchar(50) not null,                -- varchar(50)：变长字符串，最多50字符
    email varchar(100) not null,                  -- not null：这列必须有值，不能留空
    password_hash varchar(255) not null,
    status tinyint not null default 1,            -- tinyint小整数(存状态); default 1：不填时默认值为1
    created_at datetime not null default current_timestamp,  -- datetime日期时间; default current_timestamp：默认存"此刻"
    updated_at datetime not null default current_timestamp on update current_timestamp,  -- on update：每次改这行就自动更新成当前时间
    primary key (id),                             -- primary key 主键：唯一标识每一行，不重复不为空
    unique key uk_username (username),            -- unique key 唯一索引：保证 username 不重复
    unique key uk_email (email),                  -- 同理，邮箱也不能重复
    key idx_status_created_at (status, created_at) -- key 普通索引：给(status,created_at)加索引，加速查询
) engine=InnoDB default charset=utf8mb4;          -- engine=InnoDB：存储引擎(支持事务); charset=utf8mb4：字符集(能存emoji)
```

> 一行字段的读法（以 id 为例）：**列名 + 数据类型 + 各种约束**。
> `id bigint unsigned not null auto_increment` = "有个叫 id 的列，是大整数，不能为负，不能为空，自动递增"。

字段设计建议：

- 主键一般用 `BIGINT UNSIGNED AUTO_INCREMENT`。
- 金额不要用 `FLOAT`，用 `DECIMAL` 或整数分。
- 状态字段可以用 `TINYINT`，但要在文档里说明枚举含义。
- 时间字段建议保留 `created_at`、`updated_at`。
- 字符集用 `utf8mb4`。

## 3. CRUD

新增：

```sql
insert into users (username, email, password_hash)        -- insert into 表名(列1, 列2, 列3)：往哪张表的哪几列插入
values ('zhangsan', 'zhangsan@example.com', 'hash_value'); -- values (值1, 值2, 值3)：对应上面列的值，顺序要一一对应
```

查询：

```sql
select id, username, email, status   -- select：要返回哪些列（字段）。写 * 表示所有列
from users                           -- from：从哪张表查
where id = 1;                        -- where：筛选条件，只要满足条件（id=1）的行
```

> 读这条的顺序其实是：先 `from users`（去 users 表）→ 再 `where id=1`（挑出 id=1 的行）→ 最后 `select ...`（把这几列返回给你）。
> 虽然写的时候 select 在最前面，但执行时 from/where 先发生。

更新：

```sql
update users      -- update 表名：要改哪张表
set status = 0    -- set 列=值：把哪个字段改成什么（可改多个，逗号隔开）
where id = 1;     -- where：改哪些行！⚠️ 不写 where 会改全表，切记
```

删除：

```sql
delete from users   -- delete from 表名：从哪张表删行
where id = 1;        -- where：删哪些行！⚠️ 同样，不写 where 会删光全表
```

真实项目中，很多业务会使用软删除：

```sql
alter table users add column deleted_at datetime null;  -- alter table：改表结构；add column：加一个"删除时间"字段

update users                  -- 软删除 = 不真删，只打个"删除时间"标记
set deleted_at = now()        -- now()：当前时间。有值就代表"已删除"
where id = 1;                 -- 之后查询时加 where deleted_at is null 就能过滤掉"已删"的
```

## 4. 分页查询

普通分页：

```sql
select id, username, email   -- 要返回的列
from users                   -- 从 users 表
where status = 1             -- 只要 status=1（正常状态）的行
order by id desc             -- order by 列 desc：按 id 倒序排（desc 降序，asc 升序）
limit 20 offset 0;           -- limit 20：最多取 20 条；offset 0：从第 0 条开始（即第一页）
```

深分页性能会变差，例如：

```sql
limit 20 offset 100000;
```

原因是 MySQL 仍然要扫描并丢弃前面大量数据。

更好的方式是游标分页：

```sql
select id, username, email
from users
where status = 1
  and id < 100000     -- 关键：用"上一页最后一条的id"作为起点，直接跳过，不用 offset 扫描
order by id desc
limit 20;             -- 只取20条。因为有索引能直接定位 id<100000，所以再深也快
```

## 5. 关联查询

订单表：

```sql
create table orders (
    id bigint unsigned not null auto_increment,
    user_id bigint unsigned not null,                 -- 外键含义：这笔订单属于哪个用户(对应 users.id)
    order_no varchar(64) not null,                    -- 订单号
    amount decimal(10, 2) not null,                   -- decimal(10,2)：金额专用类型，共10位、2位小数，不丢精度
    status tinyint not null default 1,
    created_at datetime not null default current_timestamp,
    primary key (id),
    unique key uk_order_no (order_no),                -- 订单号唯一
    key idx_user_id_created_at (user_id, created_at)  -- 给"按用户+时间查订单"加索引(高频查询)
) engine=InnoDB default charset=utf8mb4;
```

查询用户订单：

```sql
select u.id, u.username, o.order_no, o.amount, o.status  -- u.xx 取 users 的列，o.xx 取 orders 的列
from users u                       -- from users u：给 users 起个别名叫 u（少打字）
join orders o on u.id = o.user_id  -- join orders o：再连上 orders 表(别名 o)；on：两表用什么关联（用户id=订单的用户id）
where u.id = 1                     -- 筛选：只看 id=1 这个用户
order by o.created_at desc;        -- 按订单创建时间倒序（最新的在前）
```

> JOIN 的本质：把两张表按 `on` 的条件"拼"成一张大表，再查。
> 这里就是"把用户和他的订单拼起来"，所以能一次查出"某用户 + 他的每一笔订单"。

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

