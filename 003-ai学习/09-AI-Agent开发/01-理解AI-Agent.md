# 理解 AI Agent

> **一句话先说清楚**：普通 LLM 是"问一次答一次"的问答机；Agent 是"拿到目标后自己规划、自己行动、自己检查、反复循环直到完成"的自主执行者。

---

## 第一部分：为什么需要 Agent（总）

### 普通 LLM 的天花板

想象你问 Claude 一个问题：

> 「帮我分析一下我们公司上个月的销售数据，找出下滑最严重的产品线，并给出改进建议。」

Claude 会说：**「请把数据发给我。」**

你把数据粘贴进去，Claude 分析，给出答案。

**这个流程有什么问题？**

1. 数据在数据库里，你得手动导出、手动粘贴
2. Claude 分析完，你还得手动把建议写进周报
3. 明天要再分析一次，整个过程重复一遍
4. 如果分析中途发现数据缺失，Claude 不能自己去查补

**一个普通 LLM 的本质局限：**

```
你 → [输入] → LLM → [输出] → 你
         单次调用，无状态，无行动能力
```

LLM 再聪明，也只是在"回答"，它不能"行动"。

---

### Agent 解决了什么

把刚才的例子交给 Agent：

> 「帮我分析一下我们公司上个月的销售数据，找出下滑最严重的产品线，并给出改进建议。」

Agent 会：

```
1. 思考：我需要先获取销售数据
2. 行动：调用 query_database("SELECT * FROM sales WHERE month='2024-12'")
3. 观察：返回了 3000 条数据
4. 思考：数据量大，我应该按产品线聚合
5. 行动：调用 execute_python("data.groupby('product_line')['revenue'].sum()")
6. 观察：发现"家电类"下滑 23%
7. 思考：需要找原因，查一下这段时间的客户反馈
8. 行动：调用 search_feedback("家电类 投诉 2024年12月")
9. 观察：主要反馈是价格偏高、竞争对手促销
10. 思考：信息够了，可以生成报告
11. 行动：调用 write_report(analysis_result)
12. 完成
```

你没有参与任何中间步骤。这就是 Agent。

**Agent 的本质是：给 LLM 装上手和眼睛。**

- **眼睛（感知）**：搜索引擎、数据库查询、文件读取
- **手（行动）**：执行代码、发邮件、写文件、调用 API
- **大脑（规划）**：LLM 负责思考"下一步做什么"

---

## 第二部分：Agent 的内部结构（分）

### 2.1 核心循环：思考 → 行动 → 观察

Agent 的运行本质是一个**循环**：

```
┌─────────────────────────────────────────┐
│                                         │
│   目标输入                              │
│      ↓                                  │
│   [思考 Thought]                        │
│   LLM 分析当前状态，决定下一步          │
│      ↓                                  │
│   [行动 Action]                         │
│   调用工具 or 直接输出答案              │
│      ↓                                  │
│   [观察 Observation]                    │
│   获取工具执行结果                      │
│      ↓                                  │
│   是否完成？                            │
│   ├── 否 → 回到[思考]                  │
│   └── 是 → 输出最终答案                │
│                                         │
└─────────────────────────────────────────┘
```

这个循环有个正式名字：**ReAct**（Reason + Act），来自 2022 年的同名论文。

---

### 2.2 五个核心组件

一个完整的 Agent 由以下五个部分构成：

```
┌──────────────────────────────────────────────────────────┐
│                        AI Agent                          │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  感知层  │  │  记忆层  │  │  工具层  │              │
│  │ Perception│  │  Memory  │  │  Tools   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │              │              │                     │
│       └──────────────┼──────────────┘                    │
│                       ↓                                  │
│               ┌───────────────┐                          │
│               │   规划层      │                          │
│               │   Planning    │  ← LLM 在这里思考        │
│               └───────┬───────┘                          │
│                       ↓                                  │
│               ┌───────────────┐                          │
│               │   执行层      │                          │
│               │   Action      │                          │
│               └───────────────┘                          │
└──────────────────────────────────────────────────────────┘
```

下面逐层拆解。

---

#### 感知层（Perception）：Agent 如何接收信息

Agent 的输入不止是用户文字，还可以是：

| 输入类型 | 示例 |
|----------|------|
| 文本 | 用户对话、文档内容 |
| 结构化数据 | 数据库查询结果、API 返回的 JSON |
| 工具执行结果 | 代码运行输出、搜索结果 |
| 图片 | 截图、图表（多模态 Agent） |
| 历史对话 | 多轮对话上下文 |

