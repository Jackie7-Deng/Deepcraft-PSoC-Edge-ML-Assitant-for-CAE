# DEEPCRAFT 网页知识目录

**更新日期**: 2026-03-10  
**定位**: 统一说明当前工作区中 DEEPCRAFT 官网网页资料的权威入口、抓取状态与推荐检索顺序。

---

## 1. 当前权威源已经切换到 `ingest/urls_checked.txt`

- 本轮网页整链融合以 `ingest/urls_checked.txt` 为**唯一权威检查清单**。
- 本轮明确**不回头审核**旧的 101 个 404 URL canonical 映射修正；相关历史讨论不再作为本轮工作的基准。
- 当前 `ingest/` 已收敛为 checked 清单、成功清单、失败清单、抓取审计与原始镜像五类核心资产。
- 当前统计：checked URL 130 条，唯一 URL 129 条；成功 128 条，失败 2 条；本轮实际写入 `ingest/html/*.md` 127 个文件。

## 2. 当前网页知识的四层结构

| 层级 | 位置 | 当前职责 |
|------|------|----------|
| 权威 URL 清单层 | `ingest/urls_checked.txt` | 当前人工审核后的基准清单；后续网页抓取、审计、知识摘要都以它为准 |
| 原始镜像层 | `ingest/html/*.md` | 保存本轮成功抓取页面的可回溯镜像，统一带 YAML front matter |
| 抓取审计层 | `ingest/fetch_audit.json`、`ingest/url_success.txt`、`ingest/url_missing.txt` | 记录每个 checked URL 的成功/失败状态、HTTP 码、输出文件与失败原因 |
| 知识摘要 / 导航层 | `knowledge/deepcraft_web_backfill_20260310.md`、`knowledge/retrieval_guide.md`、`knowledge/document_map.md` | 提供低 token 的主题总结、入口导航与检索策略 |
| 治理层 | `governance/CURRENT_STATUS.md`、`governance/ASSISTANT_TRAINING_AUDIT_LOG.md` | 记录当前权威源、覆盖率、保留缺口与维护口径 |

## 3. 本轮覆盖到的网页主题

| 主题 | 成功页数 |
|------|----------|
| 安装与入门 | 21 |
| 部署 | 13 |
| 数据准备 | 42 |
| 预处理 | 1 |
| 训练 | 5 |
| 评估 | 6 |
| 代码生成 | 4 |
| 其他界面 | 1 |
| 教程 | 6 |
| 排障 | 4 |
| Model Converter | 14 |
| Ready Models | 3 |
| Legal | 8 |

> 说明：`deployment/edge-api` 在 `urls_checked.txt` 中出现 2 次，因此成功 URL 数 (128) 与实际写入 html 文件数 (127) 相差 1 个。

## 4. 推荐检索顺序

1. 先看 `knowledge/deepcraft_web_catalog.md`，确认该问题属于哪个网页主题。
2. 再看 `knowledge/deepcraft_web_backfill_20260310.md`，获取按主题压缩后的总结。
3. 若要确认当前页面是否成功抓到，查看 `ingest/url_success.txt` 或 `ingest/url_missing.txt`。
4. 若需要逐条状态、重试次数、redirect、输出文件，查看 `ingest/fetch_audit.json`。
5. 若需要回溯网页正文，再进入 `ingest/html/*.md` 对应镜像文件。
6. 若问题属于 Ready Models，且需要结合本地 PDF 测试报告，优先转到 `knowledge/ready_models_catalog.md`。

## 5. 本轮抓取结果与边界

- 以 checked URL 计覆盖率：98.5%
- 以唯一 URL 计覆盖率：98.4%
- 当前仅剩 2 条 checked URL 失败：
  - `https://developer.imagimob.com/deepcraft-studio/getting-started/accelerators`
  - `https://developer.imagimob.com/deepcraft-studio/getting-started/project-templates`
- 这 2 条在现站点直接返回 404，因此保留在 `ingest/url_missing.txt` 与 `ingest/fetch_audit.json` 中。
- 本轮**不再回头处理**旧 URL 清单 / 旧 404 映射逻辑，回答网页问题时应优先信任 `urls_checked.txt` 这一新基线。

## 6. 使用时要注意什么

- `ingest/html/` 现已清理为**仅保留当前 checked 基线成功抓取到的 127 个镜像文件**。
- 需要证据时优先引用本轮新刷新的镜像文件；需要快速回答时优先使用 `knowledge/deepcraft_web_backfill_20260310.md` 的主题总结。
- 如果用户问哪些 URL 这轮没抓到，直接看 `ingest/url_missing.txt`。
