# TODO

**当前轮目标**: 根据升级版模板补齐治理/回归底座，融合新增 memory 文档，并增强、测试 PSoC Edge MCP 搜索链。

## 已完成

- [x] 对照新版模板完成 gap audit
- [x] 把两份 memory PDF 提炼进 `knowledge/memory_layout_guide.md`
- [x] 为 lightweight RAG 补 `chunk_schema.md`
- [x] 为 MCP 补 regression suite / observability / runner
- [x] 为证据链补 `knowledge_governance.md`、`evidence_scoring.md`、`evidence_arbitrator.py`

## 本轮测试待记录

- [x] 5 条 Community 搜索回归
- [x] 5 条 MSD/Case 搜索回归
- [x] 把实际阻碍与脚本缺陷回写到本文件和 `issues_log.md`

## 当前已知阻碍 / 不好用的点

1. **宿主 MCP client 不会自动接入当前仓库 `.vscode/mcp.json`**
   - 现象：仓库内 server 可启动，但对话工具层不会自动注册对应 MCP tools
   - 影响：验证时只能通过 Playwright 脚本直跑，不能完全模拟“宿主已托管的 MCP”
   - 处理：保留本地 server + browser 会话，回归改用 `run_mcp_regression.py`

2. **Case discussion 的 `Load all / Load more` 提取不稳定**
   - 现象：部分 Case 页面按钮存在但不可见或不可点
   - 影响：有时只能拿到 header / description，拿不到完整讨论闭环
   - 处理：保留问题到 `issues_log.md`，优先做搜索与摘要层增强

3. **Community 泛 query 仍容易偏向 PDF / 产品页**
   - 现象：像 memory / deploy 这类宽 query，结果会被 PDF、产品页和 GitHub 结果抢占
   - 影响：社区经验召回率不稳定
   - 处理：已扩展 `search_utils.py` 的 memory/version 词表，并新增 community source score，对文档 / GitHub / 产品页降权，对真实 community thread 加权

4. **Case 变体 query 曾退化成过泛搜索**
   - 现象：`PSoC machine learning RAM flash size limitation` 在旧逻辑下第一轮会退化成 `machine learning`
   - 影响：容易召回营销页、下载问题等弱相关 case，拉低前排结果质量
   - 处理：已调整 `build_psoc_edge_queries()`，优先保留原始 seed query，并在信号词不足时退回到 seed token 片段，而不是只保留单个宽词

5. **长自然语言虽然已不再整句入搜，但压缩后仍可能过宽**
   - 现象：`为什么 ML converter 报错...格式有什么要求` 已被压缩为 `PSoC Edge DEEPCRAFT Model Converter`，但缺少 `error` / `model format` 这类症状化提示
   - 影响：Community 仍可能优先命中产品页、PDF 或总览页，而不是故障经验帖
   - 处理：本轮冒烟先记录，待测试完成后统一补 query hint 提取

6. **Case 搜索结果顶层 `query` 字段仍可能回显原始输入**
   - 现象：虽然 `queries_tried` 已是压缩后的英文短 query，但返回 JSON 顶层 `query` 仍可能是用户原始自然语言
   - 影响：会误导上层 Agent，以为脚本仍把整句直接送进搜索框
   - 处理：本轮冒烟先记录，待测试完成后统一修正返回字段语义

## 本轮回归结果（2026-04-14）

- `governance/mcp_regression_last_run.json`：10/10 通过
- Community 平均质量分偏低的 query：
  - `PSoC Edge MTBML model deploy` -> 0.296（结果仍偏官方 guide / GitHub）
  - `PSoC Edge memory placement` -> 0.396（结果仍偏 application note / memory doc）
  - `PSoC Edge SMIF XIP external flash` -> 0.436（XIP 主题仍容易被官方 note 抢占）
- MSD/Case 平均质量分偏低的 query：
  - `PSoC machine learning RAM flash size limitation` -> 0.366（已不再先退化成 `machine learning`，但资源限制类 query 仍需更强的 memory-specific 扩词）
  - `PSoC 6 ModusToolbox programming failed KitProg` -> 0.544（能召回，但主题分布仍较散）
- 其他观察：
  - `PSoC Edge Face ID demo` -> 0.9（community thread 排序明显更靠前）
  - `community_read_playwright.py` 已输出 `summary`，但复杂长帖的 `phenomena` / `resolution_hint` 仍偏粗，需要后续继续做角色分段和问答式摘要
  - 运行期仍会出现 Node `DEP0169 url.parse()` warning，当前不阻断功能，但日志噪声较大
