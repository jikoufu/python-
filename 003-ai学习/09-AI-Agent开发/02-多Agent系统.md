# 多 Agent 系统

> **一句话先说清楚**：单个 Agent 像一个全能员工，什么都做但容易超负荷；多 Agent 系统像一个分工协作的团队，每个 Agent 只做自己最擅长的部分，复杂任务拆给多人并行处理。

---

## 第一部分：为什么需要多 Agent（总）

### 单 Agent 的三个天花板

读完上一篇（01-理解AI-Agent.md）你已经知道单 Agent 怎么工作了。但随着任务复杂度上升，单 Agent 会遇到三道硬墙。

**天花板一：上下文窗口限制**

一个 Agent 处理复杂任务时，对话历史会越来越长：

```
步骤1的思考 + 工具结果
步骤2的思考 + 工具结果
步骤3的思考 + 工具结果
...
步骤20的思考 + 工具结果   ← context window 快撑满了
```

当上下文过长，模型开始"遗忘"前面的内容，推理质量下降。

**天花板二：专业能力无法同时拉满**

一个 Prompt 很难让同一个模型同时做到：
- 精准的法律条文分析
- 严谨的 Python 代码生成  
- 流畅的中文文案写作

每加一个领域的要求，其他领域的表现都会被稀释。

**天花板三：串行执行，无法并行**

单 Agent 是严格串行的：做完第一步才能做第二步。
但很多任务的子任务之间没有依赖关系，完全可以并行：

```
任务：分析三个竞争对手的官网内容

串行（单 Agent）：
  爬取A → 分析A → 爬取B → 分析B → 爬取C → 分析C → 汇总
  耗时：6分钟

并行（多 Agent）：
  Agent1: 爬取A → 分析A ↘
  Agent2: 爬取B → 分析B  → 汇总 Agent → 最终报告
  Agent3: 爬取C → 分析C ↗
  耗时：2分钟
```

---

### 多 Agent 的本质

多 Agent 系统 = **让多个 Agent 分工协作，共同完成一个单个 Agent 无法高效完成的任务**。

每个 Agent 可以：
- 有不同的 System Prompt（专业化）
- 有不同的工具集（能力边界清晰）
- 并行运行（效率提升）
- 相互检查对方的输出（质量保障）

这和人类团队的分工逻辑完全一致。

---

## 第二部分：四种核心协作模式（分）

多 Agent 系统有四种经典的拓扑结构，每种解决不同的问题。

### 模式一：Supervisor（主管 + 下属）

**结构：**

```
用户
  ↓
Supervisor Agent（主管）
  ├── 分配任务 → Worker Agent A（专项能力）
  ├── 分配任务 → Worker Agent B（专项能力）
  └── 分配任务 → Worker Agent C（专项能力）
                              ↓
                    汇总结果 → Supervisor
                              ↓
                           回复用户
```

**特点：**
- Supervisor 负责理解任务、分配、整合结果，自己不干具体活
- Worker 只专注自己的专业领域，不需要了解全局
- 最常见的多 Agent 模式

**适用场景：**
- 任务需要多个专业领域协作（研究 + 写作 + 数据分析）
- 子任务可以明确划分给不同 Agent

---

### 模式二：Pipeline（流水线）

**结构：**

```
用户
  ↓
Agent A（采集）→ Agent B（清洗）→ Agent C（分析）→ Agent D（报告）
                                                           ↓
                                                        回复用户
```

**特点：**
- 每个 Agent 处理上一个 Agent 的输出，输出给下一个
- 严格顺序执行，每步有明确的输入输出格式
- 每个 Agent 只关注自己的那一步

**适用场景：**
- 数据处理流水线（爬取 → 解析 → 分析 → 可视化）
- 内容生产流水线（选题 → 研究 → 撰写 → 审校）
- 各步骤有明显的前后依赖关系

---

### 模式三：Peer-to-Peer（平等对话）

**结构：**

```
Agent A（提出方案）
    ↕  相互讨论、质疑、完善
Agent B（批评改进）
    ↕
Agent A（回应批评）
    ↕
Agent B（达成共识 or 继续讨论）
    ↓
最终输出
```

**特点：**
- 两个或多个 Agent 扮演不同角色（支持方/反对方、作者/审稿人）
- 通过辩论和互相审查提高输出质量
- 也叫 Reflection（反思）模式或 Debate（辩论）模式

