# 05 Agent 测试

## 学习目标

学完这一节，你需要知道：

- Agent 测试为什么比单次 LLM 调用更难。
- 如何测试工具调用的正确性。
- 如何测试多步骤任务的完成质量。
- 如何测试 Agent 的计划能力。
- 如何测试状态管理。
- 如何测试失败恢复能力。

---

## Agent 测试的特殊性

Agent 和普通 LLM 调用最大的区别是：**Agent 会循环执行多个步骤，每一步都可能出错，而且步骤之间相互依赖**。

```text
普通 LLM 调用：
  输入 → LLM → 输出
  一步，出错就是这一步的问题

Agent 执行过程：
  输入
    ↓
  步骤1：思考要做什么
    ↓
  步骤2：调用工具A，获取数据
    ↓
  步骤3：基于数据继续思考
    ↓
  步骤4：调用工具B，处理数据
    ↓
  步骤5：生成最终答案

  任意步骤出错，最终结果就可能出错
  而且步骤2的错误会影响步骤3、4、5
```

Agent 测试的难点：

- **不确定性更高**：同一个问题，每次 Agent 选择的路径可能不同。
- **工具调用顺序复杂**：有些任务要求按特定顺序调用工具。
- **中间状态难以观察**：要记录每一步的思考和行动，才能分析出错原因。
- **测试成本高**：每个测试用例都需要多次 LLM 调用，花费更多时间和 Token。

---

## 工具调用测试

### 测试工具是否被正确调用

工具调用测试检查三个方面：

1. 在该调用工具的时候，Agent 调用了吗？
2. 调用了正确的工具吗？
3. 传递的参数正确吗？

```python
import anthropic
import json
from dataclasses import dataclass, field


client = anthropic.Anthropic()


@dataclass
class ToolCall:
    """记录一次工具调用"""
    name: str
    inputs: dict
    output: str = ""


@dataclass
class AgentTrace:
    """记录 Agent 的完整执行轨迹"""
    question: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    final_answer: str = ""
    steps: int = 0


# 定义工具（测试用）
TOOLS = [
    {
        "name": "search_database",
        "description": "查询数据库，获取产品信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "查询关键词"},
                "table": {"type": "string", "description": "要查询的表名"}
            },
            "required": ["query", "table"]
        }
    },
    {
        "name": "calculate_price",
        "description": "根据数量和单价计算总价，支持折扣",
        "input_schema": {
            "type": "object",
            "properties": {
                "unit_price": {"type": "number"},
                "quantity": {"type": "integer"},
                "discount": {"type": "number", "description": "折扣率，0到1之间，默认1"}
            },
            "required": ["unit_price", "quantity"]
        }
    },
    {
        "name": "send_notification",
        "description": "发送通知消息",
        "input_schema": {
            "type": "object",
            "properties": {
                "recipient": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["recipient", "message"]
        }
    }
]


def mock_tool_executor(name: str, inputs: dict) -> str:
    """模拟工具执行（测试时不调用真实服务）"""
    if name == "search_database":
        if "产品A" in inputs.get("query", ""):
            return json.dumps({"product": "产品A", "unit_price": 100, "stock": 50})
        return json.dumps({"error": "未找到相关产品"})

    elif name == "calculate_price":
        price = inputs["unit_price"] * inputs["quantity"]
        discount = inputs.get("discount", 1)
        return str(price * discount)

    elif name == "send_notification":
        return f"通知已发送给 {inputs['recipient']}"

    return "未知工具"


def run_agent_with_trace(question: str, system_prompt: str) -> AgentTrace:
    """运行 Agent 并记录完整执行轨迹"""
    trace = AgentTrace(question=question)
    messages = [{"role": "user", "content": question}]

    for step in range(15):  # 最大步数保护
        trace.steps += 1

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    output = mock_tool_executor(block.name, block.input)

                    call = ToolCall(name=block.name, inputs=block.input, output=output)
                    trace.tool_calls.append(call)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output
                    })

            messages.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "end_turn":
            trace.final_answer = response.content[0].text
            break

    return trace


def check_tool_calls(trace: AgentTrace, expectations: dict) -> tuple[bool, list[str]]:
    """
    检查工具调用是否符合预期。

    expectations 格式：
    {
        "required_tools": ["search_database", "calculate_price"],  # 必须调用的工具
        "forbidden_tools": ["send_notification"],                   # 不能调用的工具
        "tool_params": {                                            # 工具参数检查
            "search_database": {"table": "products"}               # 必须含有这些参数
        },
        "tool_order": ["search_database", "calculate_price"]       # 工具调用顺序（可选）
    }
    """
    failures = []
    called_tools = [c.name for c in trace.tool_calls]

    # 检查必须调用的工具
    for tool in expectations.get("required_tools", []):
        if tool not in called_tools:
            failures.append(f"未调用必须的工具：{tool}")

    # 检查不能调用的工具
    for tool in expectations.get("forbidden_tools", []):
        if tool in called_tools:
            failures.append(f"调用了不应该调用的工具：{tool}")

    # 检查工具参数
    for tool_name, required_params in expectations.get("tool_params", {}).items():
        for call in trace.tool_calls:
            if call.name == tool_name:
                for param, expected_val in required_params.items():
                    actual_val = call.inputs.get(param)
                    if actual_val != expected_val:
                        failures.append(
                            f"工具 {tool_name} 的参数 {param} 错误："
                            f"期望 '{expected_val}'，实际 '{actual_val}'"
                        )

    # 检查调用顺序
    expected_order = expectations.get("tool_order", [])
    if expected_order:
        actual_order = [c.name for c in trace.tool_calls
                        if c.name in expected_order]
        if actual_order != expected_order:
            failures.append(
                f"工具调用顺序错误：期望 {expected_order}，实际 {actual_order}"
            )

    return len(failures) == 0, failures
```

