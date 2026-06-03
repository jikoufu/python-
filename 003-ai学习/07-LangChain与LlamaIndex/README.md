# 07 LangChain 与 LlamaIndex

这个目录用于系统学习 LangChain 和 LlamaIndex。重点先放在 LangChain：模型调用、Prompt、输出解析、Runnable、工具调用、Agent、记忆、检索和 RAG，再对比 LlamaIndex 的文档索引能力。

LangChain 适合快速构建大模型应用和 Agent；LlamaIndex 更偏向文档、数据连接、索引和知识库问答。实际项目里二者可以单独使用，也可以组合使用。

## 目录结构

```text
07-LangChain与LlamaIndex/
├── README.md
├── 学习路径.md
├── 01-LangChain基础/
├── 02-模型与Prompt/
├── 03-输出解析器/
├── 04-Runnable与LCEL/
├── 05-工具调用与Agent/
├── 06-记忆与上下文/
├── 07-检索与RAG/
├── 08-LlamaIndex对比/
└── 09-实战项目/
```

## 学习模块

### 01-LangChain基础

- LangChain 是什么
- LangChain v1 的核心变化
- LangChain、LangGraph、LangSmith 的关系
- LangChain 和 LlamaIndex 的区别
- 安装和环境准备

### 02-模型与 Prompt

- ChatModel
- PromptTemplate
- ChatPromptTemplate
- System / Human / AI Message
- 模型输入输出格式

### 03-输出解析器

- 为什么需要输出解析
- 字符串解析
- JSON 解析
- Pydantic 结构化输出
- 输出格式校验

### 04-Runnable 与 LCEL

- Runnable 是什么
- LCEL 管道写法
- `prompt | model | parser`
- invoke、batch、stream
- 组合、并行和分支

### 05-工具调用与 Agent

- Tool 是什么
- 函数工具
- `create_agent`
- Agent 执行流程
- 工具调用调试

### 06-记忆与上下文

- 短期记忆
- 长期记忆
- 对话历史
- 上下文压缩
- 记忆和数据库存储

### 07-检索与 RAG

- Document
- 文档加载
- 文档切分
- Embedding
- Vector Store
- Retriever
- RAG Chain
- Agentic RAG

### 08-LlamaIndex 对比

- LlamaIndex 是什么
- Document、Node、Index
- 查询引擎
- 和 LangChain 的选型区别

### 09-实战项目

- 做一个命令行 AI 助手
- 做一个文档问答 RAG
- 做一个带工具调用的 Agent
- 做一个带测试集的 AI 应用

## 学习建议

1. 先学模型调用和 Prompt，不急着上 Agent。
2. 再学输出解析，让模型输出能被程序稳定使用。
3. 然后学 Runnable 和 LCEL，理解 LangChain 的组合方式。
4. 接着学工具调用和 Agent。
5. 最后结合 RAG 和测试，做一个完整小项目。
