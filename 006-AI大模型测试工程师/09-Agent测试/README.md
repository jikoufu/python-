# 09 Agent 测试

Agent 测试是大模型测试中最难的一块。因为 Agent 不只是回答问题，它还会规划步骤、选择工具、传参数、执行动作、根据结果继续推理。测试 Agent 时，不能只看最终答案，必须看执行轨迹。

## 本章你要学会什么

- 理解 Agent 的执行流程。
- 设计任务型测试用例。
- 测试工具选择、参数、权限和失败恢复。
- 分析 Agent 执行轨迹。
- 建立 Agent 回归测试集。

## 推荐学习顺序

1. [01-Agent测试核心概念.md](</D:/PycharmProjects/python后端学习/006-AI大模型测试工程师/09-Agent测试/01-Agent测试核心概念.md>)
2. [02-Agent测试用例设计.md](</D:/PycharmProjects/python后端学习/006-AI大模型测试工程师/09-Agent测试/02-Agent测试用例设计.md>)
3. [03-Agent自动化评测流程.md](</D:/PycharmProjects/python后端学习/006-AI大模型测试工程师/09-Agent测试/03-Agent自动化评测流程.md>)
4. [04-Agent的Memory机制.md](</D:/PycharmProjects/python后端学习/006-AI大模型测试工程师/09-Agent测试/04-Agent的Memory机制.md>)
5. [05-ToolCall测试详解.md](</D:/PycharmProjects/python后端学习/006-AI大模型测试工程师/09-Agent测试/05-ToolCall测试详解.md>) —— 工具调用测试单独拆透
6. [06-学习路线与资料.md](</D:/PycharmProjects/python后端学习/006-AI大模型测试工程师/09-Agent测试/06-学习路线与资料.md>) —— 学习路线 + 资料 + 练手项目

## Agent 测试核心结论

```text
Agent 测试 = 最终结果测试 + 中间步骤测试 + 工具权限测试 + 失败恢复测试。
```

如果 Agent 带 Memory，还要额外测试：

```text
记忆是否正确保存、正确读取、用户隔离、可更新、可删除、不泄露、不污染当前任务。
```