**适用场景：**
- 需要高质量输出的场景（代码审查、文章润色、方案评审）
- 防止单个 Agent 的偏见和错误
- 复杂决策需要多角度权衡

---

### 模式四：Swarm（动态路由）

**结构：**

```
用户输入
    ↓
路由判断：这个任务适合哪个 Agent？
    ├── 技术问题 → Tech Agent（处理完可以转给其他 Agent）
    ├── 销售问题 → Sales Agent（处理完可以转给其他 Agent）
    └── 账单问题 → Billing Agent（处理完可以转给其他 Agent）
                         ↓
              Agent 自主决定是否转交给其他 Agent
```

**特点：**
- 没有固定的 Supervisor，Agent 之间可以自主互相移交（Handoff）
- 路由是动态的，由当前处理 Agent 决定下一步
- 更灵活，但更难控制

**适用场景：**
- 客服系统（技术、售后、财务等不同专线）
- 医疗分诊（根据症状转给不同科室 Agent）

---

## 第三部分：Agent 之间如何通信

多 Agent 系统中，Agent 之间需要传递信息。有三种方式。

### 方式一：共享消息列表（最简单）

把所有 Agent 的输入输出放在同一个消息列表里，所有 Agent 都能看到全部历史。

```python
# 共享的对话历史
shared_history = [
    {"role": "user", "content": "帮我写一篇关于AI的文章"},
    {"role": "assistant", "content": "[Researcher]: 以下是我找到的资料..."},
    {"role": "assistant", "content": "[Writer]: 基于以上资料，文章草稿如下..."},
    {"role": "assistant", "content": "[Editor]: 我对以下部分提出修改意见..."},
]
```

**优点**：简单，所有 Agent 有完整上下文。
**缺点**：历史越来越长，上下文消耗大。

---

### 方式二：结构化状态（推荐）

用一个共享的数据结构存储任务状态，每个 Agent 读取和更新自己负责的字段。

```python
from typing import TypedDict, Optional

class TeamState(TypedDict):
    """整个多 Agent 系统的共享状态"""
    # 输入
    task: str                        # 用户的原始任务

    # 各 Agent 的工作产物
    research_result: Optional[str]   # Researcher 的调研结果
    draft: Optional[str]             # Writer 的初稿
    review_comments: Optional[str]   # Reviewer 的审稿意见
    final_output: Optional[str]      # 最终输出

    # 控制流
    current_agent: str               # 当前哪个 Agent 在工作
    iteration: int                   # 修改轮次（防止无限循环）
    is_approved: bool                # Reviewer 是否通过
```

**优点**：结构清晰，每个 Agent 只更新自己的字段。
**缺点**：需要提前设计好状态结构。

---

### 方式三：消息传递（Handoff）

Agent A 完成工作后，显式地把任务"移交"给 Agent B，并附上移交说明。

```python
from dataclasses import dataclass

@dataclass
class Handoff:
    """Agent 之间的任务移交"""
    from_agent: str       # 谁移交的
    to_agent: str         # 移交给谁
    message: str          # 移交时的说明
    context: dict         # 附带的上下文数据
```

---

## 第四部分：从零手写一个多 Agent 系统

不用框架，手动实现一个"研究员 + 写作者 + 审稿人"三 Agent 协作系统。

### 场景

任务：给定一个主题，生成一篇高质量的技术文章。

```
Researcher Agent：负责分析主题，整理关键知识点
Writer Agent：   负责根据研究结果写作
Reviewer Agent： 负责审稿，判断是否通过，或给出修改意见
（如果不通过，Writer 根据意见修改，最多循环 3 次）
```

### 完整代码

