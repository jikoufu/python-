# AI 学习目录

这个目录用于系统学习 AI 应用开发，从数学基础、机器学习、深度学习，到大语言模型原理、Prompt 工程、RAG、Agent 开发，再到模型微调和生产部署，逐步构建完整的 AI 工程师知识体系。

## 目录结构

```text
003-ai学习/
├── README.md
├── 学习路径.md
├── 01-AI基础与数学/
├── 02-Python科学计算栈/
├── 03-机器学习基础/
├── 04-深度学习基础/
├── 05-大语言模型原理/
├── 06-Prompt工程/
├── 07-LangChain与LlamaIndex/
├── 08-RAG检索增强生成/
├── 09-AI-Agent开发/
├── 10-模型微调与部署/
├── 11-AI应用架构与工程化/
└── 12-实战项目/
```

## 学习模块

### 01-AI基础与数学

- AI、ML、DL 的关系与发展历史
- 线性代数：向量、矩阵、点积、矩阵乘法
- 微积分：导数、梯度、链式法则
- 概率与统计：概率分布、期望、条件概率、贝叶斯定理
- 信息论基础：熵、交叉熵、KL 散度

### 02-Python科学计算栈

- NumPy：多维数组、广播机制、向量化运算
- Pandas：数据读取、清洗、聚合、合并
- Matplotlib / Seaborn：数据可视化
- Scikit-learn：统一接口规范、Pipeline
- Jupyter Notebook：交互式开发与实验记录

### 03-机器学习基础

- 监督学习、无监督学习、强化学习的概念
- 线性回归与逻辑回归
- 决策树、随机森林、梯度提升（XGBoost/LightGBM）
- 特征工程：编码、归一化、特征选择
- 模型评估：过拟合、欠拟合、交叉验证、评估指标
- 超参数调优：网格搜索、随机搜索、Optuna

### 04-深度学习基础

- 神经网络结构：神经元、层、激活函数
- 前向传播与反向传播
- 损失函数与优化器（SGD、Adam）
- PyTorch 核心：Tensor、autograd、Dataset、DataLoader、nn.Module
- 卷积神经网络（CNN）
- 循环神经网络（RNN / LSTM）
- Transformer 架构详解
- 训练技巧：Dropout、BatchNorm、学习率调度

### 05-大语言模型原理

- 语言模型的演进：N-gram → Word2Vec → BERT → GPT
- Transformer 自注意力机制与位置编码
- 预训练与微调范式
- GPT 系列、Llama 系列、Claude 系列模型架构对比
- Tokenization：BPE、WordPiece、SentencePiece
- 上下文窗口、KV Cache、推理优化
- 模型能力的涌现现象

### 06-Prompt工程

- 什么是 Prompt Engineering
- 基础技巧：角色设定、格式约束、示例提供
- 思维链（Chain-of-Thought）提示
- Few-shot 与 Zero-shot 提示
- ReAct 提示范式
- 系统提示（System Prompt）设计
- 提示注入与安全防护
- Anthropic Claude API 使用与最佳实践

### 07-LangChain与LlamaIndex

- LangChain 核心概念：Chain、Runnable、LCEL
- 模型接口：LLM、ChatModel、Embeddings
- 提示模板（PromptTemplate）
- 输出解析器（OutputParser）
- 记忆模块（Memory）
- LlamaIndex 核心：Document、Node、Index
- 两个框架的适用场景与选型建议

### 08-RAG检索增强生成

- RAG 的原理与解决的问题
- 文档加载与分块策略（Chunking）
- Embedding 模型选型：OpenAI、BGE、text2vec
- 向量数据库：Chroma、Faiss、Qdrant、Weaviate、Milvus
- 相似度搜索：余弦相似度、ANN
- 混合检索：向量检索 + BM25 关键词检索
- 重排序（Rerank）：Cohere、BGE-Reranker
- RAG 评估：检索质量、生成质量、端到端指标
- 高级 RAG：HyDE、Self-RAG、Corrective RAG

### 09-AI-Agent开发

- Agent 的定义：感知 → 规划 → 行动 → 观察循环
- 工具调用（Tool Use / Function Calling）
- ReAct Agent 实现原理
- 多步推理与计划执行
- 多 Agent 协作框架：AutoGen、CrewAI、LangGraph
- 记忆系统：短期记忆、长期记忆、外部存储
- Agent 评估与调试
- Human-in-the-loop 设计

### 10-模型微调与部署

- 为什么需要微调
- 全参数微调 vs 参数高效微调（PEFT）
- LoRA / QLoRA 原理与实践
- 指令微调（Instruction Tuning）数据集构建
- 使用 HuggingFace Transformers 微调
- 量化技术：INT8、INT4、GGUF
- 模型推理服务：vLLM、Ollama、llama.cpp
- API 服务封装：FastAPI + 模型推理

### 11-AI应用架构与工程化

- AI 应用的典型架构模式
- 流式输出（Streaming）实现
- 异步并发处理 LLM 请求
- 对话历史管理与上下文压缩
- 成本控制：Token 计算、缓存策略、模型降级
- 可观测性：日志、追踪（LangSmith、Phoenix）
- 安全与合规：内容过滤、PII 脱敏
- 性能优化：批处理、并发、CDN 缓存

### 12-实战项目

- 智能文档问答系统（RAG）
- 多工具 AI 助手（Agent）
- 个人知识库（本地部署 + 向量检索）
- AI 代码审查助手
- 多模态图文理解应用

## 推荐学习方式

每个模块建议采用以下节奏：

1. 先理解核心概念，弄清楚"为什么需要它"。
2. 写一个最小可运行示例，验证理解。
3. 完成配套练习，覆盖常见场景。
4. 整理笔记，提炼关键结论。
5. 把当前模块的能力整合进阶段性项目。

## 技术栈总览

| 层次 | 技术 |
|------|------|
| 语言模型 API | Anthropic Claude、OpenAI GPT、HuggingFace |
| 开发框架 | LangChain、LlamaIndex、LangGraph |
| 向量数据库 | Chroma、Qdrant、Faiss |
| 模型推理 | vLLM、Ollama、HuggingFace Transformers |
| 微调工具 | PEFT、TRL、Axolotl |
| 后端服务 | FastAPI + asyncio |
| 可观测性 | LangSmith、Arize Phoenix |

## 最终目标

完成后具备独立设计和实现以下能力：

- 基于 RAG 的企业知识库问答系统
- 具备工具调用能力的 AI Agent
- 本地部署并微调开源大语言模型
- 生产级 AI 应用的架构设计与性能优化
