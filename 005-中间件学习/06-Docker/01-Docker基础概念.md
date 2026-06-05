# 01 Docker 基础概念

## 学习目标

学完这一节，你需要掌握：

- Docker 是什么。
- Docker 解决什么问题。
- 镜像、容器、仓库是什么。
- Docker 和虚拟机的区别。
- 为什么中间件学习要先学 Docker。

## Docker 是什么

Docker 是一个容器化工具。

**Docker 是一种轻量级的虚拟化技术，它让应用程序及其依赖环境可以被打包成一个标准化的单元，在任何地方都能一致地运行。** 如果用一个生活中的类比：**Docker 之于软件，就像集装箱之于货物**。

简单理解：

```text
Docker = 应用 + 运行环境 + 启动方式的打包和运行工具
```

比如你想运行 MySQL，不需要手动下载 MySQL 安装包、配置环境变量、配置服务。

可以直接：

```bash
docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0
```

## Docker 解决什么问题

### 1. 环境不一致

常见问题：

```text
我电脑能跑，你电脑跑不了。
测试环境能跑，生产环境跑不了。
```

Docker 可以把运行环境固定下来。

### 2. 安装复杂

MySQL、Redis、RabbitMQ、Elasticsearch 等中间件本机安装容易污染环境。

Docker 可以快速启动，用完删除。

### 3. 部署困难

应用上线需要依赖很多东西：

- Python 版本
- 依赖包
- 配置文件
- 系统库
- 中间件

Docker 可以把这些统一管理。

## 核心概念

### 1. 镜像 Image

镜像是只读模板。

可以理解为：

```text
镜像 = 安装包 + 运行环境
```

例如：

```text
mysql:8.0
redis:7
nginx:1.25
python:3.12-slim
```

### 2. 容器 Container

容器是镜像运行起来后的实例。

可以理解为：

```text
容器 = 正在运行的程序
```

同一个镜像可以启动多个容器。

例如：

```text
mysql:8.0 镜像
    ↓
mysql-dev 容器
mysql-test 容器
```

### 3. 仓库 Registry

仓库是存放镜像的地方。

常见：

- Docker Hub
- 阿里云镜像仓库
- 私有镜像仓库

拉取镜像：

```bash
docker pull redis:7
```

### 4. 数据卷 Volume

容器删除后，容器里的数据默认也会丢。

数据卷用于持久化数据。

例如 MySQL 数据应该挂载到 volume：

```bash
docker run -v mysql_data:/var/lib/mysql mysql:8.0
```

### 5. 网络 Network

Docker 网络用于容器之间通信。

例如 FastAPI 容器连接 MySQL 容器，不建议写 `127.0.0.1`，而是写服务名：

```text
mysql://root:123456@db:3306/mydb
```

## Docker 和虚拟机区别

| 对比 | Docker 容器 | 虚拟机 |
|------|-------------|--------|
| 启动速度 | 快 | 慢 |
| 资源占用 | 少 | 多 |
| 隔离级别 | 进程级 | 操作系统级 |
| 镜像大小 | 通常较小 | 通常较大 |
| 适合场景 | 应用部署、中间件 | 完整系统隔离 |

## 为什么中间件学习先学 Docker

因为后续中间件都可以用 Docker 一键启动：

```bash
docker run mysql
docker run redis
docker run nginx
docker run rabbitmq
docker run elasticsearch
```

这样学习重点会放在中间件本身，而不是本机安装配置。

## 本节重点

- 镜像是模板，容器是运行实例。
- Docker 可以解决环境一致性问题。
- 中间件学习建议优先使用 Docker。
- 数据卷用于保存数据。
- Docker 网络用于容器之间通信。