---

#### 记忆层（Memory）：Agent 如何记住信息

```
记忆类型
│
├── 短期记忆（In-Context Memory）
│   当前对话窗口内的所有内容
│   限制：受 context window 大小约束
│   类比：人的工作记忆，处理当前任务用
│
├── 长期记忆（External Memory）
│   向量数据库、关系型数据库
│   限制：需要检索（RAG），可能有噪声
│   类比：人的长期记忆，需要"回忆"
│
└── 程序记忆（Procedural Memory）
    System Prompt 中写死的规则和知识
    限制：静态，不能动态更新
    类比：人的本能和技能
```

**实际开发中的记忆策略：**

```python
# 短期记忆：对话历史
conversation_history = [
    {"role": "user", "content": "帮我分析销售数据"},
    {"role": "assistant", "content": "...tool_use..."},
    {"role": "user", "content": "...tool_result..."},
    # 每轮对话追加在这里
]

# 长期记忆：向量数据库检索
relevant_memories = vector_db.search(
    query=current_user_input,
    top_k=5
)
# 将检索结果注入 System Prompt
```

---

#### 工具层（Tools）：Agent 的能力边界

**工具是 Agent 能力的边界**。没有工具的 Agent 只是个会规划的 LLM。

工具本质上是**函数**，LLM 决定调用哪个函数、传什么参数。

```python
# 工具的定义形式（以 Claude API 为例）
tools = [
    {
        "name": "search_web",
        "description": "搜索互联网获取实时信息。当需要最新数据、新闻、或 LLM 训练数据截止后的信息时使用。",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，使用清晰简洁的短语"
                },
                "num_results": {
                    "type": "integer",
                    "description": "返回结果数量，默认 5",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
]
```

**工具描述的质量直接决定 Agent 的表现。** 写工具 description 的要点：

1. **说清楚"什么情况下用"**，而不只是"这个工具做什么"
2. **说清楚参数的含义和格式**，避免 LLM 猜
3. **说清楚返回值的格式**，让 LLM 知道如何解读结果

---

#### 规划层（Planning）：LLM 在这里思考

规划层是 LLM 本身，它负责：
- 理解当前目标
- 分析已有信息（对话历史 + 工具结果）
- 决定下一步行动（调用哪个工具，或者输出答案）

**不同规划策略的对比：**

| 策略 | 思路 | 适用场景 |
|------|------|----------|
| ReAct | 边想边做，逐步推进 | 大多数场景 |
| Plan-and-Execute | 先制定完整计划，再执行 | 复杂、长任务 |
| Reflexion | 执行后反思，修正错误 | 需要高准确率的任务 |
| Tree of Thoughts | 探索多条路径，选最优 | 搜索类、决策类问题 |

初学者先掌握 **ReAct**，它覆盖了 80% 的场景。

---

#### 执行层（Action）：行动的类型

Agent 的行动分为三类：

```
行动类型
│
├── 信息获取类
│   ├── 搜索引擎（search_web）
│   ├── 数据库查询（query_db）
│   ├── 文件读取（read_file）
│   └── API 调用（call_api）
│
├── 计算执行类
│   ├── 代码执行（execute_python）
│   ├── 数学计算（calculate）
│   └── 数据处理（transform_data）
│
└── 写入输出类
    ├── 发送邮件（send_email）
    ├── 写文件（write_file）
    ├── 数据库写入（insert_db）
    └── 调用第三方服务（create_ticket）
```

---

## 第三部分：从零手写一个 Agent（最重要的部分）

理解 Agent 最好的方法是**从零实现一个**，不借助任何框架。

### 3.1 最小 Agent：手动实现 ReAct 循环

