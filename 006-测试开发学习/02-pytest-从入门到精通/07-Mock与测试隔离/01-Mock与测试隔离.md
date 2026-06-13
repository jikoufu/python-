# 07 Mock 与测试隔离

## 是什么

Mock 是用假的对象、函数或返回值替代真实依赖。pytest 常用 `monkeypatch` 和 Python 标准库 `unittest.mock` 做 Mock。

```python
def get_env():
    import os
    return os.getenv("APP_ENV", "dev")


def test_get_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    assert get_env() == "test"
```

## 为什么要用它

单元测试应该稳定、快速、可重复。但真实依赖经常不稳定：

- 第三方接口超时。
- 数据库数据变化。
- 当前时间变化。
- 环境变量不同。
- 文件系统状态不同。

Mock 可以隔离这些不稳定因素。

## 怎么用

Mock 环境变量：

```python
def test_env(monkeypatch):
    monkeypatch.setenv("TOKEN", "fake-token")
    assert True
```

Mock 函数返回值：

```python
from unittest.mock import Mock


def test_mock_func():
    get_user = Mock(return_value={"id": 1, "name": "alice"})
    assert get_user()["name"] == "alice"
```

Mock 对象方法：

```python
from unittest.mock import patch


def test_patch_request():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"ok": True}
        assert mock_get.return_value.json()["ok"] is True
```

## 场景例子

场景：支付接口依赖第三方支付网关，不希望单元测试真的扣款。

```python
def create_order(pay_client, amount):
    result = pay_client.pay(amount)
    return result["status"] == "success"


def test_create_order_pay_success():
    pay_client = Mock()
    pay_client.pay.return_value = {"status": "success"}

    assert create_order(pay_client, 100) is True
    pay_client.pay.assert_called_once_with(100)
```

## 大厂使用的例子

大型团队通常会把测试分成：

- 单元测试：大量 Mock，追求快和稳定。
- 集成测试：少量 Mock，验证模块协作。
- 端到端测试：尽量真实，验证完整链路。

例如支付、物流、短信、邮件、风控等第三方服务，单元测试中通常不会真实调用，而是用 Mock 固定返回值，保证测试可重复。

## 推荐链接

- [pytest monkeypatch 文档](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [unittest.mock 官方文档](https://docs.python.org/3/library/unittest.mock.html)
- [pytest fixture 文档](https://docs.pytest.org/en/stable/how-to/fixtures.html)

## 本章小结

Mock 的目的不是“假装测试通过”，而是隔离不稳定依赖，让测试聚焦当前模块的行为。能正确判断哪些地方该 Mock，是测试工程能力的重要分水岭。
