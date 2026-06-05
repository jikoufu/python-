# 02 Docker 常用命令

## 学习目标

学完这一节，你需要掌握：

- 镜像相关命令。
- 容器相关命令。
- 日志查看。
- 进入容器。
- 端口映射。
- 删除容器和镜像。

## 查看 Docker 版本

```bash
docker version
docker info
```

## 镜像命令

### 常见英文缩写

| 命令 / 参数 | 英文全称 | 中文含义 |
|-------------|----------|----------|
| `rmi` | remove image | 删除镜像 |
| `rm` | remove | 删除容器 |
| `ps` | process status | 查看容器进程状态 |
| `-d` | detached | 后台运行 |
| `-p` | publish | 发布端口 / 端口映射 |
| `-v` | volume | 挂载数据卷 |
| `-e` | environment | 设置环境变量 |
| `-it` | interactive + tty | 交互式终端 |

### 拉取镜像

```bash
docker pull nginx:1.25   # pull：拉取镜像
docker pull redis:7
docker pull mysql:8.0
```

### 查看本地镜像

```bash
docker images            # images：查看本地镜像列表
```

### 删除镜像

```bash
docker rmi nginx:1.25    # rmi = remove image，删除镜像
```

如果镜像被容器占用，需要先删除容器。

## 容器命令

### 启动一个 Nginx 容器

```bash
docker run -d --name web -p 8080:80 nginx:1.25
```

参数说明：

```text
run 创建并启动容器
-d detached，后台运行
--name web 容器名
-p publish，端口映射：宿主机 8080 映射到容器 80
nginx:1.25 使用的镜像
```

访问：

```text
http://127.0.0.1:8080
```

### 查看运行中容器

```bash
docker ps                # ps = process status，查看运行中容器
```

### 查看所有容器

```bash
docker ps -a             # -a = all，查看所有容器，包括已停止容器
```

### 停止容器

```bash
docker stop web          # stop：停止容器
```

### 启动已停止容器

```bash
docker start web         # start：启动已停止容器
```

### 重启容器

```bash
docker restart web       # restart：重启容器
```

### 删除容器

```bash
docker rm web            # rm = remove，删除容器
```

强制删除运行中容器：

```bash
docker rm -f web         # -f = force，强制删除运行中的容器
```

## 查看日志

```bash
docker logs web              # logs：查看日志
docker logs -f web           # -f = follow，持续跟踪日志
docker logs --tail 100 web   # tail：只看最后 100 行
```

常用：

```bash
docker logs -f --tail 100 web
```

## 进入容器

```bash
docker exec -it web bash     # exec：在容器内执行命令，-it = interactive + tty
```

如果容器没有 bash，可以用 sh：

```bash
docker exec -it web sh
```

## 查看容器详情

```bash
docker inspect web           # inspect：查看容器详细信息
```

查看 IP：

```bash
docker inspect web
```

## 拷贝文件

从宿主机拷贝到容器：

```bash
docker cp ./index.html web:/usr/share/nginx/html/index.html   # cp = copy
```

从容器拷贝到宿主机：

```bash
docker cp web:/var/log/nginx/access.log ./access.log
```

## 清理命令

删除停止的容器：

```bash
docker container prune       # prune：清理不用的资源
```

删除未使用镜像：

```bash
docker image prune
```

删除未使用数据卷：

```bash
docker volume prune
```

谨慎使用：

```bash
docker system prune
```

它会清理多个未使用资源。

## 常用启动命令示例

### Redis

```bash
docker run -d --name redis -p 6379:6379 redis:7
```

### MySQL

```bash
docker run -d ^
  --name mysql ^
  -p 3306:3306 ^
  -e MYSQL_ROOT_PASSWORD=123456 ^
  -e MYSQL_DATABASE=test_db ^
  -v mysql_data:/var/lib/mysql ^
  mysql:8.0
```

参数记忆：

```text
-d = detached，后台运行
--name = name，指定容器名
-p = publish，端口映射
-e = environment，设置环境变量
-v = volume，挂载数据卷
```

PowerShell 单行写法：

```bash
docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=test_db -v mysql_data:/var/lib/mysql mysql:8.0
```

### RabbitMQ

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=123456 rabbitmq:3-management
```

管理界面：

```text
http://127.0.0.1:15672
```

## 本节重点

- `docker run` 用来创建并启动容器。
- `docker ps` 查看容器，`ps = process status`。
- `docker logs` 看日志。
- `docker exec` 进入容器并执行命令。
- `docker stop/start/rm` 管理容器生命周期，`rm = remove`。
- `docker rmi` 删除镜像，`rmi = remove image`。
