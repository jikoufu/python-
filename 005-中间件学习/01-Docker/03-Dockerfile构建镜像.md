# 03 Dockerfile 构建镜像

## 学习目标

学完这一节，你需要掌握：

- Dockerfile 是什么。
- 常见 Dockerfile 指令。
- 如何为 Python/FastAPI 应用构建镜像。
- Dockerfile 编写注意事项。

## Dockerfile 是什么

Dockerfile 是构建镜像的说明书。

它告诉 Docker：

```text
基于哪个基础镜像
复制哪些文件
安装哪些依赖
暴露哪个端口
容器启动时执行什么命令
```

## 常见指令

### FROM

指定基础镜像。

```dockerfile
FROM python:3.12-slim
```

### WORKDIR

设置工作目录。

```dockerfile
WORKDIR /app
```

### COPY

复制文件到镜像。

```dockerfile
COPY requirements.txt .
COPY . .
```

### RUN

构建镜像时执行命令。

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

### EXPOSE

声明容器监听端口。

```dockerfile
EXPOSE 8000
```

### CMD

容器启动时默认执行命令。

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## FastAPI Dockerfile 示例

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建镜像：

```bash
docker build -t fastapi-demo:v1 .
```

运行容器：

```bash
docker run -d --name fastapi-demo -p 8000:8000 fastapi-demo:v1
```

访问：

```text
http://127.0.0.1:8000
```

## requirements.txt 示例

```text
fastapi
uvicorn
sqlalchemy
pymysql
redis
```

## 构建缓存优化

推荐先复制依赖文件，再复制代码：

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

原因：

```text
代码经常变，依赖不经常变。
这样可以利用 Docker 构建缓存，减少重复安装依赖。
```

## .dockerignore

`.dockerignore` 用来排除不需要复制进镜像的文件。

示例：

```text
.venv
__pycache__
.git
.idea
*.pyc
logs
dist
build
```

如果不写 `.dockerignore`，镜像可能变大，构建也会变慢。

## 常见问题

### 1. 容器里不能访问 127.0.0.1

容器里的 `127.0.0.1` 指容器自己，不是宿主机。

如果 app 容器连接 db 容器，应该使用 compose 服务名：

```text
db:3306
```

### 2. 容器启动后马上退出

看日志：

```bash
docker logs 容器名
```

常见原因：

- 启动命令写错。
- 依赖没安装。
- 代码报错。
- 端口冲突。

### 3. 修改代码后镜像没变化

需要重新 build：

```bash
docker build -t fastapi-demo:v2 .
```

## 本节重点

- Dockerfile 是镜像构建说明书。
- FastAPI 镜像至少需要基础镜像、依赖、代码、启动命令。
- `.dockerignore` 很重要。
- 容器内的 `127.0.0.1` 不是宿主机。
