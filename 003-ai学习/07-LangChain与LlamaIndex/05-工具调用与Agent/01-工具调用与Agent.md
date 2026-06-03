# 01 工具调用与 Agent

## 学习目标

这一节学习 LangChain 中的工具调用和 Agent。

你需要掌握：

- Tool 是什么。
- Agent 是什么。
- 模型为什么需要工具。
- `create_agent` 的基本思路。
- Agent 和普通 Chain 的区别。

## 为什么需要工具

大模型本身擅长理解和生成文本，但它不擅长直接做这些事情：

- 查询实时天气
- 查询数据库
- 调用业务接口
- 做精确计算
- 读取本地文件
- 搜索知识库

工具就是给模型使用的外部能力。

例如：

```python
def get_weather(city: str) -> str:
    return f"{city} 今天晴朗"
```

模型可以根据用户问题决定是否调用这个函数。

## Agent 是什么

Agent 可以理解为：

```text
模型 + 工具 + 决策循环
```

普通 Chain 通常是固定流程：

```text
Prompt → Model → Parser
```

Agent 是动态流程：

```text
用户问题
    ↓
模型思考
    ↓
决定是否调用工具
    ↓
拿到工具结果
    ↓
继续判断或回答
```

## create_agent 基本结构

LangChain v1 中，常见 Agent 创建方式是 `create_agent`。

示例结构：

```python
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    """查询城市天气。"""
    return f"{city} 今天晴朗"


agent = create_agent(
    model="模型名称",
    tools=[get_weather],
    system_prompt="你是一个有帮助的助手。",
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "北京天气怎么样？"}
    ]
})
```

真正运行时需要配置具体模型 provider 和 API Key。

## 工具函数注意点

工具函数建议：

- 函数名清晰
- 参数类型明确
- docstring 写清楚用途
- 返回值尽量简洁
- 不要让工具做太多事情

示例：

```python
def calculate_tax(amount: float, rate: float) -> float:
    """根据金额和税率计算税费。"""
    return amount * rate
```

## Agent 适合做什么

适合：

- 多工具助手
- 数据查询助手
- 自动化办公
- 带 API 调用的客服
- AI 测试用例生成器
- 需要模型自己决定步骤的任务

不适合：

- 流程完全固定的简单任务
- 对延迟要求极低的接口
- 不允许模型自由选择动作的场景

这些场景用普通 Chain 或确定性代码更稳。

## Agent 测试重点

测试 Agent 时，不只看最终回答。

还要看：

- 是否选择了正确工具
- 工具参数是否正确
- 是否重复调用工具
- 工具失败后是否处理
- 是否越权调用工具
- 最终回答是否基于工具结果

## 建议练习

1. 写一个天气工具。
2. 写一个计算器工具。
3. 创建一个 Agent。
4. 问一个必须调用工具的问题。
5. 问一个不需要工具的问题。
6. 观察两种情况下 Agent 的行为。

## 本节重点

- Tool 是模型可以调用的外部能力。
- Agent 会根据问题动态决定是否调用工具。
- 普通 Chain 流程固定，Agent 流程更动态。
- 工具函数要有清晰参数和说明。
- Agent 测试要关注工具调用过程。
