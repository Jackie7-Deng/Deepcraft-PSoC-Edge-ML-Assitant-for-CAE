# PSoC Edge + DEEPCRAFT 一页纸总览

**更新日期**: 2026-03-25

## 1. 应用目标

本工作区用于将 **PSoC Edge + DEEPCRAFT Studio** 相关 PDF、README、网页资料、示例工程与本地检索能力整理成一个可检索、可引用、可维护的专属助手知识库。

## 2. 助手分层

| 层级 | 位置 | 作用 |
|------|------|------|
| 初始化层 | `CLAUDE.md`、`.claude/CLAUDE.md`、`AGENTS.md`、`.github/copilot-instructions.md`、`.github/instructions/external-search.instructions.md` | 定义身份、边界、检索触发方式与引用规则 |
| 路由层 | `.claude/skills/`、`prompts/` | 按问题类型分流 |
| 结构化知识层 | `knowledge/` | FAQ、参数、工作流、网页摘要、导航 |
| 检索与工具层 | `indexes/`、`scripts/semantic_search.py`、`mcp_servers/vector_search_server.py` | 关键词/语义混合检索、符号检索、MCP 工具调用 |
| 一级证据层 | `docs/`、`docs/readmes/`、`docs/ready_model_notes/`、`docs/MTB_docs/`、`ingest/urls_checked.txt`、`ingest/url_success.txt`、`ingest/url_missing.txt`、`ingest/fetch_audit.json`、`ingest/html/`、示例工程源码 | 最终证据来源 |
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
| Ready Model 报告 | `knowledge/ready_models_catalog.md`、`docs/ready_model_notes/*.pdf` |
| 工作流 | `knowledge/ml_workflow.md` |
| FAQ / 工程经验 | `knowledge/faq.md` |
| ModusToolbox 工具链 | `knowledge/modustoolbox_tools_summary.md` |
| Memory / linker / XIP | `knowledge/memory_layout_guide.md` |
| 网页目录入口 | `knowledge/deepcraft_web_catalog.md` |
| 网页主题摘要 | `knowledge/deepcraft_web_backfill_20260310.md` |
| 网页抓取审计 | `ingest/fetch_audit.json`、`ingest/url_success.txt`、`ingest/url_missing.txt` |
| 参数目录 | `knowledge/parameters_catalog.md` |
| 版本兼容 | `knowledge/version_compatibility_guide.md` |
| AI Kit 入口 | `knowledge/index_ai_kit_guide.md` |
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
- 当前已新增本地 Ready Model 报告目录：`docs/ready_model_notes/`（8 份 PDF），并通过 `knowledge/ready_models_catalog.md` 接入主导航链

## 6. 治理与维护入口

- 当前状态：`governance/CURRENT_STATUS.md`
- 当前审计日志：`governance/ASSISTANT_TRAINING_AUDIT_LOG.md`
- 会话状态：`memory/SESSION_STATE.md`
- 模板差距分析：`governance/plan_gap_analysis.md`
- 当前轮唯一进度源：`governance/TODO.md`
- MCP 回归与可观测：`governance/mcp_regression_suite.md`、`governance/mcp_observability.md`
- 后续计划：`knowledge/improvement_plan.md`

## 7. 当前仍待补强的专题

- **generated-code / API 线索仍需细化**：当前 `knowledge/api_reference.md` 已明确自己是入口导览，不是完整 SDK/API 字典，因此后续若要回答更细的生成代码接口或函数签名问题，仍需继续补 `generated-code` 到 API 的映射页。`knowledge/api_reference.md:23-27` `knowledge/improvement_plan.md:6-11`
- **版本兼容已补出初版专题，但仍不是全覆盖矩阵**：当前已经新增 `knowledge/version_compatibility_guide.md`，能回答 3.6 / 3.7 tools package 变化与常见 workaround；但针对全部 BSP / ML Pack / DEEPCRAFT Studio 组合的完整矩阵仍未成型。`knowledge/version_compatibility_guide.md` `knowledge/parameters_catalog.md`
- **KIT_PSE84_AI 文档入口已补到本地链条**：当前可以通过 `knowledge/index_ai_kit_guide.md` 进入 AI Kit 用户指南、schematic、layout、BoM 与制造文件，不必再只依赖网页摘要。`knowledge/index_ai_kit_guide.md` `docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#6`
- **memory 布局专题已补到本地链条**：新增应用笔记与 CTW 已通过 `knowledge/memory_layout_guide.md` 回灌到知识层，后续回答 memory placement / XIP / linker 问题应优先引用本地 PDF 页码，而不是只引用 community 贴。`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#1` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#17`
- **更细粒度排障案例仍需继续沉淀**：当前排障与 FAQ 已能做一级分诊，但真实日志模式、链接错误、烧录失败、NPU fallback、摄像头链路等二级 runbook 仍需持续扩充。`knowledge/troubleshooting_playbook.md:8-101` `knowledge/improvement_plan.md:6-11`
- **外部经验回灌入口已补齐，但默认仍应本地优先**：按照训练模板与当前初始化规则，Community / Case 经验默认只作为补充证据，不覆盖 README、源码、PDF 与本地网页镜像。`GENERIC_SPECIALIZED_QA_ASSISTANT_TEMPLATE.md:234-370` `CLAUDE.md:11-17`
- **新增治理与回归底座**：本轮补了 `governance/TODO.md`、`governance/plan_gap_analysis.md`、`governance/issues_log.md`、`governance/knowledge_governance.md`、`governance/mcp_regression_suite.*`、`governance/mcp_observability.md`、`governance/rag_regression.md` 与 `indexes/chunk_schema.md`，后续回归与补缺应优先落盘到这些文件。
