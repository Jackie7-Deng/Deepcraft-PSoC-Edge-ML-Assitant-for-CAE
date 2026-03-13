# 文档地图

**更新日期**: 2026-03-10  
**用途**: 作为全局导航入口，先缩小搜索范围，再进入 PDF、README、网页归档、结构化索引或源码。

---

## 1. 按问题类型找入口

| 问题类型 | 第一入口 | 继续深挖 |
|----------|----------|----------|
| 学习整个工作区 | `knowledge/overview.md` | `knowledge/ml_workflow.md` |
| 高频问题 / 经验问题 | `knowledge/faq.md` | `knowledge/assistant_user_guide.md` |
| ModusToolbox 工具链 / BSP / Makefile | `knowledge/modustoolbox_tools_summary.md` | `docs/MTB_docs/*.pdf`、README |
| 参数 / 上下文缺失 | `knowledge/parameters_catalog.md` | README、工作流文档、示例代码 |
| 排障 | `knowledge/troubleshooting_playbook.md` | README、源码、PDF |
| 示例选择 | `knowledge/examples_catalog.md` | `docs/readmes/README_*.md` |
| DEEPCRAFT 网页内容 | `knowledge/deepcraft_web_catalog.md` | `knowledge/deepcraft_web_backfill_20260310.md`、`ingest/urls_checked.txt`、`ingest/url_success.txt`、`ingest/url_missing.txt`、`ingest/fetch_audit.json`、`ingest/html/*.md` |
| 结构化检索 / RAG | `knowledge/retrieval_guide.md` | `indexes/index_summary.json`、`indexes/text_chunks.jsonl` |
| PSoC Edge TRM / Kit / Registers | `knowledge/index_architecture_rm.md`、`knowledge/index_kit_guide.md`、`knowledge/index_registers_rm.md` | 对应 `docs/**/*.pdf` |
| 工作区怎么用 | `README.md`、`knowledge/usage_guide.md` | `CLAUDE.md`、`.github/copilot-instructions.md` |

## 2. 核心知识入口

- `knowledge/overview.md`
- `knowledge/faq.md`
- `knowledge/modustoolbox_tools_summary.md`
- `knowledge/parameters_catalog.md`
- `knowledge/troubleshooting_playbook.md`
- `knowledge/ml_workflow.md`
- `knowledge/examples_catalog.md`
- `knowledge/api_reference.md`
- `knowledge/usage_guide.md`
- `knowledge/retrieval_guide.md`
- `knowledge/deepcraft_web_catalog.md`
- `knowledge/deepcraft_web_backfill_20260310.md`
- `README.md`

## 3. 检索与工具入口

- `indexes/index_summary.json`
- `indexes/symbol_index.json`
- `indexes/text_chunks.jsonl`
- `indexes/vector_db/`
- `evals/retrieval_cases.json`
- `evals/grounded_answer_cases.json`
- `scripts/semantic_search.py`
- `scripts/grounded_answer.py`
- `scripts/evaluate_retrieval.py`
- `scripts/evaluate_grounded_answer.py`
- `scripts/symbol_search.py`
- `mcp_servers/vector_search_server.py`
- `scripts/refresh_html_mirror.py`

## 4. 治理与状态入口

- `memory/SESSION_STATE.md`
- `governance/CURRENT_STATUS.md`
- `governance/ASSISTANT_TRAINING_AUDIT_LOG.md`
- `knowledge/improvement_plan.md`
