# 01 pytest 接口自动化测试学习过程

## 学习目标

这一模块学习接口自动化测试。

学完后你需要能够：

- 理解 pytest 的基本用法。
- 使用 requests 调用 HTTP 接口。
- 编写接口断言。
- 使用 fixture 管理测试前置条件。
- 使用参数化批量测试接口。
- 测试 FastAPI 接口。
- 生成基础测试报告。
- 为 AI 应用接口设计自动化测试。

## 接口自动化测试是什么

接口自动化测试是用代码自动请求后端接口，并检查接口返回是否符合预期。

例如测试一个登录接口：

```text
POST /login
```

需要检查：

- 状态码是否正确。
- 返回 JSON 是否包含 token。
- 错误密码是否返回 401。
- 缺少参数是否返回 422。
- 响应时间是否合理。

## 阶段 1：准备环境

安装依赖：

```bash
pip install pytest requests
```

如果测试 FastAPI 应用，还可以使用：

```bash
pip install httpx
```

FastAPI 自带的 `TestClient` 会用到相关能力。

## 阶段 2：第一个 pytest 用例

创建测试文件：

```text
test_demo.py
```

示例：

```python
def add(a, b):
    return a + b


def test_add():
    assert add(1, 2) == 3
```

运行：

```bash
pytest -q
```

pytest 会自动发现：

- `test_*.py`
- `*_test.py`
- `test_` 开头的函数

## 阶段 3：使用 requests 测接口

示例：

```python
import requests


def test_get_user():
    response = requests.get("http://127.0.0.1:8000/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
```

常见断言：

```python
assert response.status_code == 200
assert response.json()["code"] == 0
assert "token" in response.json()
assert response.elapsed.total_seconds() < 1
```

## 阶段 4：测试 POST 接口

示例：

```python
import requests


def test_create_user():
    payload = {
        "username": "zhangsan",
        "password": "abc123",
        "email": "zhangsan@example.com",
    }

    response = requests.post(
        "http://127.0.0.1:8000/users",
        json=payload,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "zhangsan"
    assert "password" not in data
```

## 阶段 5：fixture

`fixture` 用来管理测试前置条件和公共资源。

例如统一管理接口地址：

```python
import pytest


@pytest.fixture
def base_url():
    return "http://127.0.0.1:8000"
```

使用：

```python
def test_get_users(base_url):
    response = requests.get(f"{base_url}/users")
    assert response.status_code == 200
```

也可以用于登录：

```python
@pytest.fixture
def token(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={"username": "admin", "password": "123456"},
    )
    return response.json()["token"]
```

## 阶段 6：参数化

参数化适合批量测试多组数据。

```python
import pytest


@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (1, 200),
        (999, 404),
        ("abc", 422),
    ],
)
def test_get_user_by_id(base_url, user_id, expected_status):
    response = requests.get(f"{base_url}/users/{user_id}")
    assert response.status_code == expected_status
```

## 阶段 7：测试 FastAPI 应用

如果测试的是本地 FastAPI 代码，可以不用启动服务，直接用 `TestClient`。

示例：

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello FastAPI"
```

这种方式适合：

- 单元测试
- 接口逻辑测试
- CI 自动化
- 不想手动启动 uvicorn 的场景

## 阶段 8：AI 应用接口测试

AI 应用接口测试除了状态码，还要测试输出质量。

常见测试点：

- 响应状态码是否正确。
- 响应 JSON 格式是否正确。
- 模型回答是否为空。
- 是否包含必要关键词。
- 是否拒绝非法请求。
- 响应耗时是否超过阈值。
- token 成本是否过高。
- 多轮对话是否保留上下文。

示例：

```python
def test_ai_chat_answer_not_empty(base_url):
    response = requests.post(
        f"{base_url}/chat",
        json={"message": "FastAPI 是什么？"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"]
    assert "FastAPI" in data["answer"]
```

## 阶段 9：测试报告

可以安装：

```bash
pip install pytest-html
```

生成 HTML 报告：

```bash
pytest --html=report.html --self-contained-html
```

也可以自己输出 Markdown 报告，用于 AI 测试结果记录。

## 推荐项目结构

```text
api_tests/
├── conftest.py
├── test_users.py
├── test_auth.py
├── test_ai_chat.py
├── data/
│   └── chat_cases.json
└── reports/
```

文件说明：

- `conftest.py` 放公共 fixture。
- `test_users.py` 测用户接口。
- `test_auth.py` 测登录鉴权。
- `test_ai_chat.py` 测 AI 聊天接口。
- `data/` 放测试数据。
- `reports/` 放测试报告。

## 建议练习

1. 编写一个最简单的 pytest 用例。
2. 用 requests 测试一个 GET 接口。
3. 用 requests 测试一个 POST 接口。
4. 使用 fixture 管理 `base_url`。
5. 使用参数化测试多个用户 ID。
6. 使用 FastAPI `TestClient` 测试本地接口。
7. 为 AI 聊天接口写一个回答非空断言。
8. 生成一份 HTML 或 Markdown 测试报告。

## 本节重点

- pytest 是 Python 测试框架。
- requests 可以调用真实 HTTP 接口。
- FastAPI `TestClient` 可以直接测试应用代码。
- fixture 用来管理公共前置条件。
- 参数化用来批量跑多组数据。
- AI 接口测试要同时关注接口格式和回答质量。
