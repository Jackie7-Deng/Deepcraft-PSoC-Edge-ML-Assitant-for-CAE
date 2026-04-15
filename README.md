# PSoC Edge + DEEPCRAFT 专属助手工作区

**更新日期**: 2026-04-15  
**定位**: 这是给人类使用者看的工作区入口页，帮助你快速理解这个专属助手已经具备什么能力、怎么提问、什么时候需要维护索引或配置 MCP。

## 1. 这是什么

这是一个围绕 **Infineon PSoC Edge + DEEPCRAFT Studio** 搭建的专属 AI 助手工作区。  
它不是单纯的资料堆，而是一套已经接通了：

- 角色初始化层
- 技能路由层
- 结构化知识层
- 本地 RAG / 检索层
- 网页抓取与审计层
- 治理与使用说明层

的完整知识系统。

## 2. 你可以直接怎么用

### 2.1 普通用户最简单的用法

如果你是用 **Copilot / Claude / 其他支持仓库级初始化文件与本地工具的 Agent** 进入这个工作区，通常你只需要直接用自然语言提问，例如：

- “PSoC Edge 和 PSoC 6 的部署假设能混用吗？”
- “为什么新环境编不过，可能和 `CY_COMPILER_ARM_DIR` 有关吗？”
- “DEEPCRAFT 生成代码后怎么接到 ModusToolbox 工程？”
- “当前权威的 DeepCraft 网页 URL 清单是什么？”

对这类自然语言问题，用户**不需要自己手动写检索命令**。

对 **VS Code Copilot**，当前工作区的主初始化入口是：

- `.github/copilot-instructions.md`（自动随工作区加载）
- `.github/instructions/external-search.instructions.md`（当任务涉及 community / case / MCP / 外部检索时按需发现）

对偏好 `CLAUDE.md` / `AGENTS.md` 的代理，则继续使用根目录初始化文件。

### 2.2 用户需不需要自己启动 RAG 后台服务

通常**不需要**。

- 普通问答场景下，用户只要提问即可。
- 本地 RAG 索引已经存放在 `indexes/`，由 agent 在需要时调用。
- 只有在你新增了资料、刷新了网页镜像、或者维护了知识文件之后，维护者才需要执行：

```powershell
python scripts\update_kb.py
python scripts\verify_ingest.py
```

### 2.3 MCP 服务需不需要客户手动运行

通常也**不需要长期手动开一个后台进程**。

- 对支持 MCP 的宿主，`mcp_servers\vector_search_server.py` 一般由宿主在调用工具时自动拉起。
- 如果某个客户端本身不支持自动托管本地 MCP 子进程，则需要该客户端自己的 MCP 配置流程。
- 换句话说：**是否需要手动启动 MCP，更取决于客户端能力，而不是当前仓库脚本本身。**

当前与治理 / 回归相关的文档统一放在 `governance/`，避免根目录混乱。

## 3. 当前已经实现了什么

### 3.1 角色与知识链

- 根初始化：`CLAUDE.md`
- 兼容镜像：`.claude/CLAUDE.md`、`AGENTS.md`、`.github/copilot-instructions.md`
- 全局导航：`knowledge/document_map.md`
- 一页纸总览：`knowledge/overview.md`
- 高频问答：`knowledge/faq.md`
- 工具链摘要：`knowledge/modustoolbox_tools_summary.md`
- 版本兼容：`knowledge/version_compatibility_guide.md`
- AI Kit 文档入口：`knowledge/index_ai_kit_guide.md`
- 使用手册：`knowledge/usage_guide.md`
- Ready Model 报告目录：`knowledge/ready_models_catalog.md`

### 3.2 本地 RAG

- 结构化 chunk 索引：`indexes/text_chunks.jsonl`
- 符号索引：`indexes/symbol_index.json`
- 轻量向量与倒排：`indexes/vector_db/`
- CLI 检索入口：`scripts/semantic_search.py`、`scripts/symbol_search.py`
- 回答证据包：`scripts/grounded_answer.py`
- MCP 服务：`mcp_servers/vector_search_server.py`

### 3.3 网页知识链

- 权威 URL 清单：`ingest/urls_checked.txt`
- 成功 / 失败清单：`ingest/url_success.txt`、`ingest/url_missing.txt`
- 抓取审计：`ingest/fetch_audit.json`
- 原始镜像：`ingest/html/*.md`
- 摘要导航：`knowledge/deepcraft_web_catalog.md`、`knowledge/deepcraft_web_backfill_20260310.md`

## 4. 推荐先读哪里

- 快速理解整个系统：`knowledge/overview.md`
- 不知道问题该去哪里：`knowledge/document_map.md`
- 想知道如何提问：`knowledge/usage_guide.md`
- 想查 Ready Model 申请、收费、测试报告：`knowledge/ready_models_catalog.md`
- 想了解检索链：`knowledge/retrieval_guide.md`
- 想知道当前真实状态：`governance/CURRENT_STATUS.md`

## 5. 如果你是维护者

新增资料或修改知识后，建议执行：

```powershell
python scripts\update_kb.py
python scripts\verify_ingest.py
python scripts\evaluate_retrieval.py --write-report
python scripts\evaluate_grounded_answer.py --write-report
```

如果你修改了 MCP 搜索链或外部检索规则，建议再执行：

```powershell
python run_mcp_regression.py
```

## 6. 结论

- **`knowledge/usage_guide.md` 不是这个工作区的门面 README，而是更偏“用户使用手册”。**
- **本文件 `README.md` 是工作区总入口。**
- 两者关系是：
  - `README.md`：先告诉你这是什么、怎么开始
  - `knowledge/usage_guide.md`：再告诉你具体怎么问、怎么维护、怎么理解 RAG / MCP 的使用边界