```python
import anthropic
from dataclasses import dataclass, field
from typing import Optional

client = anthropic.Anthropic()

# ─── 定义共享状态 ─────────────────────────────────────────────

@dataclass
class ArticleState:
    topic: str
    research: str = ""
    draft: str = ""
    review: str = ""
    final: str = ""
    approved: bool = False
    iteration: int = 0
    max_iterations: int = 3

# ─── 定义每个 Agent ───────────────────────────────────────────

def researcher_agent(state: ArticleState) -> ArticleState:
    """
    Researcher Agent：分析主题，整理关键知识点和写作角度。
    输入：topic
    输出：research（写入 state.research）
    """
    print(f"\n{'='*50}")
    print("🔍 Researcher Agent 开始工作...")

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system="""你是一个专业的技术研究员。
你的任务是：给定一个主题，整理出关键知识点、核心概念、常见误解和写作角度。
输出结构化的研究摘要，供后续写作使用。
格式：用 Markdown 列表，分为【核心概念】【关键知识点】【常见误解】【推荐写作角度】四部分。""",
        messages=[
            {"role": "user", "content": f"请分析以下主题并整理研究摘要：{state.topic}"}
        ]
    )

    state.research = response.content[0].text
    print(f"研究摘要已完成（{len(state.research)} 字）")
    return state


def writer_agent(state: ArticleState) -> ArticleState:
    """
    Writer Agent：根据研究结果（和审稿意见）写作或修改文章。
    输入：research + review（如果有）
    输出：draft（写入 state.draft）
    """
    is_revision = bool(state.review)

    print(f"\n{'='*50}")
    if is_revision:
        print(f"✍️  Writer Agent 开始修改（第 {state.iteration} 次）...")
    else:
        print("✍️  Writer Agent 开始写作...")

    # 根据是否是修改轮次，构造不同的 Prompt
    if is_revision:
        user_msg = f"""请根据审稿意见修改文章。

【原始研究摘要】
{state.research}

【上一版文章】
{state.draft}

【审稿意见】
{state.review}

请针对审稿意见进行修改，输出完整的修改版文章。"""
    else:
        user_msg = f"""请根据以下研究摘要，写一篇面向开发者的技术文章。

【主题】{state.topic}

【研究摘要】
{state.research}

要求：
- 1200-1500 字
- 结构清晰（引言、主体、总结）
- 有代码示例或具体案例
- 语言简洁，避免废话"""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        system="你是一个经验丰富的技术文章写作者，擅长把复杂技术写得清晰易懂。",
        messages=[{"role": "user", "content": user_msg}]
    )

    state.draft = response.content[0].text
    print(f"文章草稿已完成（{len(state.draft)} 字）")
    return state


def reviewer_agent(state: ArticleState) -> ArticleState:
    """
    Reviewer Agent：审稿，判断是否通过，给出具体修改意见。
    输入：draft
    输出：review + approved（写入 state）
    """
    print(f"\n{'='*50}")
    print("📝 Reviewer Agent 开始审稿...")

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system="""你是一个严格的技术文章主编。
你的任务是审稿：判断文章质量，给出明确结论。

审核标准：
1. 技术内容是否准确
2. 结构是否清晰
3. 是否有具体例子
4. 语言是否简洁

输出格式（严格按此格式）：
【审核结论】通过 或 需要修改
【评分】X/10
【问题清单】（如果需要修改，列出具体问题，每条一行）
【修改建议】（针对每个问题的改进方向）""",
        messages=[
            {
                "role": "user",
                "content": f"请审核以下文章：\n\n主题：{state.topic}\n\n{state.draft}"
            }
        ]
    )

    review_text = response.content[0].text
    state.review = review_text

    # 解析是否通过
    state.approved = "通过" in review_text and "需要修改" not in review_text

    print(f"审稿完成：{'✅ 通过' if state.approved else '❌ 需要修改'}")
    if not state.approved:
        # 提取问题清单（简单文本解析）
        lines = review_text.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('【'):
                print(f"  · {line.strip()}")

    return state


# ─── 多 Agent 协调器 ──────────────────────────────────────────

def run_article_team(topic: str) -> str:
    """
    协调三个 Agent 完成文章写作任务。
    流程：Researcher → Writer → Reviewer → (Writer → Reviewer) × N → 最终输出
    """
    print(f"\n🚀 启动写作团队，主题：{topic}")

    state = ArticleState(topic=topic)

    # 第一步：研究员调研
    state = researcher_agent(state)

    # 第二步：写作 + 审稿循环
    while state.iteration <= state.max_iterations:

        # Writer 写作（或根据意见修改）
        state = writer_agent(state)

        # Reviewer 审稿
        state = reviewer_agent(state)

        state.iteration += 1

        if state.approved:
            print(f"\n✅ 审稿通过！（共迭代 {state.iteration} 次）")
            state.final = state.draft
            break

        if state.iteration > state.max_iterations:
            print(f"\n⚠️  达到最大迭代次数（{state.max_iterations}），使用最新版本")
            state.final = state.draft
            break

    print(f"\n{'='*50}")
    print("📄 最终文章已生成")
    print(f"{'='*50}\n")

    return state.final


# ─── 运行示例 ─────────────────────────────────────────────────

if __name__ == "__main__":
    result = run_article_team("Python 异步编程：asyncio 从入门到实践")
    print(result)
```

