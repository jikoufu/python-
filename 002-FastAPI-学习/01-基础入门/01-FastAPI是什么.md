# 01 FastAPI 是什么

## 学习目标

学完这一节，你需要知道：

- FastAPI 是用来做什么的。
- FastAPI 适合什么类型的项目。
- FastAPI 为什么适合学习 Python 后端。
- FastAPI 和普通 Python 脚本有什么区别。

## FastAPI 是什么

FastAPI 是一个 Python Web 后端框架，主要用来开发 API 接口。

简单理解：

```text
前端页面 / App / 小程序
        ↓
    请求后端接口
        ↓
FastAPI 接收请求、处理业务、返回数据
        ↓
前端拿到数据后展示给用户
```

例如，一个用户登录功能，前端会把账号密码发送给后端：

```text
POST /login
```

FastAPI 接收到请求后，会完成这些事情：

1. 获取账号和密码。
2. 校验参数格式。
3. 查询数据库。
4. 判断密码是否正确。
5. 返回登录结果。

## FastAPI 主要用来做什么

FastAPI 常用于开发：

- 后端 API 服务
- 前后端分离项目
- 管理后台接口
- App 后端接口
- 小程序后端接口
- 微服务
- AI 应用接口
- 数据服务接口

如果你想用 Python 写后端，FastAPI 是非常适合入门和实战的框架。

## FastAPI 的特点

### 1. 写法简洁

一个最简单的 FastAPI 接口长这样：

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
```

这段代码的意思是：

- 创建一个 FastAPI 应用。
- 定义一个 GET 接口 `/`。
- 访问这个接口时返回 JSON 数据。

### 2. 自动生成接口文档

FastAPI 会自动生成接口文档。

启动项目后，可以访问：

```text
http://127.0.0.1:8000/docs
```

这个页面可以直接查看接口、填写参数、发送请求，非常适合学习和调试。

### 3. 自动校验参数

FastAPI 可以结合 Pydantic 自动校验请求参数。

比如你要求年龄必须是整数，如果前端传了字符串，FastAPI 可以自动提示错误。

### 4. 性能较好

FastAPI 基于 Starlette 和 Pydantic，支持异步能力，性能在 Python Web 框架中表现很好。

### 5. 类型提示友好

FastAPI 很重视 Python 类型提示。

例如：

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

这里的 `user_id: int` 表示 `user_id` 必须是整数。FastAPI 会自动帮你转换和校验。

## FastAPI 和普通 Python 脚本的区别

普通 Python 脚本一般是自己运行一段程序：

```python
print("hello")
```

运行后程序执行完就结束了。

FastAPI 程序是一个长期运行的 Web 服务：

```text
启动服务
等待请求
接收请求
处理请求
返回响应
继续等待下一个请求
```

所以 FastAPI 后端程序通常不会立刻结束，而是一直运行，等待别人访问接口。

## 一个生活化理解

可以把 FastAPI 想象成一个餐厅服务员：

```text
用户 = 客人
请求 = 点菜
FastAPI = 服务员
业务代码 = 后厨
响应 = 上菜
数据库 = 仓库
```

用户发来请求，FastAPI 接住请求，把需要做的事情交给业务代码处理，最后把结果返回给用户。

## 本节重点

你现在只需要记住：

- FastAPI 是 Python 后端 Web 框架。
- 它主要用来写 API 接口。
- 它适合前后端分离项目。
- 它可以自动生成接口文档。
- 它可以自动校验参数。
- 学 FastAPI 的核心就是学习如何接收请求、处理业务、返回响应。

## 自测问题

学完后，试着回答下面几个问题：

1. FastAPI 是用来做什么的？
2. API 接口是什么？
3. 为什么 FastAPI 适合做前后端分离项目？
4. FastAPI 自动生成的接口文档地址是什么？
5. FastAPI 程序为什么通常会一直运行？

## 下一步

下一节建议学习：

```text
02-FastAPI、Flask、Django的区别
```

先理解 FastAPI 和其他 Python Web 框架的区别，再进入安装和第一个接口。