### 工具调用测试用例示例

```python
SYSTEM_PROMPT = "你是一个销售助手，帮助用户查询产品和计算价格。"

TOOL_TEST_CASES = [
    {
        "id": "tool_001",
        "description": "查询并计算价格",
        "question": "产品A买10个要多少钱？",
        "expectations": {
            "required_tools": ["search_database", "calculate_price"],
            "forbidden_tools": ["send_notification"],
            "tool_order": ["search_database", "calculate_price"]
        }
    },
    {
        "id": "tool_002",
        "description": "不该调用工具的情况",
        "question": "你好，你是谁？",
        "expectations": {
            "required_tools": [],          # 不需要调用任何工具
            "forbidden_tools": ["search_database", "calculate_price"]
        }
    }
]


def run_tool_tests():
    for case in TOOL_TEST_CASES:
        trace = run_agent_with_trace(case["question"], SYSTEM_PROMPT)
        ok, failures = check_tool_calls(trace, case["expectations"])

        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{status} [{case['id']}] {case['description']}")
        print(f"   步骤数：{trace.steps}，工具调用：{[c.name for c in trace.tool_calls]}")
        if not ok:
            for f in failures:
                print(f"   原因：{f}")
```

---

## 多步骤任务测试

多步骤任务测试检查 Agent 能否完成需要多个动作才能完成的目标。

### 定义任务完成标准

```python
@dataclass
class TaskTestCase:
    id: str
    description: str
    question: str
    # 任务完成的判断条件
    success_criteria: dict


MULTI_STEP_CASES = [
    TaskTestCase(
        id="task_001",
        description="查询产品、计算折扣价、发送通知的完整流程",
        question="查一下产品A的价格，以8折给客户小王报价，并通知他",
        success_criteria={
            "required_tools": ["search_database", "calculate_price", "send_notification"],
            "answer_must_contain": ["产品A", "小王"],
            "max_steps": 6  # 不应该超过 6 步才完成
        }
    )
]


def check_task_completion(
    trace: AgentTrace,
    criteria: dict
) -> tuple[bool, list[str]]:
    failures = []

    # 检查工具调用
    called = [c.name for c in trace.tool_calls]
    for tool in criteria.get("required_tools", []):
        if tool not in called:
            failures.append(f"未完成步骤：{tool}")

    # 检查最终答案
    answer = trace.final_answer
    for keyword in criteria.get("answer_must_contain", []):
        if keyword not in answer:
            failures.append(f"最终答案缺少关键词：'{keyword}'")

    # 检查步骤数（效率）
    max_steps = criteria.get("max_steps")
    if max_steps and trace.steps > max_steps:
        failures.append(f"步骤过多：实际 {trace.steps} 步，上限 {max_steps} 步")

    return len(failures) == 0, failures
```