### 执行流程可视化

```
run_article_team("Python 异步编程")
        │
        ▼
researcher_agent()
  → 分析主题，输出研究摘要
  → state.research = "【核心概念】..."
        │
        ▼
writer_agent()（第1次，写初稿）
  → 根据研究摘要写文章
  → state.draft = "# Python 异步编程..."
        │
        ▼
reviewer_agent()
  → 审核文章
  → state.approved = False（需要修改）
  → state.review = "问题：缺少实际代码示例..."
        │
        ▼
writer_agent()（第2次，根据意见修改）
  → 加入代码示例，改进结构
  → state.draft = "# Python 异步编程...（改进版）"
        │
        ▼
reviewer_agent()
  → 再次审核
  → state.approved = True（通过！）
        │
        ▼
    最终输出
```

---

## 第五部分：用 LangGraph 实现多 Agent

手写版本展示了原理，LangGraph 让多 Agent 协作更健壮、可扩展。

LangGraph 的核心优势：
- **状态持久化**：每个节点的状态自动保存，支持断点续跑
- **可视化**：图结构清晰，容易理解和调试
- **条件路由**：内置条件边，轻松实现"通过/不通过"的分支逻辑
- **流式输出**：原生支持，可以实时看到每个 Agent 的输出

### 用 LangGraph 重新实现写作团队

```python
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# ─── 定义共享状态 ─────────────────────────────────────────────

class ArticleTeamState(TypedDict):
    topic: str
    research: str
    draft: str
    review: str
    approved: bool
    iteration: int
    # 消息历史（每个节点的输出追加在这里，用于调试）
    messages: Annotated[list, operator.add]

# ─── 定义三个 Agent 节点 ──────────────────────────────────────

llm = ChatAnthropic(model="claude-haiku-4-5")

def researcher_node(state: ArticleTeamState) -> dict:
    """研究员节点"""
    response = llm.invoke([
        SystemMessage(content="""你是技术研究员。分析主题，整理关键知识点。
格式：用 Markdown 分为【核心概念】【关键知识点】【写作角度】。"""),
        HumanMessage(content=f"分析主题：{state['topic']}")
    ])
    research = response.content
    print(f"🔍 Researcher 完成（{len(research)} 字）")
    return {
        "research": research,
        "messages": [f"[Researcher] 完成研究，共 {len(research)} 字"]
    }


def writer_node(state: ArticleTeamState) -> dict:
    """写作者节点"""
    is_revision = bool(state.get("review"))

    if is_revision:
        user_content = f"""根据审稿意见修改文章。

【研究摘要】{state['research']}
【上一版】{state['draft']}
【审稿意见】{state['review']}

请输出完整修改版。"""
    else:
        user_content = f"""根据研究摘要写文章。
主题：{state['topic']}
研究摘要：{state['research']}
要求：1200字，有代码示例，结构清晰。"""

    response = llm.invoke([
        SystemMessage(content="你是技术写作专家。"),
        HumanMessage(content=user_content)
    ])
    draft = response.content
    action = "修改" if is_revision else "初稿"
    print(f"✍️  Writer 完成{action}（{len(draft)} 字）")

    return {
        "draft": draft,
        "iteration": state.get("iteration", 0) + 1,
        "messages": [f"[Writer] 完成第 {state.get('iteration', 0) + 1} 次{'修改' if is_revision else '写作'}"]
    }


def reviewer_node(state: ArticleTeamState) -> dict:
    """审稿人节点"""
    response = llm.invoke([
        SystemMessage(content="""你是严格的技术主编。审核文章。
输出格式：
【审核结论】通过 或 需要修改
【问题】（如有，每条一行）
【建议】"""),
        HumanMessage(content=f"审核文章：\n\n主题：{state['topic']}\n\n{state['draft']}")
    ])

    review = response.content
    approved = "通过" in review and "需要修改" not in review
    print(f"📝 Reviewer 完成：{'✅ 通过' if approved else '❌ 需要修改'}")

    return {
        "review": review,
        "approved": approved,
        "messages": [f"[Reviewer] {'通过' if approved else '需要修改'}"]
    }

# ─── 定义路由逻辑 ─────────────────────────────────────────────

def should_revise(state: ArticleTeamState) -> str:
    """
    审稿后的路由：
    - 通过 or 超过最大迭代 → END
    - 否则 → 回到 writer 修改
    """
    if state.get("approved"):
        return "approved"
    if state.get("iteration", 0) >= 3:
        return "max_iterations"
    return "revise"

# ─── 构建图 ───────────────────────────────────────────────────

def build_article_team():
    graph = StateGraph(ArticleTeamState)

    # 添加节点
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer",     writer_node)
    graph.add_node("reviewer",   reviewer_node)

    # 设置入口：从 researcher 开始
    graph.set_entry_point("researcher")

    # 固定边：researcher → writer → reviewer
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer",     "reviewer")

    # 条件边：reviewer 之后根据结果决定走哪里
    graph.add_conditional_edges(
        "reviewer",
        should_revise,
        {
            "approved":       END,        # 通过，结束
            "max_iterations": END,        # 超限，结束
            "revise":         "writer",   # 需要修改，回到 writer
        }
    )

    return graph.compile()


# ─── 运行 ─────────────────────────────────────────────────────

def run(topic: str) -> str:
    agent = build_article_team()

    initial_state = {
        "topic": topic,
        "research": "",
        "draft": "",
        "review": "",
        "approved": False,
        "iteration": 0,
        "messages": []
    }

    final_state = agent.invoke(initial_state)

    print("\n执行日志：")
    for msg in final_state["messages"]:
        print(f"  {msg}")

    return final_state["draft"]


# 运行
result = run("Python 异步编程：asyncio 从入门到实践")
```

