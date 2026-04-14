# 专属助手训练审计日志

**更新日期**: 2026-03-25  
**目标工作区**: `PSoC_Edge_DeepCraft_AI`  
**审计基准**: `GENERIC_SPECIALIZED_QA_ASSISTANT_TEMPLATE.md`

## 1. 历史基线（已完成）

工作区此前已经完成初始化层、路由层、结构化知识入口、检索层与治理层的基础搭建，包括：

- `CLAUDE.md` / `AGENTS.md` / `.github/copilot-instructions.md` 等初始化入口
- `.claude/skills/` 与 `prompts/` 等路由层
- `knowledge/overview.md`、`knowledge/document_map.md`、`knowledge/faq.md` 等结构化知识入口
- `indexes/`、`scripts/semantic_search.py`、`mcp_servers/vector_search_server.py` 等检索层
- `memory/` 与 `governance/` 等治理层

## 2. 本轮新增审计目标：DEEPCRAFT 官网网页整链融合

本轮的新增要求不是简单补抓网页，而是把 checked URL 对应内容从原始镜像层  抓取审计层  知识摘要 / 导航层  治理层全部打通，并明确切换权威源。

### 2.1 本轮关键决策

- 不再回头审核旧 101 个 404 canonical 映射修正。
- `ingest/urls_checked.txt` 成为当前唯一权威 URL 基线。
- 维护类文档继续统一为中文。

### 2.2 本轮完成的代码与产物更新

- 重写 `scripts/refresh_html_mirror.py`
  - 输入改为 `ingest/urls_checked.txt`
  - 输出增加 `ingest/url_success.txt` 与 `ingest/url_missing.txt`
  - `fetch_audit.json` 中为每个 checked URL 写入独立记录
  - 成功页面统一刷新到 `ingest/html/*.md`
- 更新网页知识入口链：
  - `knowledge/deepcraft_web_catalog.md`
  - `knowledge/deepcraft_web_backfill_20260310.md`
  - `knowledge/retrieval_guide.md`
  - `knowledge/overview.md`
  - `knowledge/document_map.md`
- 更新治理层：
  - `governance/CURRENT_STATUS.md`
  - `governance/ASSISTANT_TRAINING_AUDIT_LOG.md`

### 2.3 本轮抓取结果

- checked URL 总数：130
- 唯一 URL 数：129
- 成功数：128
- 失败数：2
- 实际写入 html 文件：127
- 覆盖率（checked）：98.5%
- 覆盖率（unique）：98.4%
- 重复 URL：`https://developer.imagimob.com/deepcraft-studio/deployment/edge-api`（在 checked 清单中出现 2 次）

### 2.4 本轮剩余失败项

本轮仅保留 2 条真实失败项，且都已记录到 `ingest/url_missing.txt` 与 `ingest/fetch_audit.json`：

- `https://developer.imagimob.com/deepcraft-studio/getting-started/accelerators`
- `https://developer.imagimob.com/deepcraft-studio/getting-started/project-templates`

### 2.5 审计结论

当前工作区的网页知识体系已经从旧 URL 清单 + 零散网页总结升级为checked 权威清单 + 可追踪抓取审计 + 可复核镜像层 + 低 token 摘要层 + 治理层同步的状态。

这意味着后续回答 DEEPCRAFT 官网网页类问题时，已经可以稳定遵循以下顺序：

1. `ingest/urls_checked.txt` 确认范围  
2. `ingest/fetch_audit.json` / `url_success.txt` / `url_missing.txt` 确认状态  
3. `ingest/html/*.md` 回溯原文  
4. `knowledge/deepcraft_web_backfill_20260310.md` 输出低 token 总结  
5. `governance/*.md` 记录当前口径与覆盖率

## 3. 本轮额外清理与整顿

- 删除旧 URL 清单、旧发现清单、旧对比清单等过渡抓取文件
- 删除早期已被新链路替代的审计 stub / 验收 / 交付类中间文档
- 将维护流程文档统一改写到 `urls_checked.txt -> refresh_html_mirror.py -> fetch_audit/url_success/url_missing -> indexes` 这一新链路
- 将旧 `fetch_deepcraft.py` 路径从维护流程中移除，避免继续误用

