# 模板差距分析

## 对照范围

对照 `GENERIC_SPECIALIZED_QA_ASSISTANT_TEMPLATE.md` 的第 4、5、6、7、10、13、14 节。

## 本轮发现的主要差距

1. **治理层缺失**
   - 缺 `TODO.md`、`issues_log.md`、`knowledge_governance.md`
2. **轻量 RAG 交付不完整**
   - 缺 `indexes/chunk_schema.md`
   - 缺显式的 `rag_regression.md`
3. **MCP 稳定性保障不完整**
   - 缺 `mcp_regression_suite.md/json`
   - 缺 `mcp_observability.md`
   - 缺统一执行器 `run_mcp_regression.py`
4. **证据仲裁规则未显式化**
   - 缺 `knowledge/evidence_scoring.md`
   - 缺 `scripts/evidence_arbitrator.py`
5. **新增 memory 资料未进入知识链**
   - 缺专门的 memory / linker / XIP 二级知识页

## 本轮补齐动作

- 新建 `knowledge/memory_layout_guide.md`
- 新建 `knowledge/code_map.md`
- 新建 `knowledge/evidence_scoring.md`
- 新建 `TODO.md`、`issues_log.md`、`knowledge_governance.md`
- 新建 `mcp_regression_suite.md/json`、`mcp_observability.md`、`run_mcp_regression.py`
- 新建 `indexes/chunk_schema.md`、`rag_regression.md`
- 增强 `scripts/search_utils.py`、`community_search_playwright.py`、`case_search_playwright.py`、`lightweight_rag.py`

## 尚未完全闭环的项

- 宿主侧 MCP client 自动注册仍不在仓库可控范围内
- Case discussion 深层抽取还需继续增强
- 版本兼容矩阵仍未形成单独专题
