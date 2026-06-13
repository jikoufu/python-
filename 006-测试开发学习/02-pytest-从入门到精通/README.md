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
├── 01 环境准备与测试认知
├── 02 基础断言与异常测试
├── 03 fixture 核心能力
├── 04 参数化与数据驱动
├── 05 mark、跳过、预期失败与用例选择
├── 06 接口自动化测试
├── 07 Mock 与测试隔离
├── 08 测试配置、日志与报告
├── 09 并发、重跑与稳定性治理
├── 10 CI/CD 集成
├── 11 pytest Hook 与插件开发
├── 12 自动化测试框架封装
├── 13 专项实战
└── 14 源码理解与面试提升
```

## 推荐学习顺序

1. [学习路径.md](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/学习路径.md>)
2. [01-环境准备与测试认知](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/01-环境准备与测试认知/01-环境准备与测试认知.md>)
3. [02-基础断言与异常测试](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/02-基础断言与异常测试/01-基础断言与异常测试.md>)
4. [03-fixture核心能力](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/03-fixture核心能力/01-fixture核心能力.md>)
5. [04-参数化与数据驱动](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/04-参数化与数据驱动/01-参数化与数据驱动.md>)
6. [05-mark跳过预期失败与用例选择](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/05-mark跳过预期失败与用例选择/01-mark跳过预期失败与用例选择.md>)
7. [06-接口自动化测试](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/06-接口自动化测试/01-接口自动化测试.md>)
8. [07-Mock与测试隔离](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/07-Mock与测试隔离/01-Mock与测试隔离.md>)
9. [08-测试配置日志与报告](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/08-测试配置日志与报告/01-测试配置日志与报告.md>)
10. [09-并发重跑与稳定性治理](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/09-并发重跑与稳定性治理/01-并发重跑与稳定性治理.md>)
11. [10-CI-CD集成](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/10-CI-CD集成/01-CI-CD集成.md>)
12. [11-pytest-Hook与插件开发](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/11-pytest-Hook与插件开发/01-pytest-Hook与插件开发.md>)
13. [12-自动化测试框架封装](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/12-自动化测试框架封装/01-自动化测试框架封装.md>)
14. [13-专项实战](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/13-专项实战/01-专项实战.md>)
15. [14-源码理解与面试提升](</D:/pythonCode/python-/006-测试开发学习/02-pytest-从入门到精通/14-源码理解与面试提升/01-源码理解与面试提升.md>)

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
