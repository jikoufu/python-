# 11 pytest Hook 与插件开发

## 是什么

Hook 是 pytest 提供的扩展点。通过 Hook，可以在测试收集、配置、执行、报告生成等阶段插入自己的逻辑。

插件就是把一组 Hook 和工具能力封装起来，给项目或团队复用。

## 为什么要用它

当普通 fixture 和配置不够用时，就需要 Hook：

- 增加自定义命令行参数。
- 根据环境动态选择用例。
- 失败时自动收集日志、截图、接口响应。
- 修改测试报告内容。
- 开发团队内部 pytest 插件。

## 怎么用

在 `conftest.py` 中增加命令行参数：

```python
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test")
```

在 fixture 中读取参数：

```python
import pytest


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")
```

运行：

```bash
pytest --env=dev
pytest --env=test
```

收集用例后动态处理：

```python
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "api" in item.nodeid:
            item.add_marker("api")
```

## 场景例子

场景：根据 `--env` 参数选择不同接口地址。

```python
import pytest


def pytest_addoption(parser):
    parser.addoption("--env", default="test")


@pytest.fixture(scope="session")
def base_url(request):
    env = request.config.getoption("--env")
    urls = {
        "dev": "http://dev.example.com",
        "test": "http://test.example.com",
    }
    return urls[env]
```

## 大厂使用的例子

大型团队经常会封装内部 pytest 插件：

- 统一环境参数。
- 统一登录鉴权。
- 自动采集失败上下文。
- 自动上报测试结果到质量平台。
- 根据服务名、模块名、负责人筛选用例。

例如一个测试平台可以通过 pytest Hook 收集每条用例的执行时间、失败原因、所属模块，然后统一展示在质量看板中。

## 推荐链接

- [pytest Hook 官方文档](https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html)
- [pytest 插件开发文档](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
- [pytest reference hooks](https://docs.pytest.org/en/stable/reference/reference.html#hooks)
- [pluggy 文档](https://pluggy.readthedocs.io/)

## 本章小结

Hook 是 pytest 从“测试框架”走向“测试平台能力”的关键。日常项目先掌握 `pytest_addoption`、`pytest_collection_modifyitems`、失败报告相关 Hook，就能解决很多工程化问题。
