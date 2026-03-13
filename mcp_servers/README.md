# MCP 检索服务说明

本目录用于放置当前工作区可直接落地的 MCP 服务。

## 当前服务

- `vector_search_server.py`：提供结构化 RAG 与符号检索能力

## 提供的工具

- `semantic_search`
- `symbol_search`
- `get_faq`
- `get_parameters`
- `get_troubleshooting`
- `get_index_status`
- `grounded_answer`

`semantic_search` 现支持附加过滤参数：

- `source_types`
- `path_prefix`
- `platform_tags`
- `tool_tags`
- `doc_classes`
- `evidence_tiers`

`grounded_answer` 用于高风险问答或客户回复草拟。它不会直接替你生成最终回答，而是返回：

- 查询改写后的证据检索计划
- 当前是否满足最少引用条数
- 推荐使用的本地证据
- 必须遵守的回答约束

## 本地自检

```powershell
python mcp_servers\vector_search_server.py --self-test
```

## 运行前提

先执行：

```powershell
python scripts\init_kb.py
python scripts\build_vector_index.py
python scripts\evaluate_retrieval.py --write-report
python scripts\evaluate_grounded_answer.py --write-report
```

## 运行方式说明

- 对支持 MCP 的宿主来说，通常由宿主在调用工具时**自动启动** `vector_search_server.py` 这个本地子进程，不需要用户长期手动开一个后台服务。
- 如果某个客户端不支持自动托管本地 MCP 子进程，则需要该客户端自己的 MCP 配置流程；这不是当前仓库脚本本身的限制。
