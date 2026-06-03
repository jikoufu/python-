# 03 Agent 自动化评测流程

## 学习目标

这一节学习如何自动化测试 Agent。

你需要掌握：

- Agent 接口应该返回什么。
- 如何断言工具调用。
- 如何分析执行轨迹。
- 如何输出 Agent 测试报告。

## Agent 接口响应建议

为了方便测试，Agent 接口最好返回执行轨迹：

```json
{
  "task": "查询北京天气",
  "answer": "北京今天晴朗。",
  "steps": [
    {
      "type": "tool_call",
      "tool": "get_weather",
      "args": {
        "city": "北京"
      }
    },
    {
      "type": "tool_result",
      "tool": "get_weather",
      "result": {
        "weather": "晴朗"
      }
    }
  ]
}
```

如果没有 `steps`，测试只能看最终答案，很难判断 Agent 是否真的做对了。

## 自动化断言

### 工具是否被调用

```python
tools = [step["tool"] for step in data["steps"] if step["type"] == "tool_call"]
assert "get_weather" in tools
```

### 禁止工具未被调用

```python
for forbidden_tool in case["forbidden_tools"]:
    assert forbidden_tool not in tools
```

### 参数是否正确

```python
weather_call = next(
    step for step in data["steps"]
    if step["type"] == "tool_call" and step["tool"] == "get_weather"
)

assert weather_call["args"]["city"] == "北京"
```

### 是否无限循环

```python
assert len(data["steps"]) <= 10
```

## Agent 测试报告模板

```markdown
# Agent 测试报告

## 测试范围

- Agent：学习助手 Agent
- 工具数量：6
- 测试样本：80

## 总体结果

| 指标 | 数值 |
|------|------|
| 总用例数 | 80 |
| 通过数 | 68 |
| 失败数 | 12 |
| 通过率 | 85% |

## 失败分类

| 类型 | 数量 |
|------|------|
| 工具误选 | 3 |
| 参数错误 | 4 |
| 禁止工具调用 | 1 |
| 最终回答错误 | 2 |
| 工具失败处理不当 | 2 |

## 典型失败

### AGENT_014

- 任务：查询北京天气
- 期望工具：get_weather
- 实际工具：web_search
- 失败原因：工具误选
```

## Agent 自动化优先级

建议按这个顺序做：

1. 最终答案非空。
2. 工具调用轨迹存在。
3. 期望工具被调用。
4. 禁止工具未调用。
5. 工具参数正确。
6. 调用顺序正确。
7. 工具失败时处理合理。
8. 权限和注入攻击用例通过。

## 本节重点

- Agent 自动化测试必须要求接口返回 steps。
- 工具选择、参数和禁止工具是最重要的自动断言。
- Agent 测试报告要按失败类型分类。
- 自动化测试可以先用规则断言，再引入 LLM Judge。
