# 10 CI/CD 集成

## 是什么

CI/CD 集成就是把 pytest 放进自动化流水线，让代码提交、合并、发布时自动运行测试。

常见平台：

- GitHub Actions
- GitLab CI
- Jenkins
- Azure Pipelines

## 为什么要用它

只在本地运行测试是不够的。CI 可以保证：

- 每次提交都自动验证。
- 团队成员使用一致的环境。
- 测试结果可追踪。
- 失败阻断合并或发布。
- 报告可归档。

## 怎么用

GitHub Actions 示例：

```yaml
name: pytest

on:
  pull_request:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest --junitxml=reports/junit.xml
```

推荐在 CI 中输出：

- 控制台结果
- JUnit XML
- HTML 报告
- 覆盖率报告

## 场景例子

场景：接口自动化作为 PR 质量门禁。

流程：

1. 开发提交 PR。
2. CI 安装依赖。
3. 运行 `pytest -m smoke`。
4. 生成测试报告。
5. 测试失败时阻止合并。

发布前再运行：

```bash
pytest -m regression --junitxml=reports/regression.xml
```

## 大厂使用的例子

大型团队通常有多层流水线：

- PR 阶段：运行快速单元测试和冒烟测试。
- 合并后：运行模块级回归测试。
- 发布前：运行核心业务全链路测试。
- 夜间任务：运行全量自动化和稳定性扫描。

例如用户中心修改登录逻辑时，PR 阶段会跑登录冒烟用例，夜间会跑注册、登录、权限、Token 过期、多端登录等完整回归。

## 推荐链接

- [GitHub Actions Python 文档](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [GitHub Actions setup-python](https://github.com/actions/setup-python)
- [Jenkins Pipeline 文档](https://www.jenkins.io/doc/book/pipeline/)
- [pytest JUnit XML 文档](https://docs.pytest.org/en/stable/how-to/output.html#creating-junitxml-format-files)

## 本章小结

自动化测试只有进入 CI/CD，才真正参与研发流程。目标不是“我本地能跑”，而是“团队每次变更都能自动验证”。
