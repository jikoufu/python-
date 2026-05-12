# 04 RAG 测试

## 学习目标

学完这一节，你需要知道：

- RAG 测试为什么比普通接口测试更复杂。
- 如何测试检索召回质量。
- 如何测试上下文相关性。
- 如何测试答案忠实性。
- 如何检测幻觉。
- 如何校验引用来源。

---

## RAG 系统的结构与测试层次

RAG（检索增强生成）系统由两个核心阶段组成：

```text
用户提问
    ↓
【检索阶段】
向量化提问 → 在向量数据库中搜索 → 返回 Top-K 文档片段
    ↓
【生成阶段】
将文档片段 + 用户提问拼入 Prompt → LLM 生成回答
    ↓
最终回答
```

这两个阶段都可能出错，所以 RAG 测试分两层：

| 测试层次 | 关注点 | 典型问题 |
|---------|--------|---------|
| 检索层测试 | 搜到的文档是否正确 | 该搜到的没搜到；搜了不相关的内容 |
| 生成层测试 | 基于文档的回答是否正确 | 答案和文档不一致；模型自己编内容 |

一个常见的错误认知是：**只测最终答案，不测检索结果**。

这样做的问题是：答案错了，你不知道是检索出了问题，还是生成出了问题，很难定位。

---

## 检索召回测试

### 核心概念

检索召回测试衡量：**用户提问时，相关文档是否被成功检索到**。

两个关键指标：

```text
召回率（Recall）：
  相关文档中，有多少被检索到了？
  = 被检索到的相关文档数 / 总相关文档数
  越高越好。

精确率（Precision）：
  被检索到的文档中，有多少是真正相关的？
  = 被检索到的相关文档数 / 总检索到的文档数
  越高越好。
```

### 准备检索测试集

测试集中每个样本包含：问题 + 哪些文档是相关的（Ground Truth）。

```json
[
  {
    "id": "ret_001",
    "question": "公司的年假政策是多少天？",
    "relevant_doc_ids": ["hr_policy_001", "hr_policy_002"],
    "note": "这两个文档包含年假相关内容"
  },
  {
    "id": "ret_002",
    "question": "报销流程需要哪些材料？",
    "relevant_doc_ids": ["finance_policy_003"],
    "note": "仅这一个文档描述了报销流程"
  }
]
```

### 检索召回测试脚本

```python
import json
from typing import Any


def get_retrieved_docs(question: str, top_k: int = 5) -> list[str]:
    """
    调用向量数据库，返回检索到的文档 ID 列表。
    这里是示意，实际替换为你的向量库调用。
    """
    # 示例：调用 Chroma
    # results = collection.query(
    #     query_texts=[question],
    #     n_results=top_k
    # )
    # return results["ids"][0]
    return []


def compute_retrieval_metrics(
    retrieved_ids: list[str],
    relevant_ids: list[str]
) -> dict:
    """计算单条样本的检索指标"""
    retrieved_set = set(retrieved_ids)
    relevant_set = set(relevant_ids)

    true_positives = retrieved_set & relevant_set   # 检索到且相关

    recall = len(true_positives) / len(relevant_set) if relevant_set else 0
    precision = len(true_positives) / len(retrieved_set) if retrieved_set else 0

    # Hit Rate：相关文档至少有一个被检索到
    hit = 1 if true_positives else 0

    return {
        "recall": round(recall, 3),
        "precision": round(precision, 3),
        "hit": hit,
        "retrieved_count": len(retrieved_set),
        "relevant_count": len(relevant_set),
        "true_positive_count": len(true_positives),
    }


def run_retrieval_test(test_file: str, top_k: int = 5):
    cases = json.loads(open(test_file, encoding="utf-8").read())

    all_recalls = []
    all_precisions = []
    all_hits = []

    for case in cases:
        retrieved = get_retrieved_docs(case["question"], top_k=top_k)
        metrics = compute_retrieval_metrics(retrieved, case["relevant_doc_ids"])

        all_recalls.append(metrics["recall"])
        all_precisions.append(metrics["precision"])
        all_hits.append(metrics["hit"])

        status = "✅" if metrics["hit"] else "❌"
        print(
            f"{status} [{case['id']}] "
            f"召回率={metrics['recall']:.2f} "
            f"精确率={metrics['precision']:.2f}"
        )
        if not metrics["hit"]:
            print(f"     未命中！相关文档：{case['relevant_doc_ids']}")
            print(f"     实际检索到：{retrieved}")

    avg_recall = sum(all_recalls) / len(all_recalls)
    avg_precision = sum(all_precisions) / len(all_precisions)
    hit_rate = sum(all_hits) / len(all_hits)

    print(f"\n{'='*40}")
    print(f"平均召回率：{avg_recall:.3f}")
    print(f"平均精确率：{avg_precision:.3f}")
    print(f"命中率（Hit Rate）：{hit_rate:.3f}")

    # 检索质量评估标准（参考）
    if hit_rate >= 0.9:
        print("✅ 检索质量良好")
    elif hit_rate >= 0.7:
        print("⚠️  检索质量一般，建议优化分块策略或 Embedding 模型")
    else:
        print("❌ 检索质量较差，需要重点排查")
```