### 图结构可视化

```
researcher
    │
    ▼
  writer ◄─────────────────────┐
    │                          │（需要修改，iteration < 3）
    ▼                          │
reviewer                       │
    │                          │
    ├── approved=True  → END   │
    ├── iteration>=3   → END   │
    └── otherwise      ────────┘
```

---

## 第六部分：Supervisor 模式的完整实现

Supervisor 是最常用的多 Agent 模式，单独详细展示。

```python
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# ─── 定义 Supervisor 的决策输出格式 ──────────────────────────

WORKERS = ["researcher", "coder", "writer"]

class SupervisorDecision(TypedDict):
    next: Literal["researcher", "coder", "writer", "FINISH"]
    reason: str   # 为什么选择这个 Worker

# ─── 状态定义 ─────────────────────────────────────────────────

class SupervisorState(TypedDict):
    task: str
    messages: Annotated[list, operator.add]   # 所有 Agent 的输出汇总在这里
    next: str                                  # 下一个要执行的 Agent

# ─── Supervisor Agent（调度员）──────────────────────────────

llm = ChatAnthropic(model="claude-haiku-4-5")

SUPERVISOR_PROMPT = """你是一个任务调度员，负责把复杂任务分配给合适的专家团队来完成。

你的团队成员：
- researcher：擅长信息检索、数据收集、背景调研
- coder：擅长编写代码、调试、技术实现
- writer：擅长文案写作、内容整理、报告输出

当前任务：{task}
已完成的工作：
{history}

请决定下一步应该由谁来处理，或者任务已经完成（输出 FINISH）。
输出 JSON 格式：{{"next": "团队成员名或FINISH", "reason": "理由"}}"""


def supervisor_node(state: SupervisorState) -> dict:
    """Supervisor 节点：决定下一步由谁来做"""

    history = "\n".join(state["messages"]) if state["messages"] else "（尚未开始）"

    response = llm.invoke([
        {"role": "user", "content": SUPERVISOR_PROMPT.format(
            task=state["task"],
            history=history
        )}
    ])

    import json, re
    text = response.content
    # 提取 JSON
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        decision = json.loads(match.group())
    else:
        decision = {"next": "FINISH", "reason": "无法解析决策"}

    print(f"\n🎯 Supervisor 决策：→ {decision['next']}（{decision['reason']}）")
    return {"next": decision["next"]}


# ─── Worker Agent 节点 ────────────────────────────────────────

def make_worker_node(role: str, expertise: str):
    """工厂函数：生成一个 Worker 节点"""
    def worker_node(state: SupervisorState) -> dict:
        print(f"\n⚙️  {role} 开始工作...")
        response = llm.invoke([
            {"role": "system", "content": f"你是{expertise}。针对当前任务完成你负责的部分，输出具体成果。"},
            {"role": "user", "content": f"任务：{state['task']}\n\n已有进展：\n" + "\n".join(state["messages"][-3:])}
        ])
        result = f"[{role}] {response.content[:200]}..."
        print(f"  完成（{len(response.content)} 字）")
        return {"messages": [result]}
    return worker_node


# ─── 构建 Supervisor 图 ───────────────────────────────────────

def build_supervisor_team():
    graph = StateGraph(SupervisorState)

    # 添加节点
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", make_worker_node("Researcher", "信息检索和调研专家"))
    graph.add_node("coder",      make_worker_node("Coder",      "Python 开发专家"))
    graph.add_node("writer",     make_worker_node("Writer",     "技术写作专家"))

    # 入口：先由 Supervisor 决策
    graph.set_entry_point("supervisor")

    # Worker 完成后，都回到 Supervisor
    for worker in WORKERS:
        graph.add_edge(worker, "supervisor")

    # Supervisor 的路由：根据 next 字段决定去哪个 Worker 或结束
    def route_by_supervisor(state: SupervisorState) -> str:
        return state["next"] if state["next"] != "FINISH" else END

    graph.add_conditional_edges(
        "supervisor",
        route_by_supervisor,
        {**{w: w for w in WORKERS}, END: END}
    )

    return graph.compile()


# ─── 运行 ─────────────────────────────────────────────────────

supervisor_team = build_supervisor_team()

result = supervisor_team.invoke({
    "task": "调研 Python 异步编程的最佳实践，写一份包含代码示例的技术报告",
    "messages": [],
    "next": ""
})

print("\n最终产出：")
for msg in result["messages"]:
    print(f"  {msg[:100]}...")
```