```python
import anthropic
import json
import math

client = anthropic.Anthropic()

# ─── 步骤一：定义工具 ───────────────────────────────────────

tools = [
    {
        "name": "calculator",
        "description": "执行数学计算。支持加减乘除、平方根、幂运算等。当需要精确数学计算时使用，不要自己心算。",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Python 数学表达式，例如 '2 ** 10' 或 'math.sqrt(144)'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息。",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，例如 '北京'、'上海'"
                }
            },
            "required": ["city"]
        }
    }
]

# ─── 步骤二：实现工具的实际逻辑 ─────────────────────────────

def run_tool(tool_name: str, tool_input: dict) -> str:
    """执行工具，返回字符串结果"""

    if tool_name == "calculator":
        expression = tool_input["expression"]
        try:
            # 安全计算（生产环境需要更严格的沙箱）
            result = eval(expression, {"math": math, "__builtins__": {}})
            return f"计算结果：{expression} = {result}"
        except Exception as e:
            return f"计算出错：{str(e)}"

    elif tool_name == "get_weather":
        city = tool_input["city"]
        # 模拟天气 API（真实项目中调用真实 API）
        weather_data = {
            "北京": "晴天，15°C，东风 3 级",
            "上海": "多云，22°C，东南风 2 级",
            "广州": "小雨，28°C，南风 4 级",
        }
        return weather_data.get(city, f"暂无 {city} 的天气数据")

    else:
        return f"未知工具：{tool_name}"

# ─── 步骤三：实现 Agent 主循环 ───────────────────────────────

def run_agent(user_input: str, max_steps: int = 10) -> str:
    """
    Agent 主循环：
    1. 把用户输入 + 工具定义发给 LLM
    2. LLM 返回"调用工具"或"最终答案"
    3. 如果是"调用工具"，执行工具，把结果追加到对话，继续循环
    4. 如果是"最终答案"，返回给用户
    """

    messages = [{"role": "user", "content": user_input}]

    print(f"\n{'='*50}")
    print(f"用户：{user_input}")
    print(f"{'='*50}")

    for step in range(max_steps):
        print(f"\n[步骤 {step + 1}]")

        # 调用 LLM
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # ── 情况 A：LLM 决定调用工具 ──
        if response.stop_reason == "tool_use":

            # 把 LLM 的回复（包含工具调用意图）加入对话历史
            messages.append({"role": "assistant", "content": response.content})

            # 处理所有工具调用（LLM 可能一次调用多个工具）
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  → 调用工具：{block.name}")
                    print(f"  → 参数：{json.dumps(block.input, ensure_ascii=False)}")

                    # 执行工具
                    result = run_tool(block.name, block.input)
                    print(f"  ← 结果：{result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # 把工具结果加入对话历史，让 LLM 继续思考
            messages.append({"role": "user", "content": tool_results})

        # ── 情况 B：LLM 给出最终答案 ──
        elif response.stop_reason == "end_turn":
            final_answer = response.content[0].text
            print(f"\n最终答案：{final_answer}")
            return final_answer

        # ── 异常情况 ──
        else:
            print(f"未预期的 stop_reason：{response.stop_reason}")
            break

    return "Agent 达到最大步骤数，未能完成任务"


# ─── 运行示例 ────────────────────────────────────────────────

if __name__ == "__main__":
    # 示例 1：纯计算
    run_agent("2的10次方是多少？再加上144的平方根等于多少？")

    # 示例 2：天气查询
    run_agent("北京和上海今天哪个城市更热？")

    # 示例 3：混合任务
    run_agent("上海今天几度？这个温度换算成华氏度是多少？")
```

**运行后你会看到类似输出：**

```
==================================================
用户：上海今天几度？这个温度换算成华氏度是多少？
==================================================

[步骤 1]
  → 调用工具：get_weather
  → 参数：{"city": "上海"}
  ← 结果：多云，22°C，东南风 2 级

[步骤 2]
  → 调用工具：calculator
  → 参数：{"expression": "22 * 9/5 + 32"}
  ← 结果：计算结果：22 * 9/5 + 32 = 71.6

最终答案：上海今天 22°C，多云天气。换算成华氏度是 71.6°F。
```

**读懂这段代码，你就理解了 Agent 的本质**：
- LLM 不会真的"运行代码"，它只是**输出"我要调用 calculator，参数是这个"**
- 真正执行工具的是你写的 `run_tool` 函数
- 执行结果塞回对话历史，让 LLM 继续推理
- 这个循环一直进行，直到 LLM 认为可以给出最终答案

---

### 3.2 加入记忆：多轮对话 Agent

上面的 Agent 每次调用都是全新的，没有记忆。加入持久化记忆：

