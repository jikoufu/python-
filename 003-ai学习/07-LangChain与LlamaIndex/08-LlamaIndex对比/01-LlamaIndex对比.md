# 01 LlamaIndex 对比

## 学习目标

这一节先不深入写 LlamaIndex 代码，而是理解它和 LangChain 的区别。

你需要知道：

- LlamaIndex 是什么。
- LlamaIndex 更适合什么场景。
- LangChain 更适合什么场景。
- 项目中如何选型。

## LlamaIndex 是什么

LlamaIndex 是一个偏数据连接和索引构建的大模型应用框架。

它特别适合处理：

- 文档加载
- 文档解析
- 文档切分
- 索引构建
- 查询引擎
- 知识库问答

如果你的项目核心是“把大量资料变成可查询的知识库”，LlamaIndex 很值得学习。

## LangChain 更擅长什么

LangChain 更偏应用编排：

- Prompt
- 模型调用
- 输出解析
- Runnable
- 工具调用
- Agent
- 多步骤流程
- RAG 应用组合

如果你的项目核心是“让模型调用工具并完成任务”，LangChain 更自然。

## LlamaIndex 更擅长什么

LlamaIndex 更偏数据索引：

- 文档摄取
- 数据连接
- Node 管理
- Index 构建
- 查询引擎
- 文档问答

如果你的项目核心是“围绕文档和知识库问答”，LlamaIndex 的抽象会更直接。

## 简单选型

```text
做 Agent、多工具助手、复杂流程：优先 LangChain。
做文档索引、知识库查询：优先 LlamaIndex。
做复杂 RAG 产品：两者都可以考虑。
```

## 对比表

| 维度 | LangChain | LlamaIndex |
|------|-----------|------------|
| 核心方向 | 应用编排 | 数据索引 |
| 典型能力 | Agent、Tool、Runnable | Document、Node、Index |
| 适合场景 | 多步骤 AI 应用 | 文档问答 |
| RAG 能力 | 强，偏组合流程 | 强，偏数据组织 |
| 学习重点 | Prompt、Tool、Agent | Loader、Index、Query Engine |

## 建议学习顺序

如果你是后端学习路线，建议：

1. 先学 LangChain 基础。
2. 用 LangChain 做一个最小 Agent。
3. 用 LangChain 做一个最小 RAG。
4. 再学 LlamaIndex 的文档索引。
5. 对比哪个更适合你的项目。

## 本节重点

- LangChain 更像 AI 应用编排框架。
- LlamaIndex 更像数据索引和知识库框架。
- 两者不是敌人，可以组合使用。
- 学习时先按项目需求选主线，不要同时把两个框架所有 API 都背下来。