---

## 计划能力测试

计划能力测试检查 Agent 在面对复杂任务时，能否制定合理的执行计划。

### 测试分解能力

```python
def test_task_decomposition():
    """测试 Agent 能否把复杂任务分解成合理的子步骤"""

    system_prompt = """你是一个项目助手。收到复杂任务时，先列出执行计划，再逐步执行。"""

    test_cases = [
        {
            "question": "帮我分析本季度销售数据，找出前三名产品，并生成一份摘要报告",
            "expected_plan_keywords": ["查询", "分析", "排序", "报告"],
            "description": "复杂分析任务应该有多步计划"
        },
        {
            "question": "今天几号？",
            "expected_plan_keywords": [],           # 简单问题不应该有复杂计划
            "max_steps": 2,
            "description": "简单问题不应该过度规划"
        }
    ]

    for case in test_cases:
        trace = run_agent_with_trace(case["question"], system_prompt)

        # 检查计划关键词（粗略检查是否有计划思路）
        answer_text = trace.final_answer
        plan_words_found = [w for w in case.get("expected_plan_keywords", [])
                           if w in answer_text]

        print(f"\n{case['description']}")
        print(f"  问题：{case['question']}")
        print(f"  步骤数：{trace.steps}")
        print(f"  工具调用：{[c.name for c in trace.tool_calls]}")

        if case.get("expected_plan_keywords"):
            coverage = len(plan_words_found) / len(case["expected_plan_keywords"])
            print(f"  计划覆盖率：{coverage:.0%}")

        if case.get("max_steps") and trace.steps > case["max_steps"]:
            print(f"  ⚠️  步骤过多：{trace.steps} 步（上限 {case['max_steps']}）")
```

---

## 状态管理测试

多轮对话中，Agent 需要记住之前的上下文。状态管理测试检查 Agent 能否正确维护对话状态。

```python
def test_state_management():
    """测试 Agent 在多轮对话中是否能维护正确的状态"""

    system_prompt = "你是一个购物助手，记住用户的购物偏好和已查询的产品信息。"

    # 多轮对话场景
    conversation = [
        {
            "input": "我想买产品A，帮我查一下价格",
            "check": lambda trace: "search_database" in [c.name for c in trace.tool_calls],
            "check_desc": "第一轮应该查询产品A"
        },
        {
            "input": "如果买20个，总价是多少？",    # 没有再提"产品A"，需要记住上下文
            "check": lambda trace: "calculate_price" in [c.name for c in trace.tool_calls],
            "check_desc": "第二轮应该知道还是在讨论产品A，并计算价格"
        },
        {
            "input": "好的，帮我通知销售经理李总",
            "check": lambda trace: "send_notification" in [c.name for c in trace.tool_calls],
            "check_desc": "第三轮应该发送通知"
        }
    ]

    messages = []

    for i, turn in enumerate(conversation):
        messages.append({"role": "user", "content": turn["input"]})

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=512,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )

        # 简化处理（实际需要完整的工具调用循环）
        passed = True  # 根据实际 trace 检查

        status = "✅" if passed else "❌"
        print(f"第{i+1}轮 {status} {turn['check_desc']}")
        print(f"  用户输入：{turn['input']}")
```

---

## 失败恢复测试

失败恢复测试检查当工具调用失败时，Agent 能否合理处理并继续完成任务。

