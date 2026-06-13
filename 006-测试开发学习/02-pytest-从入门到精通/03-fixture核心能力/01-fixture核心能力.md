# 03 fixture 核心能力

## 是什么

fixture 是 pytest 用来准备测试资源的机制。它可以提供测试数据、登录 token、数据库连接、临时文件，也可以负责测试后的清理工作。

```python
import pytest


@pytest.fixture
def user():
    return {"id": 1, "name": "alice"}


def test_user_name(user):
    assert user["name"] == "alice"
```

## 为什么要用它

如果没有 fixture，测试代码里会到处重复准备数据：

- 每个接口测试都要登录。
- 每个数据库测试都要创建连接。
- 每个文件测试都要创建临时文件。
- 每个业务流程测试都要初始化用户。

fixture 可以把这些公共逻辑集中管理，让用例只关注“验证什么”。

## 怎么用

基础 fixture：

```python
@pytest.fixture
def base_url():
    return "http://127.0.0.1:8000"
```

fixture 依赖 fixture：

```python
@pytest.fixture
def token(base_url):
    return "fake-token"


def test_profile(base_url, token):
    assert token
```

使用 `yield` 做清理：

```python
@pytest.fixture
def temp_user():
    user_id = create_user()
    yield user_id
    delete_user(user_id)
```

常见作用域：

```python
@pytest.fixture(scope="function")
def function_data():
    return {}


@pytest.fixture(scope="session")
def session_token():
    return login_once()
```

## 场景例子

场景：接口自动化中统一管理登录 token。

```python
import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def auth_headers(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={"username": "admin", "password": "123456"},
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_profile(base_url, auth_headers):
    response = requests.get(f"{base_url}/profile", headers=auth_headers)
    assert response.status_code == 200
```

## 大厂使用的例子

大型团队会把 fixture 当作测试资源层：

- session 级 fixture 初始化测试环境。
- module 级 fixture 准备模块测试数据。
- function 级 fixture 保证每个用例数据隔离。
- `conftest.py` 统一管理公共 fixture。

例如交易系统里，登录、创建测试账号、清理订单、初始化库存都可以由 fixture 管理，避免每个用例重复写准备逻辑。

## 推荐链接

- [pytest fixture 官方文档](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest fixture reference](https://docs.pytest.org/en/stable/reference/fixtures.html)
- [pytest tmp_path 文档](https://docs.pytest.org/en/stable/how-to/tmp_path.html)

## 本章小结

fixture 是 pytest 的灵魂。学会 fixture 后，测试就不再是一堆零散脚本，而是可以组织资源、控制生命周期、保证隔离性的工程体系。
