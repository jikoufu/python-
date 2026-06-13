# 05 mark、跳过、预期失败与用例选择

## 是什么

mark 是 pytest 给测试用例打标签的机制。通过 mark，可以区分冒烟测试、回归测试、慢速测试、线上环境禁跑测试等。

```python
import pytest


@pytest.mark.smoke
def test_login():
    assert True
```

## 为什么要用它

项目变大后，不可能每次都运行所有测试。mark 可以帮助你：

- 只运行冒烟测试。
- 跳过依赖特殊环境的用例。
- 标记已知缺陷。
- 区分单元测试、接口测试、集成测试。

## 怎么用

按标签运行：

```bash
pytest -m smoke
pytest -m "smoke and not slow"
```

按关键字运行：

```bash
pytest -k login
```

跳过测试：

```python
@pytest.mark.skip(reason="接口暂未开发完成")
def test_new_api():
    assert False
```

条件跳过：

```python
import sys
import pytest


@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_linux_command():
    assert True
```

预期失败：

```python
@pytest.mark.xfail(reason="已知缺陷，等待修复")
def test_known_bug():
    assert 1 == 2
```

在 `pytest.ini` 注册 mark：

```ini
[pytest]
markers =
    smoke: core smoke tests
    regression: full regression tests
    slow: slow tests
```

## 场景例子

场景：上线前只跑核心冒烟用例。

```python
@pytest.mark.smoke
def test_login_success():
    assert True


@pytest.mark.regression
def test_login_wrong_password():
    assert True
```

运行：

```bash
pytest -m smoke
```

## 大厂使用的例子

大型团队通常会把测试分层：

- smoke：几分钟内完成，用于部署前快速检查。
- regression：覆盖完整业务流程，定时或合并前运行。
- slow：性能慢或依赖外部服务的测试。
- online：只能在特定环境执行的检查。

例如电商平台上线前，只先跑登录、下单、支付、库存扣减这些核心冒烟测试；夜间再跑完整回归测试。

## 推荐链接

- [pytest mark 官方文档](https://docs.pytest.org/en/stable/how-to/mark.html)
- [pytest skip/xfail 文档](https://docs.pytest.org/en/stable/how-to/skipping.html)
- [pytest 命令行用法](https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags)

## 本章小结

mark 的核心价值是“选择性运行”。测试规模变大后，会不会分类、筛选、跳过和预期失败，直接决定测试能否进入真实研发流程。
