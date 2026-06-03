# 01 LangChain 检索与 RAG

## 学习目标

这一节学习如何用 LangChain 做检索增强生成，也就是 RAG。

你需要掌握：

- 为什么需要 RAG。
- LangChain 中 RAG 的基本组件。
- Document、Loader、Splitter、Embedding、Vector Store、Retriever 的作用。
- 2-step RAG 和 Agentic RAG 的区别。

## 为什么需要 RAG

大模型有两个明显限制：

- 上下文窗口有限，不能一次塞入所有资料。
- 训练知识固定，无法自动知道最新或私有资料。

RAG 的思路是：

```text
用户问题
    ↓
检索相关资料
    ↓
把资料放进 Prompt
    ↓
模型基于资料回答
```

这样模型就能回答企业文档、课程笔记、本地知识库里的问题。

## RAG 基本组件

### 1. Document

文档对象，通常包含：

- 文本内容
- 元数据

例如：

```text
page_content：文档正文
metadata：来源、文件名、页码
```

### 2. Loader

加载器，用来读取外部资料：

- PDF
- Markdown
- TXT
- 网页
- 数据库

### 3. Text Splitter

文本切分器。

长文档不能直接全部塞给模型，需要切成 chunk。

常见考虑：

- chunk 大小
- overlap 重叠
- 按段落切
- 按标题切

### 4. Embedding

Embedding 把文本转换成向量。

向量可以用来计算语义相似度。

### 5. Vector Store

向量数据库，用来保存文本向量。

常见选择：

- Chroma
- FAISS
- Qdrant
- Milvus

### 6. Retriever

检索器，根据用户问题找相关文档。

流程：

```text
问题 → 向量 → 相似度搜索 → 返回相关文档
```

## 2-step RAG

2-step RAG 是固定流程：

```text
先检索
再生成
```

优点：

- 简单
- 可控
- 容易测试

适合大多数知识库问答。

## Agentic RAG

Agentic RAG 是把检索变成 Agent 可调用的工具。

流程更像：

```text
用户问题
    ↓
Agent 判断是否需要检索
    ↓
调用检索工具
    ↓
根据结果继续检索或回答
```

优点：

- 更灵活
- 可多次检索
- 可结合多个工具

缺点：

- 更难测试
- 延迟更高
- 结果更不稳定

## RAG 测试重点

RAG 应用必须测试：

- 检索是否命中正确文档
- 文档切分是否合理
- 回答是否基于上下文
- 是否编造知识库没有的信息
- 引用来源是否准确
- 未知问题是否拒答

## 建议练习

1. 准备一个 Markdown 文档。
2. 加载文档。
3. 切分文档。
4. 生成 embedding。
5. 存入向量数据库。
6. 根据问题检索相关 chunk。
7. 把检索结果交给模型回答。
8. 写 5 条 RAG 测试样本。

## 本节重点

- RAG 用外部知识增强模型回答。
- RAG 的核心是检索质量和回答忠实性。
- 2-step RAG 简单稳定。
- Agentic RAG 灵活但更难控制。
- 做 RAG 一定要配测试集。
