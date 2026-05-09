# 02 第一个 FastAPI 接口

## 本节目标

完成一个最简单的 FastAPI 接口：

```text
GET /
```

访问这个接口时，返回：

```json
{
  "message": "Hello FastAPI"
}
```

## 示例代码

当前目录下已经创建了 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
```

## 代码解释

### 1. 导入 FastAPI

```python
from fastapi import FastAPI
```

这行代码表示从 `fastapi` 里面导入 `FastAPI`。

`FastAPI` 是创建后端应用的核心类。

### 2. 创建 FastAPI 应用

```python
app = FastAPI()
```

这行代码创建了一个 FastAPI 应用。

后面所有接口都会挂载到这个 `app` 上。

### 3. 定义 GET 接口

```python
@app.get("/")
```

这行代码表示定义一个 GET 请求接口。

`"/"` 表示接口路径是根路径。

也就是说，当用户访问：

```text
GET /
```

就会执行下面的函数。

### 4. 编写接口函数

```python
def read_root():
    return {"message": "Hello FastAPI"}
```

这个函数就是接口的处理逻辑。

当用户访问 `/` 时，FastAPI 会调用 `read_root()`，然后把返回值转换成 JSON 响应。

## 如何运行

先进入当前目录：

```bash
cd D:\PycharmProjects\python后端学习\002-FastAPI-学习\01-基础入门
```

推荐使用项目虚拟环境启动服务：

```bash
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

启动成功后，访问：

```text
http://127.0.0.1:8000/
```

如果 `8000` 端口被占用，可以换一个端口：

```bash
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8010
```

然后访问：

```text
http://127.0.0.1:8010/
```

应该看到：

```json
{
  "message": "Hello FastAPI"
}
```

## 查看自动接口文档

FastAPI 会自动生成接口文档。

访问：

```text
http://127.0.0.1:8000/docs
```

你会看到刚才写的 `/` 接口。

## 本节总结

这一节你完成了第一个 FastAPI 接口。

需要记住：

- `app = FastAPI()` 用来创建应用。
- `@app.get("/")` 用来定义 GET 接口。
- `return {"message": "Hello FastAPI"}` 会返回 JSON 数据。
- `python -m uvicorn main:app --reload` 用来启动开发服务。