---

## 第七部分：设计原则与常见坑（总）

### 7.1 什么时候用多 Agent

不是所有任务都需要多 Agent。错误使用会带来更高的复杂度和成本。

```
判断流程：

这个任务可以分解成相互独立的子任务吗？
├── 否 → 单 Agent 更合适
└── 是 → 子任务需要不同专业能力吗？
          ├── 否 → 单 Agent 配合好的 Prompt 即可
          └── 是 → 子任务是否可以并行？
                    ├── 是 → 多 Agent（并行提速）
                    └── 否 → 考虑单 Agent Pipeline（更简单）
```

| 任务类型 | 推荐方案 |
|---------|---------|
| 简单问答 | 单次 LLM 调用 |
| 有工具调用的任务 | 单 Agent（ReAct） |
| 需要多专业领域的复杂任务 | 多 Agent（Supervisor） |
| 有明确步骤的流水线任务 | 多 Agent（Pipeline） |
| 需要高质量、自我校验 | 多 Agent（Peer-to-Peer） |

---

### 7.2 五个常见设计错误

**错误一：Agent 职责不清晰**

```python
# ❌ 不清晰：Writer 既写作又审稿
writer_prompt = "你是写作者，负责写文章，写完也要自己检查质量"

# ✅ 清晰：职责单一
writer_prompt  = "你是写作者，只负责根据研究摘要写作，不做其他判断"
reviewer_prompt = "你是审稿人，只负责评审文章质量，不修改内容"
```

**错误二：没有限制最大循环次数**

```python
# ❌ 危险：无限循环
while not state.approved:
    state = writer_agent(state)
    state = reviewer_agent(state)

# ✅ 安全：有退出条件
MAX_ITER = 3
while not state.approved and state.iteration < MAX_ITER:
    state = writer_agent(state)
    state = reviewer_agent(state)
    state.iteration += 1
```

**错误三：Agent 之间传递了过多无用上下文**

```python
# ❌ 把所有历史都传给每个 Agent，浪费 Token，影响专注度
coder_input = f"""
研究员说：{research_result}（2000字）
写作者说：{writer_result}（3000字）
现在请你写代码...
"""

# ✅ 只传和当前 Agent 任务相关的信息
coder_input = f"""
请根据以下功能需求写代码：
{functional_requirements}  # 精炼后的需求，100字
"""
```

**错误四：Supervisor 自己做了太多工作**

