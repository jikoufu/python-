# 01 Pydantic 数据校验

## 本节目标

这一节学习 FastAPI 中非常重要的一部分：Pydantic 数据校验。

你需要掌握：

- `BaseModel` 是什么。
- 如何定义请求模型。
- 如何定义响应模型。
- 如何限制字段长度、范围和格式。
- 如何写自定义校验。
- 如何使用嵌套模型。
- 如何避免把密码返回给前端。

## 为什么需要数据校验

后端接口不能相信前端传来的数据。

例如注册用户时，前端可能传来：

```json
{
  "username": "a",
  "password": "123",
  "age": 999,
  "email": "不是邮箱"
}
```

这些数据都有问题：

- 用户名太短。
- 密码太短。
- 年龄不合理。
- 邮箱格式错误。

Pydantic 的作用就是：在业务代码执行之前，先帮你检查数据是否符合规则。

## 当前代码文件

本节代码在：

```text
main.py
```

运行方式：

```bash
cd D:\PycharmProjects\python后端学习\002-FastAPI-学习\03-Pydantic数据校验
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8010
```

接口文档：

```text
http://127.0.0.1:8010/docs
```

## 1. BaseModel

Pydantic 模型需要继承 `BaseModel`：

```python
class UserCreate(BaseModel):
    username: str
    password: str
    age: int
    email: EmailStr
```

这个模型表示创建用户时，前端必须传：

- `username`：字符串
- `password`：字符串
- `age`：整数
- `email`：邮箱格式字符串

如果前端传错类型，FastAPI 会自动返回 `422` 错误。

## 2. Field 字段规则

可以使用 `Field` 给字段增加校验规则：

```python
username: str = Field(..., min_length=3, max_length=20)
age: int = Field(..., ge=1, le=120)
```

含义：

- `...` 表示必填。
- `min_length` 表示最小长度。
- `max_length` 表示最大长度。
- `ge` 表示大于等于。
- `le` 表示小于等于。

## 3. 邮箱校验

邮箱可以使用 `EmailStr`：

```python
email: EmailStr
```

如果传入的内容不是合法邮箱，Pydantic 会自动报错。

注意：`EmailStr` 需要安装 `email-validator`。

```bash
pip install email-validator
```

## 4. 自定义校验

有些规则不是简单的长度和范围能表达的，这时可以使用 `field_validator`。

例如：用户名不能包含空格。

```python
@field_validator("username")
@classmethod
def username_must_not_contain_space(cls, value: str):
    if " " in value:
        raise ValueError("用户名不能包含空格")
    return value
```

例如：密码至少包含一个数字。

```python
@field_validator("password")
@classmethod
def password_must_contain_number(cls, value: str):
    if not any(char.isdigit() for char in value):
        raise ValueError("密码至少需要包含一个数字")
    return value
```

## 5. 嵌套模型

用户地址可以单独定义一个模型：

```python
class Address(BaseModel):
    province: str
    city: str
    detail: str
```

然后放到用户模型中：

```python
address: Optional[Address] = None
```

这样就可以校验嵌套 JSON。

请求示例：

```json
{
  "username": "zhaoliu",
  "password": "abc123",
  "age": 24,
  "email": "zhaoliu@example.com",
  "address": {
    "province": "广东省",
    "city": "深圳市",
    "detail": "南山区科技园 1 号"
  }
}
```

## 6. 请求模型和响应模型分离

创建用户时，请求体需要密码：

```python
class UserCreate(BaseModel):
    username: str
    password: str
    age: int
    email: EmailStr
```

但是返回给前端时，不应该返回密码。

所以要定义响应模型：

```python
class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    email: EmailStr
```

接口中使用：

```python
@app.post("/users", response_model=UserResponse)
```

这样即使内部数据里有 `password`，最终响应也只会返回 `UserResponse` 里定义的字段。

## 7. 更新模型

更新用户时，通常字段不是全部必填。

所以可以定义：

```python
class UserUpdate(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
```

配合：

```python
user_update.model_dump(exclude_unset=True)
```

只更新前端真正传入的字段。

## 建议练习

打开 Swagger UI 后测试：

1. 使用合法数据创建用户。
2. 把 `username` 改成 1 个字符，观察报错。
3. 把 `age` 改成 999，观察报错。
4. 把 `email` 改成普通字符串，观察报错。
5. 把 `password` 改成没有数字的字符串，观察报错。
6. 创建成功后，观察响应中是否没有 `password`。
7. 使用 PUT 接口只修改用户年龄。

## 本节总结

这一节要记住：

- `BaseModel` 用来定义数据结构。
- `Field` 用来定义字段规则。
- `EmailStr` 用来校验邮箱。
- `field_validator` 用来自定义校验逻辑。
- 嵌套模型可以校验复杂 JSON。
- 请求模型和响应模型应该分开。
- 敏感字段不要返回给前端。