## 4. 对照模板后仍可提升的点

- 仍缺少可量化的检索评测集与问答回归集
- 仍缺少显式 reranker、query rewrite、分层摘要索引
- 仍缺少针对网页 / README / PDF / 示例工程的统一 metadata 过滤策略
- 仍可继续补充 README 与网页中提到、但当前仓库未收录的外部资料

## 5. 本轮新增审计目标：接入 ModusToolbox 工具链知识与 RAG P1/P2

本轮新增目标分成两部分：

1. 将 `docs/MTB_docs/` 下三份 ModusToolbox 指南接入到 `knowledge/` 与 `governance/` 主链，避免助手只会回答 DEEPCRAFT 训练侧，而不会回答工程侧工具链问题。
2. 对当前本地 RAG 继续做基础增强：补充回归评测样例、metadata 标签过滤与更自然的 chunk 切分，为后续 rerank / query rewrite 打基础。

### 5.1 MTB 工具链知识链接入

- 新增 `knowledge/modustoolbox_tools_summary.md`
  - 汇总 `device-configurator.pdf`
  - 汇总 `infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf`
  - 汇总 `New-to-ModusToolbox.pdf`
- 更新知识入口：
  - `knowledge/overview.md`
  - `knowledge/document_map.md`
  - `knowledge/faq.md`
  - `knowledge/ml_workflow.md`
  - `knowledge/troubleshooting_playbook.md`
  - `knowledge/parameters_catalog.md`
  - `knowledge/retrieval_guide.md`
  - `knowledge/workspace_inventory.md`

### 5.2 本轮完成的 RAG P1/P2

- 在 `scripts/rag_index_lib.py` 中新增 metadata 提取：
  - `doc_class`
  - `evidence_tier`
  - `platform_tags`
  - `tool_tags`
  - `domain_tags`
- 将 chunk 切分从固定步长滑窗增强为优先贴近自然空行 / 小节边界的切分策略
- 新增 `evals/retrieval_cases.json` 检索回归样例
- 新增 `scripts/evaluate_retrieval.py` 检索回归执行脚本
- 扩展 `scripts/semantic_search.py` 与 MCP `semantic_search`，支持 metadata 过滤

### 5.3 为什么本轮优先做到 P1/P2，而不是直接跳到完整 P3/P4

- P1/P2 解决的是“有没有基础度量、有没有 metadata、切分是否明显失真”这些底座问题
- 如果没有评测集和 metadata，直接做显式 reranker、LLM 级 query rewrite 或更强的生成约束，很难判断改动是否真的提升
- 因此本轮采取的策略是：
  - **先落地低风险、高收益的基础能力**
  - **再为 P3/P4 留出可验证的升级接口**

### 5.4 本轮顺手带入的 P3/P4 邻接增强

虽然没有完整落地显式 reranker 或回答级 citation validator，但本轮仍带入了两类低风险增强：

- 扩展了 `DOMAIN_SYNONYMS`，加入 ModusToolbox / Device Configurator / BSP / 编译器等术语
- 在 metadata 评分中加入 query 与 chunk 标签重合加成，作为轻量级的“metadata-aware rerank”

### 5.5 本轮后仍保留的提升空间

- 仍缺少更强的模型级 query rewrite / 子问题分解
- 仍缺少回答阶段的自动 citation validator
- 仍缺少更系统的多级摘要索引

## 6. 本轮新增审计目标：实现完整版 P3/P4 并补用户入口

本轮进一步完成两件事：

1. 把 RAG 从“有基础检索能力”推进到“有查询改写、显式 rerank、grounded answer 与回答约束”的状态。
2. 把用户入口补全为“根目录 README + usage_guide + 初始化镜像”，让使用边界更清晰。

### 6.1 本轮新增的 RAG P3/P4 产物

- `scripts/grounded_answer.py`
- `scripts/evaluate_grounded_answer.py`
- `evals/grounded_answer_cases.json`
- `README.md`

### 6.2 本轮新增的实现点

- 在 `scripts/rag_index_lib.py` 中新增：
  - 查询改写
  - 查询意图识别
  - 显式 rerank
  - grounded answer 证据包
