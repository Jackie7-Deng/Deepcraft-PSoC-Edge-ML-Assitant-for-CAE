# 改进计划

**更新日期**: 2026-03-11
**定位**: 记录当前知识库的优先改进路线，而不是维护流程本身。

## P0
- 建立更完整的 generated-code / API 线索页
- 补充更细的排障验证案例与真实日志模式
- 继续调优当前混合检索排序，压低噪声结果并提升中文描述性问题命中率
- 为网页镜像 / README / PDF / 示例工程补更细的统一 metadata，支撑更强过滤检索
- 扩大标准回归问答集与检索评测集，覆盖更多 PSoC Edge / MTB / DEEPCRAFT 问题

## P1
- 编写路径一致性检查脚本
- 为新版本 DEEPCRAFT / MTB 更新建立固定审计流程
- 增加针对 `semantic_search` / `symbol_search` / MCP 工具的回归样例
- 为复杂问题加入 query rewrite / rerank / 分层检索策略
- 补充 README / 网页中提到但当前仓库未收录的外部资料

## 当前已完成
- 已补 `knowledge/modustoolbox_tools_summary.md`，接通 MTB 工具链知识链
- 已为检索增加基础 metadata 标签与过滤能力
- 已新增 `evals/retrieval_cases.json` 与 `scripts/evaluate_retrieval.py`
- 已把 chunk 切分调为更贴近自然边界的方式
- 已补查询改写、显式 rerank 与 grounded answer 证据包
- 已新增 `evals/grounded_answer_cases.json` 与 `scripts/evaluate_grounded_answer.py`
