# 检索与 RAG 使用指南

**更新日期**: 2026-03-25  
**定位**: 说明当前工作区如何在权威 URL 清单  抓取审计  原始镜像  知识摘要之间做低 token 检索。

## 1. 当前检索层包含什么

- `indexes/symbol_index.json`：函数、宏、标题等符号索引
- `indexes/text_chunks.jsonl`：按块切分后的结构化文本索引
- `indexes/processed_files.json`：已处理文件清单
- `indexes/index_summary.json`：索引摘要
- `indexes/vector_db/`：轻量向量索引与倒排表
- `mcp_servers/vector_search_server.py`：MCP 检索服务
- `knowledge/modustoolbox_tools_summary.md`：ModusToolbox 工具链低 token 摘要入口
- `knowledge/ready_models_catalog.md`：Ready Model 报告、申请方式、收费与测试入口
- `knowledge/deepcraft_web_catalog.md`：网页导航入口
- `knowledge/deepcraft_web_backfill_20260310.md`：网页主题总结摘要
- `docs/ready_model_notes/*.pdf`：本地 Ready Model 测试报告原件
- `ingest/urls_checked.txt`：当前人工审核后的权威 URL 清单
- `ingest/url_success.txt`：本轮成功抓取 URL 清单
- `ingest/url_missing.txt`：本轮失败 URL 清单与失败原因
- `ingest/fetch_audit.json`：每个 checked URL 的抓取状态、输出文件、重试次数、redirect 与原因
- `ingest/html/*.md`：本轮成功刷新的网页镜像证据层
- `evals/retrieval_cases.json`：当前检索回归样例
- `scripts/evaluate_retrieval.py`：检索回归执行脚本
- `scripts/grounded_answer.py`：带回答约束的证据包生成脚本
- `evals/grounded_answer_cases.json`：grounded answer 约束样例
- `scripts/evaluate_grounded_answer.py`：grounded answer 校验脚本

## 2. 当前网页检索推荐路径

1. 先用 `knowledge/deepcraft_web_catalog.md` 判断主题。
2. 再用 `knowledge/deepcraft_web_backfill_20260310.md` 获取压缩后的主题结论。
3. 如果只想确认这页抓到了没有，看 `ingest/url_success.txt` / `ingest/url_missing.txt`。
4. 如果想知道 HTTP 状态码、重试次数、输出文件、redirect，查看 `ingest/fetch_audit.json`。
5. 如果要引用网页正文证据，再进入 `ingest/html/*.md`。

## 3. 什么时候用什么

| 场景 | 推荐方式 |
|------|----------|
| 查概念、FAQ、排障段落 | `semantic_search.py` |
| 查函数、宏、标题 | `symbol_search.py` |
| 查 ModusToolbox / BSP / Device Configurator | `knowledge/modustoolbox_tools_summary.md`，再进 `docs/MTB_docs/*.pdf` |
| 查高风险问题的可引用证据包 | `grounded_answer.py` 或 MCP `grounded_answer` |
| 查 Ready Models / 收费 / 申请 / 本地测试报告 | `knowledge/ready_models_catalog.md`，再进 `docs/ready_model_notes/*.pdf` 与 `ingest/html/deepcraft-ready-models*.md` |
| 查当前网页主题摘要 | `knowledge/deepcraft_web_backfill_20260310.md` |
| 查某个 checked URL 本轮是否成功 | `ingest/url_success.txt` / `ingest/url_missing.txt` |
| 查某个 checked URL 的详细抓取状态 | `ingest/fetch_audit.json` |
| 查网页原文证据 | `ingest/html/*.md` |
| 新资料进入后重建索引 | `run_ingest_pipeline.py` |
| 做检索回归验证 | `evaluate_retrieval.py` |

## 4. 当前实现特点

- 当前网页权威源已经从旧 `ingest/urls.txt` 切换为 `ingest/urls_checked.txt`
- 本轮不再围绕旧 101 个 404 canonical 映射继续纠缠，直接以人工审核后的 checked 清单为准
- 成功页面与失败页面已经拆分到 `url_success.txt` / `url_missing.txt`
- 抓取审计、原始镜像、知识摘要、治理文档已经打通成同一条逻辑链
- 当前网页覆盖率：checked 98.5% / unique 98.4%
- 当前检索已支持基于 `source_type`、`path_prefix` 和新增的 metadata 过滤（平台 / 工具链 / 文档类别 / 证据层级）
- 当前检索已支持查询改写与显式 rerank
- 当前已支持 grounded answer 证据包，用于更严格的回答约束
- 当前已新增检索回归样例，可对常见问题做最小化命中率检查
- 当前 `docs/ready_model_notes/*.pdf` 仍未直接抽取页级正文；检索侧通过 `knowledge/ready_models_catalog.md` 将其接入主链

## 5. 维护时的注意事项

- 当前网页抓取输入固定为 `ingest/urls_checked.txt`。
- 不要重新引入旧的 URL 对比清单、发现清单或历史过渡文件，以免污染检索结果。
- 回答网页类问题时，优先信任 `urls_checked.txt`、`fetch_audit.json` 与本轮新镜像，不要优先引用旧抓取残留。
- 回答 ModusToolbox 工具链问题时，优先从 `knowledge/modustoolbox_tools_summary.md` 缩小范围，再回到 `docs/MTB_docs/*.pdf`。
- 回答 Ready Models 问题时，优先从 `knowledge/ready_models_catalog.md` 确认本地 PDF 是否存在，再结合网页镜像回答申请、收费与部署路径。
- 新增知识入口或评分策略后，建议执行 `python scripts\evaluate_retrieval.py --write-report` 检查回归结果。
- 如果新增了 grounded answer 约束或证据规则，建议额外执行 `python scripts\evaluate_grounded_answer.py --write-report`。
