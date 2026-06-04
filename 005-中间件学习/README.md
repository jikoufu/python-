# 中间件学习目录

这个目录用于系统学习后端开发中最常用的中间件，按照依赖关系和使用频率排序：从容器化工具 Docker 开始，依次学习数据库 MySQL、缓存 Redis、代理服务器 Nginx、消息队列 RabbitMQ，最后到搜索引擎 Elasticsearch。

## 目录结构

```text
005-中间件学习/
├── README.md
├── 学习路径.md
├── 01-Docker/
├── 02-MySQL/
├── 03-Redis/
├── 04-Nginx/
├── 05-RabbitMQ/
├── 06-Elasticsearch/
└── 99-中间件面试题/
```

## 为什么这个顺序

| 顺序 | 中间件 | 原因 |
|------|--------|------|
| 1 | Docker | 后续所有中间件都用 Docker 启动，必须先学 |
| 2 | MySQL | 最基础的数据持久化，几乎所有项目都用 |
| 3 | Redis | 缓存、Session、分布式锁，使用频率极高 |
| 4 | Nginx | 反向代理、负载均衡，上线部署必备 |
| 5 | RabbitMQ | 异步解耦，高并发场景必备 |
| 6 | Elasticsearch | 全文搜索、日志分析，进阶场景使用 |

## 各模块概览

### 01-Docker

- 镜像与容器的概念
- 常用命令：`run`、`build`、`ps`、`exec`、`logs`
- Dockerfile 编写
- docker-compose 编排多容器
- 数据卷与网络
- 生产部署最佳实践

### 02-MySQL

- 数据库、表、字段的设计
- CRUD 基本操作
- 索引原理与优化
- 事务与 ACID
- 锁机制
- 主从复制
- 与 Python（SQLAlchemy）集成
- 本机 D 盘 MySQL 配置记录

学习文件：

- [02-MySQL/README.md](</D:/PycharmProjects/python后端学习/005-中间件学习/02-MySQL/README.md>)

### 03-Redis

- 五大数据结构及使用场景
- 持久化：RDB 与 AOF
- 缓存策略与缓存失效问题
- 分布式锁实现
- 发布订阅
- Redis Stream（轻量消息队列）
- 与 Python（aioredis）集成

学习文件：

- [03-Redis/README.md](</D:/PycharmProjects/python后端学习/005-中间件学习/03-Redis/README.md>)

### 04-Nginx

- 静态文件服务
- 反向代理配置
- 负载均衡策略
- HTTPS 配置
- gzip 压缩
- 限流配置
- 日志分析

### 05-RabbitMQ

- 消息队列解决的问题
- AMQP 核心概念：Exchange、Queue、Binding
- 四种 Exchange 类型
- 消息确认与持久化
- 死信队列
- 延迟队列
- 与 Python（aio-pika）集成

学习文件：

- [05-RabbitMQ/README.md](</D:/PycharmProjects/python后端学习/005-中间件学习/05-RabbitMQ/README.md>)

### 06-Elasticsearch

- 倒排索引原理
- 核心概念：Index、Document、Mapping
- 全文搜索与聚合查询
- 中文分词（IK 分词器）
- 与 Python（elasticsearch-py）集成
- Kibana 可视化

### 99-中间件面试题

- MySQL、Redis、MQ、Nginx、Docker、Elasticsearch 必问题
- 线上慢接口、中间件异常、数据不一致等综合排查题

学习文件：

- [99-中间件面试题/README.md](</D:/PycharmProjects/python后端学习/005-中间件学习/99-中间件面试题/README.md>)

## 推荐学习方式

每个中间件建议采用以下节奏：

1. 用 Docker 一键启动中间件，不在本机直接安装。
2. 先理解这个中间件解决什么问题。
3. 完成最小可运行示例。
4. 学习核心配置和调优参数。
5. 与 Python 后端集成，完成一个实际功能。

## 技术栈关系图

```text
用户请求
    ↓
Nginx（反向代理、负载均衡、HTTPS）
    ↓
FastAPI 应用
    ├── MySQL（持久化存储）
    ├── Redis（缓存、Session、分布式锁）
    ├── RabbitMQ（异步任务、解耦）
    └── Elasticsearch（全文搜索）
    
所有服务均通过 Docker 容器运行
```
