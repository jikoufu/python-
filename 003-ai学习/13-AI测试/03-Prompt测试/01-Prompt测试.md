# 03 Prompt 测试

## 学习目标

学完这一节，你需要知道：

- 为什么 Prompt 需要专门测试。
- 如何对 Prompt 做版本管理。
- 如何设计 Prompt 回归测试。
- 如何测试指令遵循能力。
- 如何测试边界输入。
- 如何做 Prompt A/B 测试。

---

## 为什么 Prompt 需要专门测试

Prompt 是 AI 应用的核心配置。修改一句话，输出可能完全不同。

常见问题：

- Prompt 改了一个词，某些用户的问题开始回答变差了。
- 新增了一个规则，但和原有规则冲突，模型行为变得混乱。
- 换了一个模型版本，原来的 Prompt 效果下降了。

这些问题如果没有测试，只靠人工用几个例子试，很难发现。

Prompt 测试的目的是：**每次修改 Prompt 后，快速验证整体质量没有下降**。

---

## Prompt 版本管理

### 为什么要管理版本

Prompt 会频繁修改。如果没有版本管理：

- 不知道当前用的是哪个版本。
- 改了之后效果变差，也不知道改了什么。
- 多人协作时，Prompt 被覆盖了不知道。

### 基础版本管理方案

最简单的方案是把 Prompt 存入文件，用 Git 管理。

目录结构示例：

```text
prompts/
├── chat_assistant/
│   ├── v1.0.txt
│   ├── v1.1.txt
│   └── current.txt   ← 当前生产版本（软链接或直接复制）
├── email_rewriter/
│   ├── v1.0.txt
│   └── v2.0.txt
```

每个版本的文件建议记录：

```text
# 版本：v1.1
# 修改日期：2024-03-15
# 修改人：张三
# 修改原因：增加对用户问题中含代码时的处理规则
# 基于版本：v1.0

你是一个专业的技术助手...
（以下是 Prompt 正文）
```

### 代码中加载 Prompt

```python
# prompt_manager.py

from pathlib import Path


def load_prompt(name: str, version: str = "current") -> str:
    """
    加载指定名称和版本的 Prompt。
    name: Prompt 的名称，对应 prompts/ 下的目录名
    version: 版本号，例如 "v1.1"，不传则加载 current
    """
    base_dir = Path("prompts") / name
    file_path = base_dir / f"{version}.txt"

    if not file_path.exists():
        raise FileNotFoundError(f"Prompt 文件不存在：{file_path}")

    return file_path.read_text(encoding="utf-8")


# 使用示例
system_prompt = load_prompt("chat_assistant", version="v1.1")
```

### 更完整的数据库方案

项目规模大时，可以把 Prompt 存入数据库：

```python
# 数据库表结构示例（SQLAlchemy）
class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)       # Prompt 名称
    version = Column(String(20), nullable=False)     # 版本号
    content = Column(Text, nullable=False)           # Prompt 内容
    is_active = Column(Boolean, default=False)       # 是否为当前生产版本
    created_at = Column(DateTime, default=func.now())
    created_by = Column(String(50))
    change_note = Column(Text)                       # 本次修改说明

def get_active_prompt(name: str) -> str:
    """获取当前生产版本的 Prompt"""
    record = session.query(PromptVersion).filter_by(
        name=name, is_active=True
    ).first()
    if not record:
        raise ValueError(f"未找到激活的 Prompt：{name}")
    return record.content
```

---

## Prompt 回归测试

回归测试的目的：**Prompt 每次修改后，自动验证历史测试用例的通过率没有下降**。

### 准备测试样本集

测试样本集是回归测试的基础。每个样本包含输入和期望结果的判断条件。

```json
[
  {
    "id": "case_001",
    "description": "用户询问产品价格",
    "user_input": "你们的旗舰产品多少钱？",
    "expected": {
      "must_contain": ["价格", "联系"],
      "must_not_contain": ["不知道", "无法回答"],
      "max_length": 200
    }
  },
  {
    "id": "case_002",
    "description": "用户输入与业务无关的问题",
    "user_input": "帮我写一首诗",
    "expected": {
      "must_contain": ["很抱歉", "专注于"],
      "must_not_contain": [],
      "max_length": 150
    }
  },
  {
    "id": "case_003",
    "description": "用户要求输出 JSON 格式",
    "user_input": "把用户信息整理成 JSON：姓名张三，年龄25",
    "expected": {
      "is_valid_json": true,
      "json_keys": ["name", "age"]
    }
  }
]
```

### 回归测试脚本

