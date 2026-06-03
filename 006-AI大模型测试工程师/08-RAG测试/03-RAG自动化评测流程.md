# 03 RAG 自动化评测流程

## 学习目标

这一节学习如何把 RAG 测试做成自动化评测。

你需要掌握：

- 自动化评测流程。
- 测试数据格式。
- 基础断言。
- RAGAS 类指标。
- 如何输出评测报告。

## 自动化流程

```text
读取测试集
    ↓
调用 RAG 应用接口
    ↓
保存 answer / contexts / sources
    ↓
执行规则断言
    ↓
执行指标评估
    ↓
统计通过率
    ↓
输出报告
```

## 接口响应建议格式

为了方便测试，RAG 接口最好返回：

```json
{
  "question": "员工年假规则是什么？",
  "answer": "员工满一年后享有年假...",
  "contexts": [
    {
      "content": "员工满一年后享有5天年假...",
      "source": "员工手册.md",
      "score": 0.87
    }
  ],
  "sources": ["员工手册.md"],
  "usage": {
    "prompt_tokens": 1200,
    "completion_tokens": 200
  }
}
```

如果接口只返回 `answer`，测试会很难定位问题。

## 基础规则断言

可以先做不依赖 LLM Judge 的断言：

```python
assert response.status_code == 200
assert data["answer"]
assert "员工手册.md" in data["sources"]
assert any("年假" in ctx["content"] for ctx in data["contexts"])
```

优点：

- 快
- 便宜
- 稳定

缺点：

- 不能完整判断语义质量

## 指标评估

RAGAS 文档中常见 RAG 指标包括 Context Precision、Context Recall、Faithfulness 等。可以用这些指标判断检索上下文是否相关、必要上下文是否被召回、答案是否忠实于上下文。

常见指标解释：

| 指标 | 关注点 | 失败说明 |
|------|--------|----------|
| Context Precision | 检索结果是否相关 | 检索到了很多无关片段 |
| Context Recall | 必要上下文是否召回 | 正确资料没被找出来 |
| Faithfulness | 答案是否基于上下文 | 模型可能幻觉 |
| Answer Relevancy | 是否回答用户问题 | 答非所问 |

## 评测报告模板

```markdown
# RAG 评测报告

## 测试范围

- 知识库：员工手册、报销制度、系统操作文档
- 测试样本：100 条
- 模型版本：xxx
- Embedding 版本：xxx
- 向量库：xxx

## 总体结果

| 指标 | 结果 |
|------|------|
| 总用例数 | 100 |
| 通过数 | 86 |
| 失败数 | 14 |
| 通过率 | 86% |
| 平均响应时间 | 2.4s |
| 平均 Token | 1500 |

## 失败分类

| 类型 | 数量 |
|------|------|
| 检索未命中 | 5 |
| 答案幻觉 | 4 |
| 引用错误 | 3 |
| 拒答错误 | 2 |

## 典型失败样本

### RAG_023

- 问题：xxx
- 期望来源：xxx
- 实际来源：xxx
- 实际回答：xxx
- 失败原因：检索未命中

## 修复建议

- 调整 chunk size。
- 增加关键词检索。
- 加 rerank。
- 修改拒答 Prompt。
```

## RAG 自动化测试优先级

建议按这个顺序做：

1. 接口可用性测试。
2. 答案非空测试。
3. 来源文档命中测试。
4. 关键字和答案要点测试。
5. 未知问题拒答测试。
6. 引用准确性测试。
7. RAGAS / LLM Judge 指标。
8. 性能和成本统计。

## 本节重点

- RAG 接口最好返回 contexts 和 sources。
- 自动化评测先做规则断言，再做 LLM Judge。
- 指标要能帮助定位问题，而不是只给一个总分。
- 评测报告要包含失败分类和修复建议。