```python
from datetime import datetime

class AgentWithMemory:
    """带记忆的 Agent：能记住多轮对话"""

    def __init__(self, system_prompt: str):
        self.client = anthropic.Anthropic()
        self.system_prompt = system_prompt
        self.conversation_history = []   # 短期记忆：当前会话历史
        self.session_start = datetime.now()

    def chat(self, user_input: str) -> str:
        """处理一轮对话"""

        # 追加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # ── 上下文长度管理 ──
        # 防止历史太长超出 context window
        self._trim_history(max_turns=20)

        # 调用 LLM（带完整对话历史）
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=self.system_prompt,
            tools=tools,
            messages=self.conversation_history
        )

        # 处理工具调用（简化版，实际需要完整循环）
        if response.stop_reason == "tool_use":
            # ... 工具调用逻辑同上 ...
            pass

        # 追加 AI 回复到历史
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def _trim_history(self, max_turns: int):
        """保留最近 N 轮对话，防止超出 context window"""
        # 每轮 = 1 个 user + 1 个 assistant = 2 条消息
        max_messages = max_turns * 2
        if len(self.conversation_history) > max_messages:
            # 保留最新的消息（从后往前截取）
            self.conversation_history = self.conversation_history[-max_messages:]

    def clear_history(self):
        """开始新会话"""
        self.conversation_history = []


# 使用示例
agent = AgentWithMemory(
    system_prompt="你是一个智能助手，能帮用户查天气和做数学计算。记住用户的偏好和之前问过的问题。"
)

# 第一轮
agent.chat("北京今天天气怎么样？")

# 第二轮（Agent 记得上一轮问的是北京天气）
agent.chat("换算成华氏度是多少？")  # Agent 知道"这个温度"指的是北京的温度

# 第三轮
agent.chat("和上海比哪个更热？")
```

---

### 3.3 工具调用的完整生命周期

这张图是理解 Agent 最关键的图，请仔细看：

```
用户："帮我查一下北京天气"
           │
           ▼
┌─────────────────────┐
│    构造请求          │
│  messages = [...]   │
│  tools = [...]      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Claude API        │
│                     │
│  LLM 读取 tools 定义│
│  决定调用哪个工具   │
└──────────┬──────────┘
           │
           ▼
     stop_reason == "tool_use"
           │
           ▼
┌─────────────────────────────────────────┐
│  response.content = [                   │
│    TextBlock(text="好的，让我查一下"),  │ ← LLM 的思考文字（可选）
│    ToolUseBlock(                        │
│      id="toolu_01abc",                  │ ← 工具调用 ID（关联结果用）
│      name="get_weather",               │ ← 工具名
│      input={"city": "北京"}            │ ← LLM 填的参数
│    )                                    │
│  ]                                      │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│  你的代码执行工具    │
│  result = "晴，15°C" │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  把工具结果追加到对话：                 │
│  messages.append({                      │
│    "role": "user",                      │
│    "content": [{                        │
│      "type": "tool_result",             │
│      "tool_use_id": "toolu_01abc",      │ ← 必须对应上面的 ID
│      "content": "晴，15°C"              │
│    }]                                   │
│  })                                     │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│   再次调用 Claude   │
│   LLM 看到工具结果  │
│   生成最终回答      │
└──────────┬──────────┘
           │
           ▼
     stop_reason == "end_turn"
           │
           ▼
    "北京今天晴天，15°C"
```

**关键认知**：工具并不是 LLM 自己执行的，LLM 只是"说出"要调用什么、参数是什么，然后**你的代码**去真正执行，再把结果喂回给 LLM。

---

## 第四部分：用框架实现 Agent（LangGraph）

手写 Agent 之后，我们用框架。框架的价值不是"更容易"，而是**解决了手写 Agent 的痛点**：

| 手写 Agent 的痛点 | LangGraph 的解决方案 |
|-------------------|---------------------|
| 循环逻辑混乱，难以调试 | 显式定义图结构，可视化工作流 |
| 无法处理并行工具调用 | 原生支持并行节点 |
| 状态管理手动维护 | 内置状态管理 |
| 流式输出难以实现 | 原生支持 streaming |
| 复杂分支逻辑难以维护 | 条件边（conditional edges）清晰表达 |

### LangGraph 的核心概念

```
LangGraph = 把 Agent 工作流建模为有向图

节点（Node）：一个处理步骤（调用 LLM、执行工具、做判断）
边（Edge）：节点之间的连接（顺序流转）
条件边（Conditional Edge）：根据状态决定走哪条路
状态（State）：贯穿整个图的共享数据
```

### 用 LangGraph 实现一个完整 Agent

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import operator

# ─── 步骤一：定义状态（State）───────────────────────────────
# State 是贯穿整个 Agent 生命周期的数据容器

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]  # 对话历史（自动追加）
    # 可以加更多字段：
    # user_id: str
    # task_complete: bool

# ─── 步骤二：定义工具 ───────────────────────────────────────

