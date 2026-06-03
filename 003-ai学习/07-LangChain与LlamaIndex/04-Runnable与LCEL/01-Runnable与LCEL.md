# 01 Runnable 与 LCEL

## 学习目标

这一节学习 LangChain 的组合方式：

- Runnable
- LCEL
- 管道符 `|`
- `invoke`
- `batch`
- `stream`

## Runnable 是什么

Runnable 可以理解为 LangChain 中“可运行的组件”。

很多对象都可以是 Runnable：

- Prompt
- Model
- OutputParser
- Retriever
- Chain

只要它能接收输入、产生输出，就可以参与组合。

## LCEL 是什么

LCEL 是 LangChain Expression Language。

它让你用管道方式组合大模型应用流程。

最常见写法：

```python
chain = prompt | model | parser
```

含义：

```text
输入变量
    ↓
Prompt
    ↓
Model
    ↓
Parser
    ↓
最终结果
```

## invoke

`invoke` 用来执行一次调用：

```python
result = chain.invoke({"question": "LangChain 是什么？"})
```

适合单条输入。

## batch

`batch` 用来批量执行：

```python
results = chain.batch([
    {"question": "LangChain 是什么？"},
    {"question": "RAG 是什么？"},
    {"question": "Agent 是什么？"},
])
```

适合测试集批量评估。

## stream

`stream` 用来流式输出：

```python
for chunk in chain.stream({"question": "解释 RAG"}):
    print(chunk, end="")
```

适合聊天应用逐字显示。

## 为什么 LCEL 很重要

LCEL 可以让复杂流程保持清晰：

```text
Prompt 负责组织输入
Model 负责生成
Parser 负责整理输出
Retriever 负责查资料
Tool 负责执行动作
```

每一层职责分开，后面更容易测试、替换和调试。

## 建议练习

1. 写一个 `prompt | model`。
2. 加上输出解析器，变成 `prompt | model | parser`。
3. 用 `invoke` 跑一条问题。
4. 用 `batch` 跑三条问题。
5. 用 `stream` 做流式输出。

## 本节重点

- Runnable 是 LangChain 的可组合单元。
- LCEL 用管道方式组合流程。
- `invoke` 执行单次调用。
- `batch` 执行批量调用。
- `stream` 执行流式调用。
- `prompt | model | parser` 是最核心的入门结构。
