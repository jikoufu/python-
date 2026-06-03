# 01 模型与 Prompt

## 学习目标

这一节学习 LangChain 中最基础的两件事：

- 调用模型
- 编写 Prompt 模板

大多数 LangChain 应用都从这两步开始。

## 为什么需要 Prompt 模板

如果直接把字符串传给模型，简单场景可以工作。

但真实项目里，Prompt 往往包含变量：

```text
你是一个 {role}。
请用 {style} 的方式回答这个问题：
{question}
```

这时就适合使用 Prompt 模板。

Prompt 模板的好处：

- 结构清晰
- 变量可复用
- 方便版本管理
- 方便测试
- 方便和模型、解析器组合

## 常见消息类型

聊天模型通常使用消息格式：

```text
System Message：系统规则
Human Message：用户输入
AI Message：模型回复
```

例如：

```text
System：你是一个 FastAPI 老师。
Human：请解释 Depends 是什么。
AI：Depends 是 FastAPI 的依赖注入机制。
```

## PromptTemplate

普通字符串模板可以使用 `PromptTemplate`：

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "请用简单的话解释：{topic}"
)

result = prompt.invoke({"topic": "LangChain"})
print(result)
```

## ChatPromptTemplate

聊天模型更常用 `ChatPromptTemplate`：

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个耐心的 AI 编程老师。"),
    ("human", "请解释 {topic}。"),
])

messages = prompt.invoke({"topic": "LangChain"})
print(messages)
```

## 和模型组合

典型结构：

```python
chain = prompt | model
result = chain.invoke({"topic": "LangChain"})
```

这里的 `|` 表示把前一步输出交给下一步。

流程是：

```text
变量
  ↓
Prompt 模板
  ↓
模型
  ↓
模型回复
```

## 配置模型

不同模型 provider 需要不同包。

OpenAI 示例：

```bash
pip install -U langchain-openai
```

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1-mini")
```

Anthropic 示例：

```bash
pip install -U langchain-anthropic
```

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-5")
```

具体模型名称会随服务商更新，实际项目中以当前 provider 文档为准。

## 建议练习

1. 写一个普通 `PromptTemplate`。
2. 写一个 `ChatPromptTemplate`。
3. 给 Prompt 添加 `role`、`topic`、`style` 三个变量。
4. 把 Prompt 和模型组合成 `chain`。
5. 修改 Prompt，观察模型回答变化。

## 本节重点

- Prompt 模板用于管理可复用提示词。
- 聊天模型更常用 `ChatPromptTemplate`。
- System Message 负责规则和角色。
- Human Message 负责用户问题。
- `prompt | model` 是 LangChain 常见组合方式。
