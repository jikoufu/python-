# 02 中间件 Middleware

## 本节目标

这一节学习 FastAPI 的中间件。

你需要掌握：

- 中间件是什么。
- 中间件和依赖注入的区别。
- 如何在请求前后执行公共逻辑。
- 如何记录请求日志。
- 如何给响应添加自定义 Header。
- 多个中间件的执行顺序。
- 中间件适合处理哪些事情。

## 什么是中间件

中间件是在请求进入接口之前、响应返回客户端之前执行的一层公共逻辑。

请求流程可以理解为：

```text
客户端请求
    ↓
中间件：请求进入前
    ↓
接口函数
    ↓
中间件：响应返回前
    ↓
客户端收到响应
```

比如你想给所有接口统计耗时，如果每个接口都写一次，就很麻烦。

这时就适合使用中间件。

## 当前代码

本节在 `main.py` 中添加了两个中间件。

第一个中间件写在代码上方，用来统计耗时：

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("1. 进入耗时统计中间件")
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    response.headers["X-Learning-Stage"] = "depends-and-middleware"
    print("4. 离开耗时统计中间件")
    return response
```

第二个中间件写在代码下方，用来演示执行顺序：

```python
@app.middleware("http")
async def show_middleware_order(request: Request, call_next):
    print("0. 进入顺序演示中间件")
    response = await call_next(request)
    response.headers["X-Middleware-Order"] = (
        "show_middleware_order -> add_process_time_header -> endpoint"
    )
    print("5. 离开顺序演示中间件")
    return response
```

## 多个中间件的执行顺序

多个中间件非常重要的一点是：

```text
请求进入时：按照代码从下到上执行。
响应返回时：按照代码从上到下返回。
```

比如代码顺序是：

```python
@app.middleware("http")
async def add_process_time_header(...):
    ...


@app.middleware("http")
async def show_middleware_order(...):
    ...
```

虽然 `add_process_time_header` 写在上面，`show_middleware_order` 写在下面，但是请求进入时会先执行下面这个：

```text
show_middleware_order
```

然后再执行上面这个：

```text
add_process_time_header
```

完整流程是：

```text
请求进入
    ↓
show_middleware_order 请求前
    ↓
add_process_time_header 请求前
    ↓
接口函数
    ↓
add_process_time_header 响应后
    ↓
show_middleware_order 响应后
    ↓
响应返回客户端
```

终端日志大概会看到：

```text
0. 进入顺序演示中间件
1. 进入耗时统计中间件
4. 离开耗时统计中间件
5. 离开顺序演示中间件
```

简单记：

```text
进来：从下到上。
出去：从上到下。
```

## 单个中间件代码解释

以前面的耗时中间件为例：

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    print(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} time={process_time:.6f}s"
    )
    return response
```

### 1. 注册中间件

```python
@app.middleware("http")
```

这表示注册一个 HTTP 中间件。

所有 HTTP 请求都会经过它。

### 2. 接收 Request 和 call_next

```python
async def add_process_time_header(request: Request, call_next):
```

参数说明：

- `request`：当前请求对象。
- `call_next`：调用下一个处理流程，也就是继续执行后面的接口。

### 3. 请求进入前

```python
start_time = time.perf_counter()
```

这里在接口执行前记录开始时间。

### 4. 执行接口

```python
response = await call_next(request)
```

这行代码会继续执行真正的接口函数。

如果没有这行，请求就不会进入接口。

### 5. 响应返回前

```python
process_time = time.perf_counter() - start_time
response.headers["X-Process-Time"] = f"{process_time:.6f}"
```

接口执行完成后，计算耗时，并把耗时放到响应头里。

## 如何运行

```bash
cd D:\PycharmProjects\python后端学习\002-FastAPI-学习\04-依赖注入
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8010
```

访问：

```text
http://127.0.0.1:8010/articles
```

响应 Header 中会多出：

```text
X-Process-Time
X-Learning-Stage
X-Middleware-Order
```

## 中间件适合做什么

中间件适合做所有接口都需要的公共处理：

- 请求日志
- 接口耗时统计
- 跨域 CORS
- 全局异常包装
- 请求 ID
- 统一响应 Header
- IP 黑名单
- 简单限流

## 中间件和 Depends 的区别

`Depends` 更适合某些接口需要的逻辑。

例如：

```text
获取当前用户
检查管理员权限
数据库 Session
分页参数
```

中间件更适合所有请求都会经过的逻辑。

例如：

```text
记录请求日志
统计接口耗时
添加通用响应头
处理跨域
```

简单记：

```text
Depends：接口需要什么，就注入什么。
Middleware：所有请求经过时，统一处理什么。
```

## 建议练习

1. 启动服务。
2. 访问 `GET /articles`。
3. 查看响应 Header 里的 `X-Process-Time`。
4. 查看响应 Header 里的 `X-Middleware-Order`。
5. 查看终端里打印的中间件执行顺序。
6. 访问 `GET /users/me`，观察即使返回 `401`，中间件也会执行。
7. 尝试把 `X-Learning-Stage` 改成自己的学习标记。

## 本节总结

这一节要记住：

- 中间件会包住接口执行流程。
- 多个中间件请求进入时按代码从下到上执行。
- 多个中间件响应返回时按代码从上到下返回。
- `call_next(request)` 表示继续执行真正的接口。
- 中间件可以在请求前和响应后做公共处理。
- 统计耗时、请求日志、统一 Header 很适合放在中间件。
- 中间件作用范围通常比 `Depends` 更大。
