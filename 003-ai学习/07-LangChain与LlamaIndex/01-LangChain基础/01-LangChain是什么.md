# 01 LangChain 是什么

## 学习目标

学完这一节，你需要知道：

- LangChain 是什么。
- LangChain 主要解决什么问题。
- LangChain、LangGraph、LangSmith 的关系。
- LangChain 和 LlamaIndex 的区别。
- 学 LangChain 应该先抓哪些重点。

## LangChain 是什么

LangChain 是一个用于构建大语言模型应用的开发框架。

它的作用不是训练大模型，而是帮助你把大模型接入真实应用。

例如：

```text
用户问题
    ↓
Prompt 模板
    ↓
大模型
    ↓
输出解析
    ↓
工具调用 / 检索 / 数据库 / API
    ↓
返回最终结果
```

LangChain 让这些步骤更容易组合、复用和工程化。

## LangChain 适合做什么

LangChain 适合开发：

- AI 聊天助手
- 文档问答系统
- RAG 知识库应用
- 工具调用 Agent
- 自动化办公助手
- AI 测试用例生成器
- 数据查询助手
- 多步骤推理应用

## LangChain 不是什么

LangChain 不是大模型本身。

它不会替你训练 GPT、Claude、Llama。

它更像一个应用开发框架，负责把这些能力组织起来：

- 模型调用
- Prompt 管理
- 输出解析
- 工具调用
- 检索
- 记忆
- Agent
- 可观测性

## LangChain v1 的学习重点

LangChain v1 更强调：

- 标准模型接口
- Agent 架构
- `create_agent`
- Runnable 组合
- 检索和工具
- LangGraph 底座
- LangSmith 调试和观测

学习时不要只盯着旧版的 `LLMChain`。

更推荐先理解：

```text
Prompt
Model
Parser
Runnable
Tool
Agent
Retriever
```

## LangChain、LangGraph、LangSmith 的关系

### LangChain

用于快速开发大模型应用。

你会经常用它写：

- Prompt
- 模型调用
- 工具
- Agent
- RAG

### LangGraph

LangGraph 是更底层的 Agent 编排框架。

适合复杂工作流：

- 多步骤状态机
- 可恢复执行
- Human-in-the-loop
- 多 Agent 协作
- 更精细的流程控制

可以理解为：

```text
LangChain：更容易上手，适合快速构建应用。
LangGraph：更底层、更可控，适合复杂 Agent 工作流。
```

### LangSmith

LangSmith 用来调试、追踪和评估大模型应用。

它关注：

- 每次模型调用的输入输出
- Agent 执行轨迹
- Token 消耗
- 失败样本
- 评估结果

可以理解为大模型应用的观测和调试平台。

## LangChain 和 LlamaIndex 的区别

LangChain 更偏应用编排：

- 调模型
- 写 Prompt
- 组合链路
- 调工具
- 做 Agent

LlamaIndex 更偏数据和索引：

- 加载文档
- 文档切分
- 构建索引
- 查询知识库
- 数据连接

简单记：

```text
LangChain：把大模型应用流程串起来。
LlamaIndex：把外部数据组织成可查询的知识结构。
```

如果你做一个 RAG 项目：

- 文档索引能力强，可以考虑 LlamaIndex。
- Agent 和工具调用多，可以考虑 LangChain。
- 复杂项目里也可以两个一起用。

## 最小安装

官方推荐先安装 LangChain：

```bash
pip install -U langchain
```

如果要调用具体模型，还需要安装对应 provider 包。

例如 OpenAI：

```bash
pip install -U langchain-openai
```

例如 Anthropic：

```bash
pip install -U langchain-anthropic
```

## 最小 Agent 思路

LangChain v1 中，Agent 通常可以通过 `create_agent` 创建。

思路是：

```text
定义工具函数
    ↓
创建 Agent
    ↓
传入模型、工具和系统提示
    ↓
调用 Agent
```

伪代码结构：

```python
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    return f"{city} 今天天气晴朗"


agent = create_agent(
    model="模型名称",
    tools=[get_weather],
    system_prompt="你是一个有帮助的助手",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "北京天气怎么样？"}]}
)
```

这里先看懂结构即可，真正运行需要配置具体模型和 API Key。

## 学习 LangChain 的正确顺序

建议按这个顺序：

1. 模型调用
2. Prompt 模板
3. 输出解析
4. Runnable 和 LCEL
5. 工具调用
6. Agent
7. 检索和 RAG
8. 记忆和上下文
9. LangSmith 调试
10. 项目实战

## 本节重点

你现在只需要记住：

- LangChain 是大模型应用开发框架。
- 它不是模型本身，而是用来组织模型、Prompt、工具、检索和 Agent。
- LangChain v1 重点关注 Agent、Runnable、工具和 LangGraph 底座。
- LangGraph 更适合复杂 Agent 编排。
- LangSmith 用来调试和观测。
- LlamaIndex 更偏文档索引和知识库查询。

## 自测问题

1. LangChain 是用来训练模型的吗？
2. LangChain 主要解决什么问题？
3. LangChain 和 LangGraph 有什么区别？
4. LangSmith 是干什么的？
5. LangChain 和 LlamaIndex 分别更擅长什么？
