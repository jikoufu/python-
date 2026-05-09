# 01 Depends 依赖注入

## 本节目标

这一节学习 FastAPI 的依赖注入，也就是 `Depends`。

你需要掌握：

- 什么是依赖注入。
- 为什么要使用 `Depends`。
- 如何封装公共查询参数。
- 如何封装数据库连接。
- 如何封装当前登录用户。
- 如何封装管理员权限。
- 多个依赖如何组合使用。

## 什么是依赖注入

依赖注入可以理解为：接口函数需要什么公共能力，就让 FastAPI 自动帮你准备好。

比如很多接口都需要分页参数：

```python
page: int = 1
page_size: int = 10
```

如果每个接口都写一遍，就会重复。

使用依赖注入后，可以把分页逻辑抽成函数：

```python
def get_page_params(...):
    return PageParams(page=page, page_size=page_size)
```

然后接口里这样使用：

```python
page_params: PageParams = Depends(get_page_params)
```

FastAPI 会先执行 `get_page_params()`，再把返回值传给接口函数。

## 当前代码文件

本节代码在：

```text
main.py
```

运行方式：

```bash
cd D:\PycharmProjects\python后端学习\002-FastAPI-学习\04-依赖注入
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8010
```

接口文档：

```text
http://127.0.0.1:8010/docs
```

## 1. 封装分页参数

代码：

```python
def get_page_params(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=50)] = 10,
):
    return PageParams(page=page, page_size=page_size)
```

使用：

```python
@app.get("/articles")
def list_articles(page_params: PageParams = Depends(get_page_params)):
    ...
```

请求示例：

```text
GET /articles?page=1&page_size=2
```

这样分页规则只需要写一次，多个接口都可以复用。

## 2. 封装数据库依赖

本节先用内存数据模拟数据库：

```python
def get_db():
    return {
        "users": users,
        "articles": articles,
    }
```

接口中使用：

```python
db: dict = Depends(get_db)
```

以后学习真正数据库时，`get_db()` 通常会返回数据库 Session。

## 3. 封装当前登录用户

本节用 Header 模拟登录。

请求时传：

```text
Authorization: Bearer user-token
```

依赖函数：

```python
def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
    db: dict = Depends(get_db),
):
    ...
```

注意这里的 `get_current_user()` 里面又使用了：

```python
db: dict = Depends(get_db)
```

这就是多层依赖。

## 4. 获取当前用户接口

接口：

```text
GET /users/me
```

代码：

```python
@app.get("/users/me", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

如果请求头中没有正确的 `Authorization`，接口会返回 `401`。

## 5. 获取自己的文章

接口：

```text
GET /articles/mine
```

这个接口需要登录。

代码：

```python
@app.get("/articles/mine")
def list_my_articles(
    current_user: User = Depends(get_current_user),
    db: dict = Depends(get_db),
):
    ...
```

它同时依赖：

- 当前用户
- 数据库

## 6. 管理员权限依赖

先封装权限判断：

```python
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user
```

再用于管理员接口：

```python
@app.get("/admin/users")
def list_all_users(admin_user: User = Depends(require_admin)):
    ...
```

如果普通用户访问，会返回 `403`。

## 测试 Token

本节准备了两个 token：

```text
普通用户：
Authorization: Bearer user-token

管理员：
Authorization: Bearer admin-token
```

## 建议练习

打开 Swagger UI 后测试：

1. 访问 `GET /articles?page=1&page_size=2`。
2. 不带 Authorization 访问 `GET /users/me`，观察 `401`。
3. 带 `Bearer user-token` 访问 `GET /users/me`。
4. 带 `Bearer user-token` 访问 `GET /articles/mine`。
5. 带 `Bearer user-token` 访问 `GET /admin/users`，观察 `403`。
6. 带 `Bearer admin-token` 访问 `GET /admin/users`。

## 本节总结

这一节要记住：

- `Depends` 用来声明依赖。
- 依赖函数会在接口函数之前执行。
- 依赖函数的返回值会传给接口参数。
- 公共参数、数据库连接、当前用户、权限判断都适合做成依赖。
- 依赖里面还可以继续使用其他依赖，这叫多层依赖。
