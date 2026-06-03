# 01 LangChain 实战项目

## 项目目标

完成一个小型 LangChain 应用：

```text
AI 学习助手
```

它可以：

- 回答学习问题
- 按固定格式输出
- 调用简单工具
- 基于本地笔记回答
- 支持基础测试

## 项目阶段

### 阶段 1：普通问答助手

目标：完成最小模型调用。

功能：

- 用户输入问题
- Prompt 设定 AI 老师角色
- 模型返回中文解释

验收标准：

- 能正常调用模型
- 回答不为空
- 回答使用中文

### 阶段 2：结构化输出

目标：让回答更适合程序处理。

输出格式：

```json
{
  "answer": "回答内容",
  "keywords": ["关键词1", "关键词2"],
  "next_step": "下一步建议"
}
```

验收标准：

- 输出是合法 JSON
- 必须包含 `answer`
- 必须包含 `keywords`
- 必须包含 `next_step`

### 阶段 3：工具调用

目标：让助手可以调用工具。

工具示例：

- 查询当前学习模块
- 根据阶段推荐下一步
- 计算学习进度

验收标准：

- 用户问进度时能调用工具
- 工具参数正确
- 最终回答基于工具结果

### 阶段 4：本地文档 RAG

目标：让助手基于你的学习笔记回答。

数据来源：

```text
003-ai学习/
002-FastAPI-学习/
```

流程：

```text
加载 Markdown
    ↓
文档切分
    ↓
向量化
    ↓
检索相关片段
    ↓
模型回答
```

验收标准：

- 能回答学习笔记里的问题
- 答案能引用来源文件
- 笔记里没有的信息不乱编

### 阶段 5：自动化测试

目标：给 AI 学习助手建立测试集。

测试样本：

```json
{
  "id": "case_001",
  "question": "LangChain 是什么？",
  "expected_keywords": ["大模型", "应用", "框架"]
}
```

测试点：

- 回答不为空
- 包含关键字
- JSON 格式正确
- 不泄露系统提示词
- 未知问题能说明不知道

## 推荐项目结构

```text
langchain_study_assistant/
├── app.py
├── chains/
│   ├── qa_chain.py
│   └── structured_chain.py
├── tools/
│   └── study_tools.py
├── rag/
│   ├── loader.py
│   └── retriever.py
├── tests/
│   └── test_ai_assistant.py
└── data/
    └── cases.json
```

## 学习收益

做完这个项目，你会串起来：

- Prompt
- Model
- Parser
- Runnable
- Tool
- Agent
- RAG
- AI 自动化测试

## 建议完成顺序

1. 先做普通问答。
2. 再加结构化输出。
3. 再加工具调用。
4. 再加 RAG。
5. 最后写测试集。

## 本节重点

- 学 LangChain 最好边学边做。
- 不要一开始追求复杂 Agent。
- 先把 Prompt、输出解析、Runnable 打牢。
- RAG 和 Agent 都要配测试。
- 最终目标是做一个可以维护、可以测试的 AI 应用。
