# PSoC Edge + DEEPCRAFT 一页纸总览

**更新日期**: 2026-03-10

## 1. 应用目标

本工作区用于将 **PSoC Edge + DEEPCRAFT Studio** 相关 PDF、README、网页资料、示例工程与本地检索能力整理成一个可检索、可引用、可维护的专属助手知识库。

## 2. 助手分层

| 层级 | 位置 | 作用 |
|------|------|------|
| 初始化层 | `CLAUDE.md`、`.claude/CLAUDE.md`、`AGENTS.md`、`.github/copilot-instructions.md` | 定义身份、边界与引用规则 |
| 路由层 | `.claude/skills/`、`prompts/` | 按问题类型分流 |
| 结构化知识层 | `knowledge/` | FAQ、参数、工作流、网页摘要、导航 |
| 检索与工具层 | `indexes/`、`scripts/semantic_search.py`、`mcp_servers/vector_search_server.py` | 关键词/语义混合检索、符号检索、MCP 工具调用 |
| 一级证据层 | `docs/`、`docs/readmes/`、`docs/MTB_docs/`、`ingest/urls_checked.txt`、`ingest/url_success.txt`、`ingest/url_missing.txt`、`ingest/fetch_audit.json`、`ingest/html/`、示例工程源码 | 最终证据来源 |
| 治理层 | `memory/`、`governance/` | 状态、审计、改进记录 |

## 3. 平台边界

- **PSoC Edge E8x**：NPU / Edge AI 主场景
- **PSoC 6 / CY8CKIT-062S2-AI**：MTB ML / Imagimob 示例场景

## 3.1 开发工具链栈

- **ModusToolbox tools package**：负责 Dashboard、Project Creator、构建系统、manifest/BSP 发现等工程级能力。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#6` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`
- **Device Configurator**：负责 pins、clocks、peripherals、DMA 等器件级硬件配置，并生成 `GeneratedSource`。`docs\MTB_docs\device-configurator.pdf#4` `docs\MTB_docs\device-configurator.pdf#11`
- **Machine Learning configurator**：属于 library-level configurator，和 Device Configurator 不是同一层。`docs\MTB_docs\New-to-ModusToolbox.pdf#2`
- **本工作区的低 token 入口**：`knowledge\modustoolbox_tools_summary.md`

## 4. 关键入口地图

| 类型 | 入口 |
|------|------|
| 全局导航 | `knowledge/document_map.md` |
| 工作区门面 | `README.md` |
| 示例与 README | `knowledge/examples_catalog.md`、`docs/readmes/README_*.md` |
| 工作流 | `knowledge/ml_workflow.md` |
| FAQ / 工程经验 | `knowledge/faq.md` |
| ModusToolbox 工具链 | `knowledge/modustoolbox_tools_summary.md` |
| 网页目录入口 | `knowledge/deepcraft_web_catalog.md` |
| 网页主题摘要 | `knowledge/deepcraft_web_backfill_20260310.md` |
| 网页抓取审计 | `ingest/fetch_audit.json`、`ingest/url_success.txt`、`ingest/url_missing.txt` |
| 参数目录 | `knowledge/parameters_catalog.md` |
| 排障手册 | `knowledge/troubleshooting_playbook.md` |
| 检索指南 | `knowledge/retrieval_guide.md` |
| 索引摘要 | `indexes/index_summary.json` |

## 5. 当前网页知识状态

- 本轮网页工作已经明确切换到 `ingest/urls_checked.txt` 作为权威清单
- 当前 checked URL 130 条，唯一 URL 129 条
- 成功抓取 128 条，失败 2 条，实际写入镜像 127 个
- 失败项仅剩 2 条旧路径 404；本轮不再追查旧 canonical 映射
- 回答网页问题时，应先走目录  摘要  审计  原文镜像的路径
- 当前还支持 grounded answer 证据包，可用于高风险回答和客户回复前的证据组织

## 6. 治理与维护入口

- 当前状态：`governance/CURRENT_STATUS.md`
- 当前审计日志：`governance/ASSISTANT_TRAINING_AUDIT_LOG.md`
- 会话状态：`memory/SESSION_STATE.md`
- 后续计划：`knowledge/improvement_plan.md`