### 检索质量差时的排查方向

```text
命中率低 → 按以下顺序排查：

1. 文档分块问题
   症状：问题的答案被切断在两个 chunk 之间
   解法：减小 chunk_size，增大 overlap，或改用语义分块

2. Embedding 模型不匹配
   症状：中文问题检索中文文档效果差
   解法：换成中文 Embedding 模型（如 BGE-M3）

3. 相似度阈值太高
   症状：检索返回的结果很少
   解法：降低阈值或增大 top_k

4. 文档没有被正确索引
   症状：直接搜关键词也找不到
   解法：检查文档加载和向量化流程是否有遗漏
```

---

## 上下文相关性测试

上下文相关性测试衡量：**检索到的文档，是否真的和用户问题相关**。

即使召回了文档，文档的内容也可能和问题关系不大（检索到了，但检索错了）。

### 用 LLM 评估相关性

```python
import anthropic

client = anthropic.Anthropic()


def score_context_relevance(question: str, context: str) -> dict:
    """
    用 LLM 对检索到的上下文打分。
    返回相关性分数（1-5）和理由。
    """
    prompt = f"""
请评估以下检索到的文档片段与用户问题的相关程度。

用户问题：
{question}

检索到的文档片段：
{context}

评分标准：
5 - 文档片段直接回答了用户问题
4 - 文档片段包含与问题高度相关的信息
3 - 文档片段部分相关，但不完整
2 - 文档片段与问题关系很小
1 - 文档片段与问题完全无关

请严格按照以下 JSON 格式输出，不要输出其他内容：
{{"score": 分数, "reason": "简短理由"}}
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=128,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        result = json.loads(response.content[0].text)
        return {"score": result["score"], "reason": result["reason"]}
    except Exception:
        return {"score": 0, "reason": "解析评分失败"}


def run_context_relevance_test(test_cases: list[dict]):
    """
    test_cases 格式：
    [{"question": "...", "retrieved_contexts": ["context1", "context2"]}]
    """
    all_scores = []

    for case in test_cases:
        question = case["question"]
        print(f"\n问题：{question}")

        for i, ctx in enumerate(case["retrieved_contexts"]):
            result = score_context_relevance(question, ctx)
            all_scores.append(result["score"])
            flag = "✅" if result["score"] >= 3 else "⚠️ "
            print(f"  {flag} 文档 {i+1} 相关性：{result['score']}/5 — {result['reason']}")

    avg = sum(all_scores) / len(all_scores) if all_scores else 0
    print(f"\n平均上下文相关性：{avg:.2f}/5")
```

---

## 答案忠实性测试

答案忠实性测试衡量：**模型给出的回答，是否基于检索到的文档，而不是自己"编"出来的**。

这是 RAG 测试中最重要的维度之一。

```text
忠实性问题示例：

检索到的文档内容：
"本公司年假为 10 天，工龄满 5 年后增至 15 天。"

用户问题：年假是多少天？

忠实的回答：年假为 10 天，工龄满 5 年后可增至 15 天。   ✅

不忠实的回答（模型编造）：年假为 15 天，节假日另算。  ❌
（文档中没有提到"节假日另算"）
```

### 忠实性评估脚本

```python
def check_faithfulness(
    question: str,
    context: str,
    answer: str
) -> dict:
    """
    检查答案是否忠实于检索到的上下文。
    """
    prompt = f"""
你是一个严格的事实核查员。请判断以下 AI 回答是否完全基于给定的参考文档。

用户问题：
{question}

参考文档：
{context}

AI 回答：
{answer}

判断标准：
- 如果 AI 回答的每一个事实都能在参考文档中找到依据，则"忠实"。
- 如果 AI 回答中有任何信息是参考文档中没有的（即使这个信息可能是正确的），也算"不忠实"。

请按以下 JSON 格式输出：
{{
  "faithful": true 或 false,
  "issues": ["具体哪句话不忠实（如果有）"],
  "score": 0到1之间的小数（1=完全忠实，0=完全不忠实）
}}
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        return json.loads(response.content[0].text)
    except Exception:
        return {"faithful": None, "issues": ["解析失败"], "score": None}


def run_faithfulness_test(test_cases: list[dict]):
    """
    test_cases 格式：
    [{"question": "...", "context": "...", "answer": "..."}]
    """
    scores = []

    for case in test_cases:
        result = check_faithfulness(
            case["question"],
            case["context"],
            case["answer"]
        )

        faithful = result.get("faithful")
        score = result.get("score", 0)
        scores.append(score)

        flag = "✅" if faithful else "❌"
        print(f"{flag} 问题：{case['question'][:30]}...")
        print(f"   忠实性分数：{score}")
        if result.get("issues"):
            for issue in result["issues"]:
                print(f"   问题：{issue}")

    avg = sum(scores) / len(scores) if scores else 0
    print(f"\n平均忠实性：{avg:.3f}")
    if avg < 0.8:
        print("⚠️  忠实性较低，建议检查 Prompt 中的指令约束或增加引用要求")
```

