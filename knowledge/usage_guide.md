# 助手使用说明

**更新日期**: 2026-03-25  
**定位**: 给人类使用者看的完整使用手册。相比根目录 `README.md`，这里更详细地说明提问方式、RAG / MCP 使用边界、维护动作与推荐路径。

## 1. 当前专属助手已经能做什么

### 1.1 普通问答能力

- 学习路线与阅读顺序建议
- 文档 / README / 示例工程导航
- PSoC Edge / PSoC 6 平台边界区分
- DEEPCRAFT / Imagimob 工作流解释
- ModusToolbox / BSP / Device Configurator / Makefile 工程问题解释
- 部署与排障问题分诊
- 带证据的客户回复草稿

### 1.2 当前已经实现的 RAG 能力

- 结构化 chunk 切分
- 符号索引
- 轻量向量 + 倒排混合检索
- 中文/英文混合 tokenization
- 同义词扩展
- metadata 标签过滤（平台 / 工具链 / 文档类别 / 证据层级）
- 查询改写
- 显式 rerank
- grounded answer 证据包
- 检索回归评测与 grounded answer 约束评测

## 2. 用户应该怎么提问

### 2.1 默认方式：直接自然语言提问

是的，**默认就应该直接用自然语言提问**。

例如：

- “PSoC Edge 和 PSoC 6 可以混用同一套部署假设吗？”
- “为什么新环境编译失败，可能是编译器路径问题吗？”
- “DEEPCRAFT 生成代码后怎么接到 ModusToolbox 工程？”
- “Device Configurator 到底负责什么？”
- “当前 DeepCraft 网页知识是从哪些 URL 来的？”

用户**不需要先自己运行检索命令**，也不需要先自己挑知识文件。

### 2.2 如果你愿意提供更多上下文，会更稳

最好补充：

- 平台（PSoC Edge / PSoC 6）
- 板卡 / BSP
- ModusToolbox 版本
- DEEPCRAFT 版本
- 工程路径或示例名
- 模型信息、量化、NPU 状态
- 日志、报错、截图

## 3. 一旦进入工作区，角色和知识链是怎么被拿到的

### 3.1 角色定义

当前工作区已经把角色定义写进：

- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `prompts/main.md`

这意味着：

- **支持仓库初始化文件的 Agent**，进入工作区后通常会直接获得角色、边界和回答规则。
- **不支持自动读取仓库初始化文件的工具**，仍可以通过 `prompts/main.md` 获得手动提示入口。

### 3.2 知识逻辑链

知识链已经被整理成：

1. `knowledge/document_map.md`：全局导航
2. `knowledge/overview.md`：系统总览
3. `knowledge/*.md`：结构化知识层
4. `ingest/`：网页原始镜像与抓取审计
5. `indexes/`：RAG 索引层
6. `governance/`：状态、审计与改进记录

所以在支持这些初始化文件和本地工具的环境中，agent 不是“从零开始猜”，而是有明确的角色和知识链路入口。

## 4. 用户需要自己运行 RAG 吗

### 4.1 普通用户

通常**不需要**。

只要你是在支持仓库初始化和本地工具的 agent 环境中使用这个工作区，直接自然语言提问就可以。

### 4.2 维护者

当你新增 PDF、网页镜像、FAQ、README 摘要或治理文档之后，维护者应重建索引：

```powershell
python scripts\update_kb.py
python scripts\verify_ingest.py
```

如果还想确认升级没有把检索质量打坏，再运行：

```powershell
python scripts\evaluate_retrieval.py --write-report
python scripts\evaluate_grounded_answer.py --write-report
```

## 5. MCP 服务要不要手动启动

### 5.1 一般情况

一般**不需要手动长期开一个后台服务**。

`mcp_servers/vector_search_server.py` 是一个本地 MCP server，通常由支持 MCP 的宿主在需要调用工具时自动拉起。

### 5.2 什么时候可能需要手动配置

如果你使用的客户端：

- 不支持自动托管本地 MCP 子进程
- 或没有为该仓库注册 MCP server

那么你需要按该客户端自己的方式配置 MCP。  
也就是说，**MCP 需不需要你手动配，主要取决于客户端，不是因为这个仓库必须常驻一个人工维护的后台服务。**

## 6. 推荐入口

- 总入口：根目录 `README.md`
- 全局导航：`knowledge/document_map.md`
- 一页纸总览：`knowledge/overview.md`
- 高频问答：`knowledge/faq.md`
- Ready Model 报告目录：`knowledge/ready_models_catalog.md`
- ModusToolbox 工具链：`knowledge/modustoolbox_tools_summary.md`
- 参数入口：`knowledge/parameters_catalog.md`
- 排障入口：`knowledge/troubleshooting_playbook.md`
- 检索说明：`knowledge/retrieval_guide.md`

## 7. 如果你是高级使用者

### 7.1 你可以直接用检索 CLI

```powershell
python scripts\semantic_search.py "Device Configurator 在 PSoC 工程里是做什么的" --with-plan
python scripts\symbol_search.py "IMAI_Init"
python scripts\grounded_answer.py "GeneratedSource 为什么不能删除" --json
```

### 7.2 什么时候优先用 grounded answer

以下问题建议优先使用 grounded answer 证据包：

- 需要写给客户或团队的正式回答
- 高风险技术判断
- 需要严格引用
- 当前资料可能不完整，想先判断“证据够不够”

## 8. 语言约定

- 助手默认使用中文回答
- 产品名、函数名、文件名和路径可保留原始英文
- 若没有证据，助手必须明确写 `未在当前知识库找到依据`
