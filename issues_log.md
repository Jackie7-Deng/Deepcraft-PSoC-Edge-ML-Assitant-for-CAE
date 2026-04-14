# Issues Log

## Open

### ISSUE-001 宿主未自动接入仓库 MCP server
- **状态**: open
- **影响**: 无法直接通过宿主侧 MCP tools 验证，只能脚本直跑
- **当前处理**: 通过 `run_mcp_regression.py` + Playwright 脚本做回归

### ISSUE-002 Case discussion “Load all / Load more” 不稳定
- **状态**: open
- **影响**: 某些 Case 只能提到 header/summary，拿不到完整讨论链
- **当前处理**: 保留为已知限制；优先记录问题和已有摘要

### ISSUE-005 Community 搜索对官方文档/产品页偏置
- **状态**: open
- **影响**: 宽 query 虽能返回结果，但前排不一定是 community 经验帖，导致经验沉淀效率下降
- **当前处理**: 已在 `community_search_playwright.py` 和 `search_utils.py` 中加入 source-aware score；后续仍需继续优化 query 扩词

### ISSUE-006 Memory 资源限制类 Case query 仍过泛
- **状态**: open
- **影响**: `PSoC machine learning RAM flash size limitation` 一类问题仍可能命中营销/下载主题，Case 相关性不足
- **当前处理**: 已修复 query 变体优先级，优先跑原始 seed query，并避免退化成单一宽词；但仍需继续补 memory-specific 症状词和资源约束词

### ISSUE-008 回归期间存在 Node `DEP0169 url.parse()` 噪声
- **状态**: open
- **影响**: 不阻塞搜索，但会污染回归日志，降低可观测性可读性
- **当前处理**: 先登记为已知问题；后续可切换到 WHATWG URL API 或压制第三方依赖的 warning

### ISSUE-009 Community 长帖结构化摘要仍偏粗
- **状态**: open
- **影响**: `community_read_article` 已能输出 `summary`，但复杂长帖仍可能把原问题大段带入 `phenomena` / `resolution_hint`，摘要可读性一般
- **当前处理**: 已增加标题优先、论坛噪声清理、去除对原问题的复读；后续仍需补做 role-aware 分段和问答式摘要

### ISSUE-010 长自然语言 query 压缩后仍可能缺少症状提示
- **状态**: resolved
- **影响**: 已避免把中文整句直接送进 Community / Case，但当前压缩结果仍可能只剩 `PSoC Edge DEEPCRAFT Model Converter` 这种宽 query，导致结果偏产品页或总览页
- **当前处理**: 已补中英文症状/格式 hint 提取；当前压缩结果可生成 `PSoC Edge DEEPCRAFT Model Converter error`、`PSoC Edge DEEPCRAFT Model Converter error model format`

### ISSUE-011 Case 顶层 query 字段语义不一致
- **状态**: resolved
- **影响**: `queries_tried` 已是压缩后的英文短 query，但顶层 `query` 仍可能回显用户原始自然语言，容易让上层误判为脚本仍在直接搜整句
- **当前处理**: 已统一改为顶层 `query` 返回实际 seed query，并把原始输入放到 diagnostics.`original_input`

## Resolved

### ISSUE-003 新增 memory 文档未纳入知识链
- **状态**: resolved
- **处理**: 新建 `knowledge/memory_layout_guide.md`，并更新 document map / FAQ / 参数 / 排障入口

### ISSUE-004 缺少 MCP 回归与可观测文档
- **状态**: resolved
- **处理**: 新建 regression suite、observability 说明和回归执行器

### ISSUE-007 缺少 5+5 固定回归执行记录
- **状态**: resolved
- **处理**: 已生成 `governance/mcp_regression_events.jsonl` 和 `governance/mcp_regression_last_run.json`，本轮结果为 10/10 通过
