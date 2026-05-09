# 01 接口参数与 CRUD

## 本节目标

完成常见的 5 个接口：

```text
GET    /users/{user_id}
GET    /users?page=1&page_size=10
POST   /users
PUT    /users/{user_id}
DELETE /users/{user_id}
```

这几个接口可以帮助你理解：

- 路径参数从哪里来。
- 查询参数从哪里来。
- 请求体从哪里来。
- Header 怎么接收。
- Cookie 怎么接收。
- 状态码怎么返回。

## 当前代码文件

本节代码在：

```text
main.py
```

运行方式：

```bash
cd D:\PycharmProjects\python后端学习\002-FastAPI-学习\02-请求与响应
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8010
```

接口文档：

```text
http://127.0.0.1:8010/docs
```

## 1. 路径参数

接口：

```text
GET /users/{user_id}
```

代码：

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

请求示例：

```text
GET http://127.0.0.1:8010/users/1
```

这里的 `1` 会被 FastAPI 传给 `user_id`。

## 2. 查询参数

接口：

```text
GET /users?page=1&page_size=10
```

代码：

```python
@app.get("/users")
def list_users(page: int = 1, page_size: int = 10):
    ...
```

请求示例：

```text
GET http://127.0.0.1:8010/users?page=1&page_size=2
```

`page` 和 `page_size` 出现在问号 `?` 后面，所以它们是查询参数。

## 3. 请求体

接口：

```text
POST /users
```

请求体：

```json
{
  "name": "赵六",
  "age": 24,
  "email": "zhaoliu@example.com"
}
```

代码：

```python
class UserCreate(BaseModel):
    name: str
    age: int
    email: Optional[str] = None


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    ...
```

这里的 JSON 请求体会被 FastAPI 解析成 `UserCreate` 对象。

## 4. Header 参数

本节的分页接口里接收了 `User-Agent`：

```python
user_agent: Optional[str] = Header(default=None)
```

请求时，浏览器或接口工具一般会自动带上 `User-Agent`。

返回结果里的 `request_info.user_agent` 可以看到它。

## 5. Cookie 参数

本节的分页接口里也接收了 `session_id`：

```python
session_id: Optional[str] = Cookie(default=None)
```

如果请求带了 Cookie：

```text
session_id=abc123
```

接口就可以读取到这个值。

## 6. 状态码

本节代码里用到了几个常见状态码：

```text
200 OK                  请求成功
201 Created             创建成功
204 No Content          删除成功，但不返回内容
404 Not Found           数据不存在
```

示例：

```python
@app.post("/users", status_code=status.HTTP_201_CREATED)
```

表示新增用户成功后返回 `201`。

如果用户不存在：

```python
raise HTTPException(status_code=404, detail="用户不存在")
```

FastAPI 会返回错误响应。

## 建议练习

在 Swagger UI 中按顺序测试：

1. 查询用户列表：`GET /users`
2. 根据 ID 查询用户：`GET /users/1`
3. 新增用户：`POST /users`
4. 修改用户：`PUT /users/1`
5. 删除用户：`DELETE /users/1`
6. 再查询刚删除的用户，观察 `404`。

## 本节总结

这一节要记住：

- 路径参数写在 URL 路径里，例如 `/users/1`。
- 查询参数写在 `?` 后面，例如 `?page=1&page_size=10`。
- 请求体一般用于 `POST`、`PUT` 这类提交数据的接口。
- Header 常用于传递客户端信息、Token 等。
- Cookie 常用于传递浏览器保存的会话信息。
- 状态码用来告诉客户端请求结果。
