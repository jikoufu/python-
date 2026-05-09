# 03 lifespan 生命周期

## 本节目标

这一节学习 FastAPI 的 `lifespan`。

你需要掌握：

- `lifespan` 是什么。
- `lifespan` 什么时候执行。
- `lifespan` 和 `Depends`、`Middleware` 的区别。
- 启动时适合初始化什么。
- 关闭时适合释放什么。
- 如何把启动时创建的资源保存到 `app.state`。

## lifespan 是什么

`lifespan` 是 FastAPI 应用的生命周期管理机制。

它关注的不是某一次请求，而是整个应用的启动和关闭。

简单理解：

```text
启动 FastAPI 应用
    ↓
lifespan 启动部分执行一次
    ↓
应用开始接收请求
    ↓
处理很多很多请求
    ↓
关闭 FastAPI 应用
    ↓
lifespan 关闭部分执行一次
```

## lifespan 的重点

`lifespan` 的重点是：

```text
应用启动时初始化资源。
应用关闭时释放资源。
```

它不是每个请求都会执行。

它只在应用启动和关闭时执行。

## 当前示例文件

本节单独创建了一个示例：

```text
lifespan_demo.py
```

运行方式：

```bash
cd D:\PycharmProjects\python后端学习\002-FastAPI-学习\04-依赖注入
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m uvicorn lifespan_demo:app --reload --port 8010
```

访问：

```text
http://127.0.0.1:8010/status
```

## 示例代码

```python
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("应用启动：初始化资源")
    app.state.started_at = datetime.now()
    app.state.fake_db_pool = {
        "name": "fake mysql pool",
        "status": "connected",
    }

    yield

    print("应用关闭：释放资源")
    app.state.fake_db_pool["status"] = "closed"


app = FastAPI(title="阶段 4：lifespan 生命周期", lifespan=lifespan)
```

## 代码解释

### 1. asynccontextmanager

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
```

`lifespan` 通常使用 `asynccontextmanager` 来写。

它把函数分成两段：

```text
yield 前：应用启动时执行
yield 后：应用关闭时执行
```

### 2. yield 前

```python
print("应用启动：初始化资源")
app.state.started_at = datetime.now()
app.state.fake_db_pool = {
    "name": "fake mysql pool",
    "status": "connected",
}
```

这些代码会在应用启动时执行一次。

适合放：

- 数据库连接池初始化
- Redis 连接初始化
- 配置加载
- 缓存预热
- 机器学习模型加载
- 定时任务启动

### 3. yield

```python
yield
```

`yield` 表示应用正式开始运行。

在 `yield` 期间，FastAPI 会接收并处理请求。

### 4. yield 后

```python
print("应用关闭：释放资源")
app.state.fake_db_pool["status"] = "closed"
```

这些代码会在应用关闭时执行一次。

适合放：

- 关闭数据库连接池
- 关闭 Redis 连接
- 停止后台任务
- 写入最后的日志
- 清理临时资源

## app.state 是什么

`app.state` 可以用来保存应用级别的共享资源。

例如：

```python
app.state.fake_db_pool = {"status": "connected"}
```

接口里可以通过 `request.app.state` 读取：

```python
@app.get("/status")
def get_status(request: Request):
    return {
        "started_at": request.app.state.started_at,
        "db_pool": request.app.state.fake_db_pool,
    }
```

以后连接数据库时，可以把连接池、缓存客户端等资源放到 `app.state`。

## lifespan、Middleware、Depends 的区别

### lifespan

执行时机：

```text
应用启动时执行一次。
应用关闭时执行一次。
```

适合：

```text
初始化和释放应用级资源。
```

### Middleware

执行时机：

```text
每次请求进入前执行。
每次响应返回前执行。
```

适合：

```text
请求日志、耗时统计、统一响应头、跨域处理。
```

### Depends

执行时机：

```text
某个接口被调用时，根据接口声明执行。
```

适合：

```text
当前用户、权限判断、分页参数、数据库 Session。
```

## 三者对比

```text
lifespan   管应用启动和关闭
Middleware 管每一次请求的前后
Depends    管某个接口需要的资源或逻辑
```

再简单一点：

```text
lifespan：程序的一生。
Middleware：请求的一路。
Depends：接口的一项需要。
```

## 建议练习

1. 启动 `lifespan_demo.py`。
2. 观察终端是否打印 `应用启动：初始化资源`。
3. 访问 `GET /status`。
4. 查看返回的 `started_at` 和 `fake_db_pool`。
5. 停止服务。
6. 观察终端是否打印 `应用关闭：释放资源`。

## 本节总结

这一节要记住：

- `lifespan` 管理应用启动和关闭。
- `yield` 前是启动逻辑。
- `yield` 后是关闭逻辑。
- `lifespan` 不是每个请求都会执行。
- 应用级共享资源可以放在 `app.state`。
- 数据库连接池、Redis、模型加载都适合放在 `lifespan`。
