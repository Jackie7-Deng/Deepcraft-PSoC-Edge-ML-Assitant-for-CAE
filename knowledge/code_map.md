# 工作区代码与脚本地图

**更新日期**: 2026-04-14  
**定位**: 当前 `code/` 目录仍为空，因此本页主要给出检索脚本、MCP 脚本与回归脚本的导航入口。

## 1. MCP / 浏览器自动化

| 文件 | 作用 |
|------|------|
| `mcp_servers/infineon_browser_server.py` | PSoC Edge / DeepCraft AI 的 Community + MSD/Case MCP 入口，负责 tool/resource/prompt 暴露 |
| `scripts/launch_infineon_mcp_browser.py` | 启动或复用带 CDP 的 Edge 浏览器 |
| `scripts/community_search_playwright.py` | 通过网络拦截抓 Community 搜索结果 |
| `scripts/community_read_playwright.py` | 读取 Community 帖子或 KBA 正文 |
| `scripts/case_search_playwright.py` | 读取 Dynamics Case 搜索页并抽取 Cases 表格 |
| `scripts/case_read_playwright.py` | 打开 Case 详情页并抽取摘要、discussion、header fields |
| `scripts/case_summary.py` | 把 Case discussion 粗摘要成 problem / actions / resolution note |

## 2. 关键词扩展与仲裁

| 文件 | 作用 |
|------|------|
| `scripts/search_utils.py` | 外部搜索关键词扩展、结果打分、质量评分 |
| `scripts/evidence_arbitrator.py` | 规则化证据打分与排序，帮助在 PDF / README / community / case 之间做优先级仲裁 |
| `knowledge/evidence_scoring.md` | 证据等级与评分规则说明 |

## 3. 轻量 RAG

| 文件 | 作用 |
|------|------|
| `scripts/lightweight_rag.py` | 轻量本地 chunk index 的构建与搜索核心 |
| `scripts/build_lightweight_index.py` | 生成 `indexes/lightweight_index.json` |
| `scripts/search_lightweight_index.py` | 直接查询 lightweight index |
| `indexes/chunk_schema.md` | lightweight index 的字段契约 |
| `rag_regression.md` | 轻量 RAG 固定查询回归集 |

## 4. MCP 回归与可观测

| 文件 | 作用 |
|------|------|
| `mcp_regression_suite.json` | 5 条 Community + 5 条 MSD/Case 固定回归用例 |
| `mcp_regression_suite.md` | 回归用例的人类可读说明 |
| `mcp_observability.md` | MCP 回归落盘字段与 stop rules 说明 |
| `run_mcp_regression.py` | 执行 MCP 回归、输出 summary JSON 与 JSONL 审计日志 |

## 5. 当前边界

- 当前 `code/` 目录没有已提交源码，因此若用户问“业务逻辑在哪个 `.c/.h`”，多数情况下仍应回到示例工程目录、README 或 `scripts/` / `mcp_servers/`。
- 若后续将示例工程源码系统化沉淀进 `code/`，建议把本页升级为真正的源码模块地图，而不只是脚本地图。
