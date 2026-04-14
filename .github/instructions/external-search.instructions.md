---
description: "Use when searching community, case, MCP, external evidence, field experience, historical issues, or when the user says 搜索此问题 / 查社区 / 查case / 外部检索. Covers query compression, iterative search, search-select-read separation, and anti-loop safeguards for PSoC Edge and PSoC 6 support."
---
# 外部检索与 MCP 指令

- 先判断本地知识是否已足够；只有本地证据不足，或用户明确要求查 Community / Case 时，才进入外部检索。
- 不要把用户原句原封不动丢进搜索框。先压缩成短 query，再扩展：
  1. **第一轮**：芯片/板卡/示例 + 主症状
  2. **第二轮**：补 ML 框架 / toolchain / memory
  3. **第三轮**：补 platform / peripheral / version
- 当前仓库的外部检索语境必须是 **PSoC Edge / PSoC 6 / DEEPCRAFT / MTB ML**，不要复用旧项目的 `FX3 / CX3 / UVC` 词表。
- 搜索不要只做一次。默认流程：
  1. `search`
  2. 选最相关的 2~3 条结果
  3. `read`
  4. 先摘要，再决定是否改写下一轮 query
- Community / Case 正文先摘要成：
  - 问题
  - 现象
  - 调试过程
  - 解决建议
  - 未决项
- 对 Case 系统，搜索结果页要优先切到 `Cases` 结果表，再抽 `Subject / Description / Case number`。
- 组合式防循环默认值：
  - 同一 query / URL 最多重复 2~3 次
  - 若自动化真的会展开结果链接，单轮最多打开 10~20 个
  - Search / read 都要有超时预算
  - 连续 3~5 次没有拿到新证据时停止
- 停止时必须返回：
  - 最佳已得证据
  - 还缺什么
  - 为什么停止
  - 下一步建议