from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """搜索互联网获取实时信息。query 参数是搜索关键词。"""
    # 真实项目用 Tavily、Serper 等搜索 API
    return f"搜索 '{query}' 的结果：[模拟结果] 相关信息..."

@tool
def calculate(expression: str) -> str:
    """执行数学计算。expression 是 Python 数学表达式。"""
    import math
    try:
        result = eval(expression, {"math": math, "__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"

tools = [search_web, calculate]

# ─── 步骤三：定义节点 ───────────────────────────────────────

llm = ChatAnthropic(model="claude-sonnet-4-6").bind_tools(tools)

def agent_node(state: AgentState) -> dict:
    """
    Agent 节点：调用 LLM 做决策
    输入：当前状态（包含对话历史）
    输出：LLM 的回复（追加到 messages）
    """
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)  # LangGraph 内置：自动执行工具

# ─── 步骤四：定义路由逻辑 ───────────────────────────────────

def should_continue(state: AgentState) -> str:
    """
    条件边：决定下一步走哪里
    - 如果 LLM 要调用工具 → 去 tool_node
    - 如果 LLM 要输出答案 → 结束
    """
    last_message = state["messages"][-1]

    # 检查最后一条消息是否包含工具调用
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "call_tools"   # 去工具节点
    else:
        return "end"          # 结束

# ─── 步骤五：构建图 ─────────────────────────────────────────

graph_builder = StateGraph(AgentState)

# 添加节点
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tool_node)

# 设置入口
graph_builder.set_entry_point("agent")

# 添加条件边：agent 节点执行后，根据 should_continue 决定下一步
graph_builder.add_conditional_edges(
    "agent",           # 从哪个节点出发
    should_continue,   # 路由函数
    {
        "call_tools": "tools",   # 返回 "call_tools" → 去 tools 节点
        "end": END               # 返回 "end" → 结束
    }
)

# 添加普通边：tools 执行完后回到 agent
graph_builder.add_edge("tools", "agent")

# 编译图
agent = graph_builder.compile()

# ─── 步骤六：运行 ───────────────────────────────────────────

def run(user_input: str):
    result = agent.invoke({
        "messages": [HumanMessage(content=user_input)]
    })
    return result["messages"][-1].content

print(run("帮我搜索一下 Python 3.13 的新特性，并计算一下 2 的 32 次方"))
```

### 图的结构（可视化）

```
          ┌──────────┐
   START  │          │
  ──────► │  agent   │
          │  (LLM)   │
          └────┬─────┘
               │
    should_continue()
               │
    ┌──────────┴──────────┐
    │                     │
  "call_tools"          "end"
    │                     │
    ▼                     ▼
┌──────────┐            END
│  tools   │
│ (执行工具)│
└────┬─────┘
     │
     └─────────────────► agent（循环）
```

---

## 第五部分：架构规律与最佳实践（总）

经过前面的学习，现在回到高处看 Agent 的设计规律。

### 5.1 选择工具调用还是 Agent？

**不是所有任务都需要 Agent。** 错误使用 Agent 会带来：延迟高、成本高、调试难。

```
判断流程：

这个任务需要多步骤吗？
├── 否 → 直接调用 LLM，不需要 Agent
└── 是 → 步骤是确定的吗？
          ├── 是 → 用固定流水线（Chain），不需要 Agent
          └── 否 → 步骤需要 LLM 动态决定吗？
                    ├── 否 → 规则代码处理
                    └── 是 → ✅ 使用 Agent
```

**例子：**

| 任务 | 方案 |
|------|------|
| 翻译一段文字 | 直接调用 LLM |
| 翻译 → 润色 → 格式化 | Chain（固定三步） |
| 研究一个主题，步骤未知 | Agent |
| 根据用户需求从不同来源收集信息 | Agent |

### 5.2 Agent 的常见失败模式

**失败一：工具描述模糊**

```python
# ❌ 模糊的描述，LLM 不知道什么时候用
{
    "name": "search",
    "description": "搜索信息"
}

# ✅ 清晰的描述，说明使用场景和参数格式
{
    "name": "search_web",
    "description": "在互联网上搜索实时信息。当需要：1) 最新新闻 2) LLM 训练截止后的数据 3) 实时价格/天气时使用。不适合搜索私有文档。",
    "input_schema": {
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词，使用 3-5 个核心词，不要写完整句子"
            }
        }
    }
}
```

**失败二：没有设置最大步骤数**

```python
# ❌ 危险：Agent 可能无限循环
while True:
    response = llm.invoke(messages)
    ...

