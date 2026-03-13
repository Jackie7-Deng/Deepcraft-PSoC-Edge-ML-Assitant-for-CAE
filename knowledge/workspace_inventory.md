# 工作区清单

**更新日期**: 2026-03-10
**工作区路径**: `C:\Users\DengJi\Desktop\workfiles\16-AI-Agent_for copilot\PSoC_Edge_DeepCraft_AI\`

## 1. 助手层现状
- 规范初始化入口：`CLAUDE.md`
- 镜像初始化入口：`.claude/CLAUDE.md`
- Skills：`.claude/skills/`（4 个）
- Prompts：`prompts/`（4 个）
- 结构化索引：`indexes/`
- MCP 服务：`mcp_servers/`
- 状态面板：`memory/SESSION_STATE.md`
- 治理文件：`governance/CURRENT_STATUS.md`、`governance/ASSISTANT_TRAINING_AUDIT_LOG.md`

## 2. 关键知识入口
- `knowledge/document_map.md`
- `knowledge/overview.md`
- `knowledge/faq.md`
- `knowledge/modustoolbox_tools_summary.md`
- `knowledge/parameters_catalog.md`
- `knowledge/troubleshooting_playbook.md`
- `knowledge/examples_catalog.md`
- `knowledge/retrieval_guide.md`
- `knowledge/usage_guide.md`
- `README.md`

## 3. 检索与工具资产
- `indexes/index_summary.json`
- `indexes/symbol_index.json`
- `indexes/text_chunks.jsonl`
- `indexes/vector_db/`
- `scripts/semantic_search.py`
- `scripts/grounded_answer.py`
- `scripts/evaluate_retrieval.py`
- `scripts/evaluate_grounded_answer.py`
- `scripts/symbol_search.py`
- `scripts/verify_ingest.py`
- `mcp_servers/vector_search_server.py`
- `evals/retrieval_cases.json`
- `evals/grounded_answer_cases.json`

## 3.1 当前网页抓取核心资产
- `ingest/urls_checked.txt`
- `ingest/url_success.txt`
- `ingest/url_missing.txt`
- `ingest/fetch_audit.json`
- `ingest/html/*.md`

## 4. 语言约定
- 当前助手维护层主干文档默认使用中文
- 原始证据类文档允许保留原始英文内容，以保证可追溯性
