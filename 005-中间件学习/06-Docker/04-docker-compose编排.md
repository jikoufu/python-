# 04 docker compose 编排

## 学习目标

学完这一节，你需要掌握：

- docker compose 是什么。
- 为什么需要 compose。
- 如何一键启动 FastAPI + MySQL + Redis。
- compose 文件怎么写。
- 常用 compose 命令。

## docker compose 是什么

Docker 适合启动单个容器。

但真实项目通常有多个服务：

```text
FastAPI 应用
MySQL
Redis
Nginx
RabbitMQ
Elasticsearch
```

docker compose 用来管理多容器应用。

一个 `docker-compose.yml` 可以定义所有服务，然后一键启动。

## 基础结构

```yaml
services:
  app:
    image: myapp:latest

  db:
    image: mysql:8.0
```

## FastAPI + MySQL + Redis 示例

```yaml
services:
  app:
    build: .
    container_name: fastapi-app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://root:123456@db:3306/app_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: mysql:8.0
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: app_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7
    container_name: redis-cache
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  mysql_data:
  redis_data:
```

## 常用命令

启动：

```bash
docker compose up -d
```

查看服务：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs
docker compose logs -f app
```

停止并删除容器：

```bash
docker compose down
```

停止并删除容器和数据卷：

```bash
docker compose down -v
```

重新构建：

```bash
docker compose up -d --build
```

进入服务容器：

```bash
docker compose exec app bash
docker compose exec db mysql -uroot -p123456
```

## depends_on 注意点

`depends_on` 只能保证容器启动顺序，不保证服务已经完全可用。

例如 MySQL 容器启动了，但 MySQL 服务可能还没准备好。

更严谨可以加 healthcheck。

```yaml
db:
  image: mysql:8.0
  environment:
    MYSQL_ROOT_PASSWORD: 123456
    MYSQL_DATABASE: app_db
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
    interval: 10s
    timeout: 5s
    retries: 5
```

## 服务名就是域名

在 compose 网络里，服务名可以作为域名。

例如 app 连接 MySQL：

```text
db:3306
```

连接 Redis：

```text
redis:6379
```

不要写：

```text
127.0.0.1
```

因为容器里的 `127.0.0.1` 是容器自己。

## 本节重点

- docker compose 用来管理多个容器。
- compose 文件里服务名可以互相访问。
- `depends_on` 不等于服务可用。
- 数据库必须挂载 volume。
- `docker compose down -v` 会删除数据，慎用。