- 在 `mcp_servers/vector_search_server.py` 中新增：
  - MCP 工具 `grounded_answer`
- 在 `scripts/semantic_search.py` 中新增：
  - `--with-plan`
  - rerank 与匹配词输出

### 6.3 本轮文档链更新

- 更新 `knowledge/usage_guide.md`
- 新增根目录 `README.md`
- 更新 `knowledge/retrieval_guide.md`
- 更新 `knowledge/document_map.md`
- 更新 `knowledge/overview.md`
- 更新初始化镜像：`CLAUDE.md`、`.claude/CLAUDE.md`、`AGENTS.md`、`.github/copilot-instructions.md`

### 6.4 本轮验证结果

- 执行 `python scripts\update_kb.py`：通过
- 执行 `python scripts\verify_ingest.py`：通过
- 执行 `python scripts\evaluate_retrieval.py --write-report`：通过
- 当前索引摘要：
  - `file_count=417`
  - `chunk_count=5587`
  - `symbol_count=14245`
  - `token_count=32711`
- 当前检索回归结果：
  - `total_cases=8`
  - `hit_count=8`
  - `hit_rate=100%`
- 当前 grounded answer 约束评测：
  - `total_cases=4`
  - `ok_count=4`
  - `ok_rate=100%`

## 7. 本轮新增审计目标：整理 README 摆放并接入 Ready Model 本地证据

本轮新增目标聚焦两个问题：

1. 清理根目录大量示例 `README_*.md` 与 `docs/readmes/` 并存造成的导航混乱。
2. 将新加入的 `docs/ready_model_notes/` 8 份 Ready Model PDF，以及 `docs/机器震动异常检测模型训练指南.md` 接入知识主链与检索链。

### 7.1 本轮完成的整理动作

- 删除根目录已归档的示例 `README_*.md`，保留根目录门面 `README.md`
- 统一知识文档中示例 README 的引用入口到 `docs/readmes/README_*.md`
- 新增 `knowledge/ready_models_catalog.md`
- 在 `knowledge/document_map.md`、`knowledge/overview.md`、`knowledge/retrieval_guide.md`、`knowledge/usage_guide.md`、`knowledge/examples_catalog.md` 中接入 Ready Model 主链
- 在 `knowledge/deepcraft_web_backfill_20260310.md` 与 `knowledge/deepcraft_web_catalog.md` 中补充本地 Ready Model PDF 导航关系
- 将 `docs/机器震动异常检测模型训练指南.md` 接入导航与示例链

### 7.2 本轮检索链增强

- 在 `scripts/rag_index_lib.py` 中为以下概念补充了查询同义词扩展：
  - `ready model`
  - `factory alarm detection`
  - `收费`
  - `申请`
  - `量产`
- 为 Ready Model 相关查询增加了轻量级路径 rerank：
  - 优先提升 `knowledge/ready_models_catalog.md`
  - 提升 `ingest/html/deepcraft-ready-models*.md`
  - 提升 `ingest/html/legal_licensing-metrics-and-fees.md`

### 7.3 当前验证结果

- 执行 `python scripts\update_kb.py`：通过
- 执行 `python scripts\verify_ingest.py`：通过
- 执行 `python scripts\evaluate_retrieval.py --write-report`：通过
- 执行 `python scripts\evaluate_grounded_answer.py --write-report`：通过
- 当前索引摘要：
  - `file_count=405`
  - `chunk_count=5446`
  - `symbol_count=14121`
  - `token_count=33144`
- 当前检索回归结果：
  - `total_cases=8`
  - `hit_count=8`
  - `hit_rate=100%`
- 当前 grounded answer 约束评测：
  - `total_cases=4`
  - `ok_count=4`
  - `ok_rate=100%`

### 7.4 本轮后仍保留的真实缺口

- `docs/ready_model_notes/*.pdf` 目前仍未做页级正文抽取，检索主要通过 `knowledge/ready_models_catalog.md` 间接接入。
- 对 `Factory Alarm Detection Ready Model 收费 / 申请 / 部署` 这类复合查询，当前排序已明显改善，但结果前列仍可能先出现网页测试页，再出现目录页；后续仍可继续做更细粒度的 query intent routing。