---

## 幻觉检测

幻觉是指模型生成了文档中不存在、甚至与事实相悖的内容。

### 幻觉的类型

```text
类型一：凭空捏造
  文档中完全没有这个信息，模型自己加上去了。
  示例：文档说"年假10天"，模型说"年假10天，另有带薪病假20天"。

类型二：混淆来源
  把 A 文档的信息安到了 B 问题的回答里。
  示例：用户问退款政策，模型却用了换货政策的内容来回答。

类型三：数字错误
  文档中的数字被模型记错或改写。
  示例：文档说"3个工作日"，模型说"3天"（可能指自然日）。

类型四：过度推断
  基于文档中有限的信息，模型进行了过度推理。
  示例：文档只说"支持微信支付"，模型说"支持所有主流支付方式"。
```

### 幻觉检测脚本

```python
def detect_hallucination(
    context: str,
    answer: str
) -> dict:
    """检测回答中是否存在幻觉"""

    prompt = f"""
你是一个严格的文本核查员。请仔细对比参考文档和 AI 回答，找出回答中所有无法在文档中找到依据的内容。

参考文档：
{context}

AI 回答：
{answer}

请将回答中每一个声明与文档对比核查，然后按以下 JSON 格式输出：
{{
  "has_hallucination": true 或 false,
  "hallucinated_parts": [
    {{
      "text": "回答中无依据的原文",
      "type": "凭空捏造 / 混淆来源 / 数字错误 / 过度推断"
    }}
  ]
}}

如果没有幻觉，hallucinated_parts 为空数组。
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        return json.loads(response.content[0].text)
    except Exception:
        return {"has_hallucination": None, "hallucinated_parts": []}
```

---

## 引用来源校验

如果 RAG 系统要求模型引用来源（如"根据《XX 政策》第3条"），需要校验引用是否真实存在。

### 引用校验逻辑

```python
def verify_citations(
    answer: str,
    retrieved_docs: list[dict]
) -> dict:
    """
    校验回答中的引用是否存在于检索到的文档中。

    retrieved_docs 格式：
    [{"id": "doc_001", "title": "XX政策", "content": "..."}]
    """
    doc_titles = {doc["title"] for doc in retrieved_docs}
    doc_ids = {doc["id"] for doc in retrieved_docs}

    issues = []

    # 简单方案：检查引用的文档标题是否在检索结果中
    # 实际项目中，可以让模型先提取引用，再做校验
    for doc_title in doc_titles:
        if doc_title in answer:
            # 找到引用，验证文档确实存在
            pass

    # 更完整的方案：用 LLM 提取引用并逐一核查
    extract_prompt = f"""
从以下 AI 回答中提取所有引用的文档名称或来源。
只输出 JSON 数组，格式：["来源1", "来源2"]
如果没有引用，输出 []

AI 回答：{answer}
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=128,
        messages=[{"role": "user", "content": extract_prompt}]
    )

    import json
    try:
        cited_sources = json.loads(response.content[0].text)
    except Exception:
        cited_sources = []

    # 核查每个引用是否在检索文档中
    for source in cited_sources:
        found = any(source in doc["title"] or source in doc["content"]
                    for doc in retrieved_docs)
        if not found:
            issues.append(f"引用了不存在的来源：'{source}'")

    return {
        "all_citations_valid": len(issues) == 0,
        "cited_sources": cited_sources,
        "issues": issues
    }
```

---

## RAG 测试的完整流程

```text
1. 建立测试集
   ├── 问题（来自真实用户或人工构造）
   ├── 相关文档 ID（Ground Truth，人工标注）
   └── 期望回答要点（可选）

2. 检索层测试
   ├── 召回率（Recall）
   ├── 精确率（Precision）
   └── 命中率（Hit Rate）

3. 生成层测试
   ├── 上下文相关性（Context Relevance）
   ├── 答案忠实性（Faithfulness）
   ├── 幻觉检测（Hallucination）
   └── 引用校验（Citation Verification）

4. 端到端指标
   └── 用户实际问题的答案正确率

5. 定位问题
   ├── 检索层有问题 → 优化分块、Embedding、检索参数
   └── 生成层有问题 → 优化 Prompt、增加引用约束
```

---

## 本节重点

- RAG 测试分检索层和生成层，两层都要测，才能准确定位问题。
- 检索层测召回率和命中率，判断相关文档有没有被找到。
- 生成层测忠实性和幻觉，判断模型有没有基于文档回答。
- 忠实性：答案中每一个信息都要能在文档中找到依据。
- 幻觉检测：关注凭空捏造、数字错误、过度推断三种常见类型。

## 自测问题

1. RAG 测试为什么要分检索层和生成层分别测试？
2. 召回率和精确率分别衡量什么？
3. 答案忠实性的判断标准是什么？
4. 幻觉有哪几种常见类型？举例说明。
5. 检索命中率很低时，应该从哪些方向排查？
