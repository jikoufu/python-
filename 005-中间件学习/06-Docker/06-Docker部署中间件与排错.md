# 06 Docker 部署中间件与排错

## 学习目标

学完这一节，你需要掌握：

- 用 Docker 启动常见中间件。
- 如何查看日志和排查问题。
- 常见错误怎么定位。
- 学习阶段应该怎么管理容器。

## MySQL

```bash
docker run -d --name mysql ^
  -p 3306:3306 ^
  -e MYSQL_ROOT_PASSWORD=123456 ^
  -e MYSQL_DATABASE=study_db ^
  -v mysql_data:/var/lib/mysql ^
  mysql:8.0
```

进入 MySQL：

```bash
docker exec -it mysql mysql -uroot -p123456
```

常见问题：

- 3306 端口被占用。
- 忘记设置 root 密码。
- 没挂载 volume，删除容器后数据丢。

## Redis

```bash
docker run -d --name redis ^
  -p 6379:6379 ^
  -v redis_data:/data ^
  redis:7 redis-server --appendonly yes
```

进入 Redis：

```bash
docker exec -it redis redis-cli
```

测试：

```bash
SET name docker
GET name
```

## Nginx

```bash
docker run -d --name nginx -p 8080:80 nginx:1.25
```

访问：

```text
http://127.0.0.1:8080
```

查看日志：

```bash
docker logs nginx
```

## RabbitMQ

```bash
docker run -d --name rabbitmq ^
  -p 5672:5672 ^
  -p 15672:15672 ^
  -e RABBITMQ_DEFAULT_USER=admin ^
  -e RABBITMQ_DEFAULT_PASS=123456 ^
  rabbitmq:3-management
```

管理页面：

```text
http://127.0.0.1:15672
```

账号：

```text
admin / 123456
```

## Elasticsearch

```bash
docker run -d --name es ^
  -p 9200:9200 ^
  -e "discovery.type=single-node" ^
  -e "xpack.security.enabled=false" ^
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" ^
  elasticsearch:8.13.0
```

测试：

```bash
curl http://127.0.0.1:9200
```

注意：

```text
Elasticsearch 比较吃内存，学习阶段可以先给 512m。
```

## 排错流程

### 1. 看容器是否运行

```bash
docker ps
docker ps -a
```

如果容器退出，看状态和日志。

### 2. 看日志

```bash
docker logs 容器名
docker logs -f --tail 100 容器名
```

### 3. 看端口是否映射

```bash
docker ps
```

确认：

```text
0.0.0.0:宿主机端口->容器端口
```

### 4. 进入容器检查

```bash
docker exec -it 容器名 bash
```

没有 bash 用：

```bash
docker exec -it 容器名 sh
```

### 5. 检查配置和环境变量

```bash
docker inspect 容器名
```

重点看：

- Env
- Mounts
- NetworkSettings
- Ports

## 常见错误

### 端口冲突

表现：

```text
Bind for 0.0.0.0:3306 failed
```

解决：

```bash
docker run -p 3307:3306 mysql:8.0
```

### 容器启动即退出

解决：

```bash
docker logs 容器名
```

根据日志看：

- 密码没设置。
- 配置错。
- 命令错。
- 权限问题。

### 数据丢失

原因：

```text
没有挂载 volume
或者执行了 docker compose down -v
```

解决：

```text
重要中间件必须挂载 volume。
```

### 容器之间连不上

检查：

- 是否在同一个 Docker 网络。
- 地址是否写服务名。
- 端口是否写容器内部端口。

compose 中连接 MySQL 应该写：

```text
db:3306
```

不是：

```text
127.0.0.1:3306
```

## 学习阶段建议

建议每个中间件都使用固定命名：

```text
mysql
redis
nginx
rabbitmq
es
```

查看：

```bash
docker ps -a
```

停止全部学习容器：

```bash
docker stop mysql redis nginx rabbitmq es
```

启动：

```bash
docker start mysql redis nginx rabbitmq es
```

## 本节重点

- 先看 `docker ps -a`，再看 `docker logs`。
- 端口冲突就换宿主机端口。
- 数据库和 Redis 要挂载 volume。
- compose 中容器互连用服务名。
- 不要随便执行 `docker compose down -v`。