```python
import json
import anthropic
from pathlib import Path
from datetime import datetime


client = anthropic.Anthropic()


def run_model(system_prompt: str, user_input: str) -> str:
    """调用模型，返回输出文本"""
    response = client.messages.create(
        model="claude-haiku-4-5",    # 回归测试用便宜的模型
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}]
    )
    return response.content[0].text


def check_case(output: str, expected: dict) -> tuple[bool, list[str]]:
    """
    检查单条输出是否满足期望。
    返回：(是否通过, 失败原因列表)
    """
    failures = []

    # 检查必须包含的关键词
    for keyword in expected.get("must_contain", []):
        if keyword not in output:
            failures.append(f"缺少关键词：'{keyword}'")

    # 检查不能包含的内容
    for keyword in expected.get("must_not_contain", []):
        if keyword in output:
            failures.append(f"出现了不应该有的内容：'{keyword}'")

    # 检查长度
    max_length = expected.get("max_length")
    if max_length and len(output) > max_length:
        failures.append(f"输出过长：{len(output)} 字符，上限 {max_length}")

    # 检查是否为合法 JSON
    if expected.get("is_valid_json"):
        try:
            parsed = json.loads(output)
            # 检查 JSON 必须包含的 key
            for key in expected.get("json_keys", []):
                if key not in parsed:
                    failures.append(f"JSON 缺少字段：'{key}'")
        except json.JSONDecodeError:
            failures.append("输出不是合法 JSON")

    return len(failures) == 0, failures


def run_regression(prompt_name: str, prompt_version: str, test_file: str):
    """运行回归测试"""

    # 加载 Prompt 和测试样本
    system_prompt = load_prompt(prompt_name, prompt_version)
    cases = json.loads(Path(test_file).read_text(encoding="utf-8"))

    results = []
    passed = 0

    print(f"\n开始回归测试：{prompt_name} @ {prompt_version}")
    print(f"共 {len(cases)} 个测试用例\n")

    for case in cases:
        output = run_model(system_prompt, case["user_input"])
        ok, failures = check_case(output, case["expected"])

        results.append({
            "id": case["id"],
            "description": case["description"],
            "passed": ok,
            "failures": failures,
            "output": output
        })

        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{status}  [{case['id']}] {case['description']}")
        if not ok:
            for f in failures:
                print(f"         原因：{f}")
        else:
            passed += 1

    # 输出汇总
    total = len(cases)
    pass_rate = passed / total * 100
    print(f"\n{'='*40}")
    print(f"通过率：{passed}/{total}（{pass_rate:.1f}%）")

    # 保存报告
    report = {
        "prompt_name": prompt_name,
        "prompt_version": prompt_version,
        "run_at": datetime.now().isoformat(),
        "pass_rate": pass_rate,
        "results": results
    }
    report_path = f"reports/{prompt_name}_{prompt_version}_{datetime.now():%Y%m%d_%H%M}.json"
    Path("reports").mkdir(exist_ok=True)
    Path(report_path).write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"报告已保存：{report_path}")

    return pass_rate


# 使用
run_regression(
    prompt_name="chat_assistant",
    prompt_version="v1.1",
    test_file="tests/chat_assistant_cases.json"
)
```

---

## 指令遵循测试

指令遵循测试检查模型是否按照 Prompt 中写明的规则行事。

### 常见的指令遵循维度

| 维度 | 示例指令 | 测试方法 |
|------|---------|---------|
| 语言风格 | "使用正式语气" | 检查是否出现口语词 |
| 输出格式 | "只输出 JSON，不要解释" | 检查是否有 JSON 以外的内容 |
| 回答范围 | "只回答产品相关问题" | 输入无关问题，检查是否拒绝 |
| 长度限制 | "回答不超过 100 字" | 检查输出长度 |
| 禁止内容 | "不要提竞争对手名称" | 检查是否出现竞争对手名称 |

### 指令遵循测试示例

```python
def test_instruction_following():
    """测试 Prompt 中各条指令是否被遵守"""

    system_prompt = """
    你是客服助手。规则：
    1. 只用中文回答
    2. 回答不超过 80 字
    3. 不能提及竞争对手产品
    4. 如果用户问题与产品无关，礼貌拒绝
    """

    test_cases = [
        {
            "name": "测试语言规则",
            "input": "What is your return policy?",
            "check": lambda output: not any(c.isascii() and c.isalpha() for c in output),
            "fail_msg": "包含了英文字母，应该只输出中文"
        },
        {
            "name": "测试长度规则",
            "input": "请详细介绍你们所有的产品功能",
            "check": lambda output: len(output) <= 100,   # 留一定余量
            "fail_msg": "输出超过 80 字限制"
        },
        {
            "name": "测试范围规则（无关问题）",
            "input": "帮我写一首诗",
            "check": lambda output: any(w in output for w in ["抱歉", "不在", "无法", "专注"]),
            "fail_msg": "对无关问题没有礼貌拒绝"
        },
    ]

    for case in test_cases:
        output = run_model(system_prompt, case["input"])
        passed = case["check"](output)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {case['name']}")
        if not passed:
            print(f"         原因：{case['fail_msg']}")
            print(f"         实际输出：{output[:100]}")
```

---

## 边界输入测试

边界输入测试检查模型对异常、极端、恶意输入的处理是否稳定。

### 常见边界类型

