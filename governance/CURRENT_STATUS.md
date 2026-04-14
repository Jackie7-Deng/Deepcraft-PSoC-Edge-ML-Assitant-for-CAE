# 当前状态

**更新日期**: 2026-03-25
**工作区**: `PSoC_Edge_DeepCraft_AI`

## 当前结论

当前工作区的 DEEPCRAFT 官网网页知识链路已经切换到新的权威源并完成整链刷新：

- 当前网页权威清单：`ingest/urls_checked.txt`
- 当前抓取审计：`ingest/fetch_audit.json`
- 当前成功 / 失败清单：`ingest/url_success.txt`、`ingest/url_missing.txt`
- 当前网页主题摘要：`knowledge/deepcraft_web_backfill_20260310.md`
- 当前网页导航入口：`knowledge/deepcraft_web_catalog.md`
- 当前治理记录：`governance/ASSISTANT_TRAINING_AUDIT_LOG.md`
- 当前 Ready Model 本地目录：`docs/ready_model_notes/`
- 当前 Ready Model 导航入口：`knowledge/ready_models_catalog.md`

此外，本轮已经补上 **ModusToolbox 工具链知识入口** 与 **RAG 基础评测 / metadata 能力**：

- 新增 MTB 知识入口：`knowledge/modustoolbox_tools_summary.md`
- 新增检索评测样例：`evals/retrieval_cases.json`
- 新增检索评测脚本：`scripts/evaluate_retrieval.py`
- `semantic_search.py` / MCP `semantic_search` 已支持 metadata 过滤

本轮进一步补上 **RAG P3/P4 完整版能力**：

- 查询改写与显式 rerank
- grounded answer 证据包
- grounded answer 约束评测
- 根目录 `README.md` 与完整 `knowledge/usage_guide.md`

## 本轮已完成的关键事项

1. 明确停止回头审核旧 101 个 404 canonical 映射修正。
2. 将 `ingest/urls_checked.txt` 设为当前人工审核后的唯一权威 URL 基线。
3. 新增并刷新 `ingest/url_success.txt` / `ingest/url_missing.txt`。
4. 重写 `scripts/refresh_html_mirror.py`，使其以 checked 清单为输入，并同步写 mirror / success / missing / audit 四类产物。
5. 将 `ingest/html/*.md` 统一刷新为本轮成功抓取的 YAML front matter + markdown 镜像格式。
6. 将知识摘要层、导航层与治理层文档全部切换到新的权威口径。
7. 清理旧 `urls.txt`、旧发现清单、旧对比清单与过渡审计报告，避免旧口径继续污染工作区理解。
8. 将 `docs/MTB_docs/` 下三份 ModusToolbox 指南融合到 `knowledge/` 主链。
9. 为本地 RAG 增加 metadata 标签、自然边界切分与检索回归样例。
10. 为本地 RAG 增加查询改写、显式 rerank、grounded answer 与回答约束评测。
11. 新增根目录 `README.md`，把“用户如何用、是否要手动运行 RAG/MCP”说清楚。
12. 清理根目录示例 `README_*.md` 的重复摆放，统一由 `docs/readmes/` 作为归档入口。
13. 新增 `docs/ready_model_notes/` 8 份 Ready Model 测试报告，并通过 `knowledge/ready_models_catalog.md` 接入知识导航主链。

## 本轮抓取状态

- checked URL 总数：130
- 唯一 URL 数：129
- 成功数：128
- 失败数：2
- 实际写入 html 文件数：127
- 覆盖率（checked）：98.5%
- 覆盖率（unique）：98.4%
- 重复 URL：1 条（`https://developer.imagimob.com/deepcraft-studio/deployment/edge-api` 在 checked 清单中出现 2 次）

## 当前仍保留的真实缺口

- 当前仅有 2 条 checked URL 失败，且都是现站点 404：
  - `https://developer.imagimob.com/deepcraft-studio/getting-started/accelerators`
  - `https://developer.imagimob.com/deepcraft-studio/getting-started/project-templates`
- `ingest/html/` 已收敛为当前 checked 基线成功抓取的 127 个镜像文件；后续继续以 `fetch_audit.json` / `url_success.txt` 为准。
- 站点未来如果再次改版，仍需要以新的人工审核清单为准重新刷新，而不是自动继承旧 URL 假设。
- 当前 RAG 已补上标准检索回归样例、基础 metadata 过滤、查询改写、显式 rerank 与 grounded answer；但仍缺少更强的模型级 query rewrite、多级索引摘要层与自动 citation validator。
- 当前 `docs/ready_model_notes/*.pdf` 尚未做页级文本抽取；目前通过 `knowledge/ready_models_catalog.md` 作为检索入口，后续仍可补 PDF 解析 / citation validator。

## 本轮验证

- `scripts/refresh_html_mirror.py` 执行完成：通过
- `ingest/url_success.txt` 已生成：通过
- `ingest/url_missing.txt` 已生成：通过
- `ingest/fetch_audit.json` 已更新为 checked 基线审计结果：通过
- `knowledge/deepcraft_web_catalog.md` 已切换到 checked 权威口径：通过
- `knowledge/deepcraft_web_backfill_20260310.md` 已更新为主题化摘要：通过
- `knowledge/retrieval_guide.md` / `knowledge/overview.md` / `knowledge/document_map.md` 已同步：通过
- `governance/ASSISTANT_TRAINING_AUDIT_LOG.md` 已同步：通过
- `knowledge/modustoolbox_tools_summary.md` 已新增并接入知识链：通过
- `scripts/evaluate_retrieval.py` / `evals/retrieval_cases.json` 已新增：通过
- `knowledge/ready_models_catalog.md` 已新增并接入主导航链：通过
- 根目录重复 `README_*.md` 已清理，`docs/readmes/` 归档保留：通过
- 本轮索引重建完成：`file_count=405`、`chunk_count=5446`、`symbol_count=14121`：通过
- 本轮检索回归：`8/8` 命中，`hit_rate=100%`：通过
- `scripts/grounded_answer.py` / `scripts/evaluate_grounded_answer.py` / `evals/grounded_answer_cases.json` 已新增：通过
- grounded answer 约束评测：`4/4` 通过，`ok_rate=100%`：通过
- `README.md` / `knowledge/usage_guide.md` 已更新：通过