```python
# ❌ Supervisor 既调度又实现，失去了多 Agent 的意义
def supervisor_node(state):
    # Supervisor 自己写了代码、写了文章、做了调研...
    pass

# ✅ Supervisor 只做调度决策，实际工作交给 Worker
def supervisor_node(state):
    # 只决定：下一步由谁来做
    return {"next": "researcher"}
```

**错误五：没有测试单个 Agent 就测整个系统**

```python
# ✅ 先单独测试每个 Agent
def test_researcher_alone():
    state = ArticleState(topic="Python asyncio")
    result = researcher_agent(state)
    assert result.research, "Researcher 应该输出研究结果"
    assert len(result.research) > 100, "研究结果不能太短"

def test_writer_alone():
    state = ArticleState(
        topic="Python asyncio",
        research="【核心概念】协程..."
    )
    result = writer_agent(state)
    assert result.draft, "Writer 应该输出文章草稿"

# 单个 Agent 测试通过后，再测整体流程
def test_full_pipeline():
    result = run_article_team("Python asyncio")
    assert result, "最终应该有文章输出"
```

---

### 7.3 多 Agent 系统的调试技巧

```python
# 技巧一：在每个节点打印状态快照
def debug_node(state, node_name):
    print(f"\n{'─'*40}")
    print(f"节点：{node_name}")
    print(f"当前状态：")
    for k, v in state.items():
        if isinstance(v, str) and len(v) > 50:
            print(f"  {k}: {v[:50]}...（共{len(v)}字）")
        else:
            print(f"  {k}: {v}")

# 技巧二：用 LangSmith 追踪整个执行图
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your_key"
# 运行后可在 LangSmith 网页上看到完整执行图

# 技巧三：记录每个 Agent 的输入输出到文件
import json
from pathlib import Path
from datetime import datetime

def log_agent_io(agent_name: str, input_data: dict, output_data: dict):
    log = {
        "agent": agent_name,
        "time": datetime.now().isoformat(),
        "input": input_data,
        "output": output_data
    }
    path = Path(f"logs/{agent_name}_{datetime.now():%Y%m%d_%H%M%S}.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2))
```

---

### 7.4 多 Agent 的成本控制

多 Agent 意味着更多 LLM 调用，成本会快速上升。

```python
# 策略一：分层用不同模型
# Supervisor 只做简单决策 → 用便宜的 Haiku
# Worker 做复杂工作 → 用 Sonnet 或 Opus

supervisor_llm = ChatAnthropic(model="claude-haiku-4-5")    # 调度决策，便宜
worker_llm     = ChatAnthropic(model="claude-sonnet-4-6")  # 实际工作，质量更好

# 策略二：限制每个 Agent 的 max_tokens
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,  # 根据 Agent 职责设置合理上限
    ...
)

# 策略三：并行调用（节省时间，但不节省成本）
import asyncio

async def run_workers_parallel(tasks: list[dict]) -> list[str]:
    """并行运行多个独立 Worker，节省时间"""
    async_client = anthropic.AsyncAnthropic()

    async def call_one(task):
        response = await async_client.messages.create(**task)
        return response.content[0].text

    results = await asyncio.gather(*[call_one(t) for t in tasks])
    return results
```

---

## 总结：多 Agent 的思维模型

```
单 Agent：
  一个全能员工，串行完成所有任务
  上限：context window + 单线程 + 难以专精

多 Agent：
  一个团队，每人专精一个领域，并行协作
  上限：协调成本 + 通信开销 + 设计复杂度

四种模式的记忆口诀：
  Supervisor  = 经理分配任务给专家
  Pipeline    = 流水线，上一步的产出是下一步的输入
  Peer-to-Peer = 辩论，互相审查提高质量
  Swarm       = 动态路由，Agent 自主移交

三个设计原则：
  1. 职责单一：每个 Agent 只做一件事
  2. 接口清晰：Agent 之间用结构化格式传递信息
  3. 有退出条件：循环必须有最大次数限制

什么时候不用多 Agent：
  任务简单 → 单次 LLM 调用
  工具调用 → 单 Agent（ReAct）
  步骤固定 → 硬编码 Pipeline，不用 Agent 也行
```

**下一步学习**：
- [LangGraph 官方文档 - Multi-agent](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)
- [CrewAI](https://github.com/crewAIInc/crewAI)：更高层的多 Agent 框架，角色驱动
- [AutoGen](https://github.com/microsoft/autogen)：微软的多 Agent 对话框架