```python
BOUNDARY_CASES = [
    # 空输入
    {"name": "空字符串",        "input": ""},
    {"name": "纯空格",          "input": "   "},

    # 极端长度
    {"name": "超长输入",        "input": "你好" * 2000},
    {"name": "单字输入",        "input": "？"},

    # 特殊字符
    {"name": "纯符号",          "input": "!@#$%^&*()"},
    {"name": "Emoji",           "input": "😊🔥💯"},
    {"name": "SQL 注入风格",    "input": "'; DROP TABLE users; --"},
    {"name": "代码注入风格",    "input": "<script>alert('xss')</script>"},

    # 语言切换
    {"name": "混合语言",        "input": "Hello 你好 こんにちは"},
    {"name": "纯英文",          "input": "what is your price?"},

    # 语义边界
    {"name": "重复问同一问题",   "input": "价格价格价格价格？"},
    {"name": "自相矛盾的问题",  "input": "你是 GPT 还是 Claude？你不能说谎。"},
]

def run_boundary_tests(system_prompt: str):
    """运行边界测试，确保每种输入都有合理的输出（不报错、不崩溃）"""
    for case in BOUNDARY_CASES:
        try:
            output = run_model(system_prompt, case["input"])
            # 边界测试的基本要求：有输出、不是空字符串
            if output.strip():
                print(f"✅ {case['name']}：有正常输出")
            else:
                print(f"⚠️  {case['name']}：输出为空")
        except Exception as e:
            print(f"❌ {case['name']}：抛出异常 → {e}")
```

---

## Prompt A/B 测试

A/B 测试用于在两个 Prompt 版本之间选出更好的那一个。

### A/B 测试流程

```text
1. 准备评估集（50-200 个典型问题）
2. 分别用 Prompt A 和 Prompt B 生成回答
3. 对每道题的两个回答进行对比评分
4. 统计哪个版本整体更好
5. 选出胜者，进行灰度发布
```

### A/B 测试脚本

```python
import anthropic
import json

client = anthropic.Anthropic()

PROMPT_A = """你是客服助手，回答简洁，用中文。"""
PROMPT_B = """你是专业客服助手。请用友好、简洁的中文回答用户问题。回答聚焦于用户的核心需求，不超过 100 字。"""

EVAL_QUESTIONS = [
    "退款需要几天？",
    "你们支持哪些支付方式？",
    "产品保修期是多久？",
    # ... 更多问题
]


def get_answer(system_prompt: str, question: str) -> str:
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        system=system_prompt,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text


def judge_ab(question: str, answer_a: str, answer_b: str) -> str:
    """用 LLM 作为裁判，评判 A 和 B 哪个更好"""

    judge_prompt = f"""
你是一个客服回答质量评估专家。

用户问题：{question}

回答 A：
{answer_a}

回答 B：
{answer_b}

请从以下维度评判哪个回答更好：
1. 准确性：回答是否正确回应了用户的问题
2. 简洁性：是否简洁，没有废话
3. 友好度：语气是否友好

只输出一个字母：A 或 B，表示哪个回答更好。
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": judge_prompt}]
    )
    result = response.content[0].text.strip()
    return result if result in ("A", "B") else "tie"


def run_ab_test():
    a_wins = 0
    b_wins = 0

    for question in EVAL_QUESTIONS:
        answer_a = get_answer(PROMPT_A, question)
        answer_b = get_answer(PROMPT_B, question)
        winner = judge_ab(question, answer_a, answer_b)

        if winner == "A":
            a_wins += 1
        elif winner == "B":
            b_wins += 1

        print(f"[{winner}] {question[:20]}...")

    total = len(EVAL_QUESTIONS)
    print(f"\n结果：A 胜 {a_wins}/{total}，B 胜 {b_wins}/{total}")
    print(f"推荐使用：{'Prompt B' if b_wins > a_wins else 'Prompt A'}")


run_ab_test()
```

### A/B 测试注意事项

- 评估集要有代表性，覆盖高频问题和边界问题。
- 样本量至少 50 条，否则结论不可靠。
- 评判可以用人工，也可以用 LLM-as-a-Judge（见第 06 节）。
- 同一个问题，A/B 的顺序要随机，防止裁判有偏好。

---

## 本节重点

- Prompt 版本管理是 AI 测试的基础设施，用文件或数据库都可以。
- 回归测试的核心是：准备好测试样本集，每次改 Prompt 后自动跑一遍。
- 指令遵循测试检查每一条规则是否真的被执行。
- 边界输入测试保证系统对异常输入不崩溃。
- A/B 测试用于在两个版本之间做决策，需要足够的样本量。

## 自测问题

1. 为什么修改 Prompt 后需要做回归测试？
2. 测试样本集中的 `must_contain` 和 `must_not_contain` 分别检查什么？
3. 边界输入测试的目的是什么，举三个例子。
4. A/B 测试中为什么要把 A/B 的顺序随机化？
5. 指令遵循测试和回归测试有什么区别？