# ✅ 安全：设置最大步骤
for step in range(max_steps := 15):
    response = llm.invoke(messages)
    if response.stop_reason == "end_turn":
        break
else:
    log.warning(f"Agent 达到最大步骤数 {max_steps}，强制终止")
```

**失败三：工具错误没有优雅处理**

```python
# ❌ 工具抛异常，整个 Agent 崩溃
def search_web(query: str) -> str:
    return requests.get(f"https://api.search.com?q={query}").json()["results"]

# ✅ 捕获异常，返回描述性错误信息给 LLM
def search_web(query: str) -> str:
    try:
        response = requests.get(f"https://api.search.com?q={query}", timeout=10)
        response.raise_for_status()
        return response.json()["results"]
    except requests.Timeout:
        return "搜索超时，请尝试更简短的关键词或稍后重试"
    except Exception as e:
        return f"搜索失败：{str(e)}。可以尝试其他方式获取信息。"
```

**失败四：上下文窗口爆满**

```python
# 长任务中工具返回了大量数据，直接塞进对话会超出 context window

# ❌ 直接返回完整数据
def query_database(sql: str) -> str:
    results = db.execute(sql).fetchall()
    return str(results)  # 可能是几千行

# ✅ 返回摘要 + 关键数据
def query_database(sql: str) -> str:
    results = db.execute(sql).fetchall()
    total = len(results)
    if total > 20:
        return f"查询返回 {total} 条记录。前 5 条：\n{results[:5]}\n建议使用更具体的条件缩小结果范围。"
    return str(results)
```

### 5.3 Agent 的调试技巧

```python
# 技巧一：打印每一步的思考过程
def agent_with_logging(user_input: str):
    for step, (thought, action, observation) in enumerate(agent.stream(user_input)):
        print(f"\n── 步骤 {step + 1} ──")
        print(f"思考：{thought}")
        print(f"行动：{action}")
        print(f"观察：{observation}")

# 技巧二：使用 LangSmith 追踪（强烈推荐）
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your_key"
# 之后所有 LangChain/LangGraph 调用都会自动上传到 LangSmith

# 技巧三：单独测试每个工具
def test_tools():
    print(search_web("Python 3.13"))
    print(calculate("2 ** 32"))
    # 确保工具本身正常，再集成到 Agent 中测试
```

### 5.4 Agent 设计的黄金原则

```
原则一：最小工具集
  给 Agent 10 个工具，不如给 3 个精准的工具。
  工具太多 → LLM 选择困难 → 行为不稳定。

原则二：工具幂等性
  同一个工具，调用一次和调用十次结果相同。
  查询操作天然幂等，写操作要加保护。

原则三：人工确认高风险操作
  发邮件、删数据、转账 → 执行前请求用户确认。
  这叫 Human-in-the-loop（人在循环中）。

原则四：失败是正常状态
  工具会失败，LLM 会误判。
  Agent 要能从失败中恢复，而不是直接崩溃。

原则五：可观测性优先
  生产环境每一次 LLM 调用都要记录：
  输入、输出、耗时、Token 数、工具调用链。
  没有日志，问题无法复现，无法优化。
```

---

## 总结：Agent 的思维模型

```
普通 LLM：
用户 ──[问题]──► LLM ──[回答]──► 用户
            单次、被动、无状态

Agent：
用户 ──[目标]──► Agent ─────────────────────────────┐
                   │                                 │
                   ▼                                 │
              [思考] LLM 规划                        │
                   │                                 │
                   ▼                                 │
              [行动] 调用工具                        │
                   │                                 │
                   ▼                                 │
              [观察] 获取结果                        │
                   │                                 │
             目标完成了吗？                          │
             ├── 否 ─────────────────────────────────┘
             └── 是 ──► 用户
             循环、主动、有状态

Agent = LLM 的大脑 + 工具的双手 + 记忆的存储 + 循环的驱动
```

**你已经理解了 Agent 的核心。** 接下来的进阶方向：

| 进阶主题 | 学习重点 |
|----------|----------|
| 多 Agent 协作 | CrewAI、LangGraph 多 Agent |
| Agent 评估 | 如何量化 Agent 的准确率和效率 |
| Long-horizon Agent | 处理需要几十步的复杂任务 |
| Agent 安全 | 防止提示注入、防止权限滥用 |
| 生产部署 | 异步执行、任务队列、状态持久化 |