```python
def mock_failing_tool(name: str, inputs: dict, fail_rate: float = 0.5) -> str:
    """
    模拟偶发性失败的工具。
    fail_rate：失败概率（0-1）
    """
    import random
    if random.random() < fail_rate:
        return json.dumps({"error": "服务暂时不可用，请稍后重试"})
    return mock_tool_executor(name, inputs)


FAILURE_TEST_CASES = [
    {
        "id": "fail_001",
        "description": "工具返回错误时，Agent 应该重试或使用备选方案",
        "question": "查询产品A的库存",
        "tool_responses": {
            # 第一次调用返回错误，第二次正常
            "search_database": [
                '{"error": "数据库连接超时"}',
                '{"product": "产品A", "stock": 50}'
            ]
        },
        "success_criteria": {
            "answer_must_contain": ["产品A"],           # 最终要给出答案
            "answer_must_not_contain": ["失败", "错误"] # 不能直接把错误甩给用户
        }
    },
    {
        "id": "fail_002",
        "description": "工具持续失败时，Agent 应该告知用户而不是死循环",
        "question": "发送紧急通知给所有人",
        "tool_responses": {
            "send_notification": ['{"error": "服务不可用"}'] * 10   # 始终失败
        },
        "success_criteria": {
            "max_steps": 8,   # 不应该无限重试
            "answer_must_contain": ["无法", "失败", "稍后"]  # 应该告知用户
        }
    }
]


def run_failure_recovery_test():
    """运行失败恢复测试"""
    for case in FAILURE_TEST_CASES:
        print(f"\n测试：{case['description']}")
        # 使用模拟失败的工具执行器
        # 实际测试中，替换 mock_tool_executor 为 mock_failing_tool
        trace = run_agent_with_trace(case["question"], "你是一个助手。")

        criteria = case["success_criteria"]
        failures = []

        if criteria.get("max_steps") and trace.steps > criteria["max_steps"]:
            failures.append(f"步骤过多：{trace.steps}（上限 {criteria['max_steps']}）")

        for kw in criteria.get("answer_must_contain", []):
            if kw not in trace.final_answer:
                failures.append(f"答案中缺少预期内容：'{kw}'")

        for kw in criteria.get("answer_must_not_contain", []):
            if kw in trace.final_answer:
                failures.append(f"答案中出现了不应有的内容：'{kw}'")

        status = "✅ PASS" if not failures else "❌ FAIL"
        print(f"  {status} 步骤数：{trace.steps}")
        for f in failures:
            print(f"  原因：{f}")
```

---

## Agent 测试的执行轨迹记录

对 Agent 做测试，**记录完整执行轨迹是关键**。没有轨迹，发现问题时无法分析原因。

```python
def save_agent_trace(trace: AgentTrace, test_id: str):
    """保存 Agent 执行轨迹，便于后续分析"""
    import json
    from pathlib import Path
    from datetime import datetime

    record = {
        "test_id": test_id,
        "run_at": datetime.now().isoformat(),
        "question": trace.question,
        "steps": trace.steps,
        "tool_calls": [
            {
                "name": c.name,
                "inputs": c.inputs,
                "output": c.output
            }
            for c in trace.tool_calls
        ],
        "final_answer": trace.final_answer
    }

    path = Path(f"traces/{test_id}_{datetime.now():%Y%m%d_%H%M%S}.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2))
```

---

## 本节重点

- Agent 测试比单次 LLM 测试复杂，因为有多个步骤，任意步骤出错都影响结果。
- 工具调用测试检查三点：是否调用了、调用了哪个、参数是否正确。
- 多步骤测试要检查任务完成率和步骤效率（步骤数不能过多）。
- 状态管理测试验证 Agent 在多轮对话中能否记住上下文。
- 失败恢复测试验证工具出错时 Agent 的处理是否合理。
- 记录完整执行轨迹是 Agent 测试的基础，没有轨迹无法分析问题。

## 自测问题

1. Agent 测试为什么比普通 LLM 调用测试更复杂？
2. 工具调用测试检查哪三个方面？
3. 多步骤任务测试中，为什么要限制最大步骤数？
4. 状态管理测试的典型场景是什么？
5. 失败恢复测试中，"工具持续失败"的预期行为应该是什么？
