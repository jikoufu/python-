# pytest 从入门到精通

这个目录用于系统学习 pytest。目标不是只会写几个 `assert`，而是把 pytest 学成一套可落地的测试工程能力：能写单元测试、接口自动化、数据驱动测试、Mock 测试、插件扩展、报告生成、CI 集成，并最终沉淀自己的测试框架。

## 适合人群

- Python 基础已经入门，想进入自动化测试。
- 正在学习测试开发，想把 pytest 作为核心测试框架。
- 做后端、FastAPI、AI 应用开发，想补齐自动化回归能力。
- 准备测试开发、自动化测试、AI 测试岗位面试。

## 学习主线

```text
pytest 学习主线
├── 01 基础入门：安装、测试发现、断言、运行参数
├── 02 核心语法：fixture、参数化、mark、异常测试
├── 03 工程实践：目录结构、conftest.py、配置文件、测试数据
├── 04 接口自动化：requests/httpx、鉴权、依赖接口、响应断言
├── 05 Mock 与隔离：monkeypatch、unittest.mock、外部服务隔离
├── 06 插件与报告：pytest-html、allure、coverage、xdist
├── 07 CI/CD 集成：GitHub Actions、Jenkins、失败重跑、报告归档
├── 08 框架封装：配置、日志、客户端、断言、数据驱动、分层设计
├── 09 高级能力：Hook、插件开发、性能优化、 flaky 用例治理
└── 10 实战项目：接口自动化框架、FastAPI 测试、AI 接口评测框架
```

## 推荐学习顺序

1. [学习路径.md](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/学习路径.md>)
2. 搭建本地 pytest 练习项目。
3. 完成基础语法练习。
4. 完成 fixture 和参数化专项练习。
5. 完成接口自动化小项目。
6. 接入测试报告和覆盖率。
7. 接入 CI 自动运行。
8. 封装一个自己的 pytest 测试框架。

## 最终目标

学完后你应该能做到：

- 熟练编写 pytest 测试用例。
- 使用 fixture 管理测试前置、后置和公共资源。
- 使用参数化实现数据驱动测试。
- 编写接口自动化测试并处理鉴权、依赖、断言和测试数据。
- 使用 Mock 隔离数据库、第三方接口、文件、时间和环境变量。
- 生成 HTML、Allure、覆盖率等测试报告。
- 把 pytest 接入 CI/CD。
- 设计一个清晰、可维护、可扩展的自动化测试框架。
- 能在面试中讲清楚 pytest 的核心机制和工程落地经验。

## 建议项目结构

```text
pytest_project/
├── pytest.ini
├── requirements.txt
├── README.md
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── test_calculator.py
│   ├── api/
│   │   ├── test_auth.py
│   │   └── test_users.py
│   └── integration/
│       └── test_order_flow.py
├── common/
│   ├── config.py
│   ├── logger.py
│   ├── http_client.py
│   └── assertions.py
├── data/
│   ├── users.yaml
│   └── login_cases.json
└── reports/
```

## 学习原则

- 先会写，再会组织，再会封装。
- 每学一个 pytest 特性，都要找一个真实测试场景练习。
- 不要一开始就堆复杂框架，先把用例、数据、断言、报告跑通。
- 用例可读性优先，封装是为了减少重复和降低维护成本。
- 所有自动化测试最终都要能在 CI 里稳定运行。
