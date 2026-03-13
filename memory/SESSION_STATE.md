# PSoC Edge + DEEPCRAFT 助手状态面板

**更新日期**: 2026-03-11

## 当前结构状态
- 规范初始化入口已切换到根目录 `CLAUDE.md`
- `.claude/CLAUDE.md` 保留为兼容镜像
- Skills 层已补齐：主路由 / 排障 / 代码导航 / 参数查询
- Prompts 层已补齐：主提示 / 排障 / 代码导航 / 客户回复
- 全局导航入口已补齐：`knowledge/document_map.md`
- 结构化索引已落地：`indexes/text_chunks.jsonl`、`indexes/symbol_index.json`
- 轻量向量索引已落地：`indexes/vector_db/`
- MCP 检索服务已落地：`mcp_servers/vector_search_server.py`
- ModusToolbox 工具链摘要已落地：`knowledge/modustoolbox_tools_summary.md`
- 检索回归样例已落地：`evals/retrieval_cases.json`
- grounded answer 证据包已落地：`scripts/grounded_answer.py`
- grounded answer 评测已落地：`evals/grounded_answer_cases.json`
- 当前审计日志位于：`governance/ASSISTANT_TRAINING_AUDIT_LOG.md`
- 后续新增维护类文档默认使用中文

## 当前已知缺口
- 语义检索排序仍可继续调优
- 更强的模型级 query rewrite / 多级摘要索引仍未完成
- 自动 citation validator 仍未完成
- 一致性检查脚本仍可继续增强
- 部分知识页仍有继续精炼空间
- 抓取脚本与抓取审计之间仍需进一步校验一致性
