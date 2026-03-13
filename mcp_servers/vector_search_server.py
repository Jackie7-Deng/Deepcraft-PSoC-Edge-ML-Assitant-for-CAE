#!/usr/bin/env python3
"""PSoC Edge + DEEPCRAFT 结构化 RAG MCP 服务。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from rag_index_lib import (
    INDEX_SUMMARY_PATH,
    VECTOR_META_PATH,
    build_grounded_answer_pack,
    load_json,
    rel_path,
    search_chunks,
    search_symbols,
    ROOT,
)

SERVER_INFO = {
    "name": "psoc-edge-deepcraft-rag",
    "version": "1.0.0",
}

def format_text_result(data: Any) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False, indent=2)}]}

def list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "semantic_search",
            "description": "执行结构化混合检索，适合中文自然语言问题、近义词查询和跨文档召回。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 8},
                    "source_types": {"type": "array", "items": {"type": "string"}},
                    "path_prefix": {"type": "string"},
                    "platform_tags": {"type": "array", "items": {"type": "string"}},
                    "tool_tags": {"type": "array", "items": {"type": "string"}},
                    "doc_classes": {"type": "array", "items": {"type": "string"}},
                    "evidence_tiers": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["query"],
            },
        },
        {
            "name": "symbol_search",
            "description": "查找函数、宏、类或 Markdown 标题。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_faq",
            "description": "在 FAQ 中做定向召回。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_parameters",
            "description": "在参数目录中做定向召回。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_troubleshooting",
            "description": "在排障手册中做定向召回。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_index_status",
            "description": "查看当前索引和向量库状态。",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "grounded_answer",
            "description": "生成带回答约束的证据包，适合高风险问答、客户回复和需要严格引用的场景。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 6},
                    "min_citations": {"type": "integer", "default": 2},
                    "source_types": {"type": "array", "items": {"type": "string"}},
                    "path_prefix": {"type": "string"},
                    "platform_tags": {"type": "array", "items": {"type": "string"}},
                    "tool_tags": {"type": "array", "items": {"type": "string"}},
                    "doc_classes": {"type": "array", "items": {"type": "string"}},
                    "evidence_tiers": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["query"],
            },
        },
    ]

def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "semantic_search":
        data = search_chunks(
            query=arguments["query"],
            top_k=int(arguments.get("top_k", 8)),
            source_types=arguments.get("source_types"),
            path_prefix=arguments.get("path_prefix"),
            platform_tags=arguments.get("platform_tags"),
            tool_tags=arguments.get("tool_tags"),
            doc_classes=arguments.get("doc_classes"),
            evidence_tiers=arguments.get("evidence_tiers"),
        )
        return format_text_result(data)
    if name == "symbol_search":
        data = search_symbols(arguments["query"], top_k=int(arguments.get("top_k", 10)))
        return format_text_result(data)
    if name == "get_faq":
        data = search_chunks(arguments["query"], top_k=int(arguments.get("top_k", 5)), path_prefix="knowledge\\faq.md")
        return format_text_result(data)
    if name == "get_parameters":
        data = search_chunks(arguments["query"], top_k=int(arguments.get("top_k", 5)), path_prefix="knowledge\\parameters_catalog.md")
        return format_text_result(data)
    if name == "get_troubleshooting":
        data = search_chunks(arguments["query"], top_k=int(arguments.get("top_k", 5)), path_prefix="knowledge\\troubleshooting_playbook.md")
        return format_text_result(data)
    if name == "get_index_status":
        data = {
            "workspace": rel_path(ROOT),
            "index_summary": load_json(INDEX_SUMMARY_PATH, {}),
            "vector_meta": load_json(VECTOR_META_PATH, {}),
        }
        return format_text_result(data)
    if name == "grounded_answer":
        data = build_grounded_answer_pack(
            query=arguments["query"],
            top_k=int(arguments.get("top_k", 6)),
            min_citations=int(arguments.get("min_citations", 2)),
            source_types=arguments.get("source_types"),
            path_prefix=arguments.get("path_prefix"),
            platform_tags=arguments.get("platform_tags"),
            tool_tags=arguments.get("tool_tags"),
            doc_classes=arguments.get("doc_classes"),
            evidence_tiers=arguments.get("evidence_tiers"),
        )
        return format_text_result(data)
    return {"isError": True, "content": [{"type": "text", "text": f"未知工具: {name}"}]}

def write_message(payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()

def read_message() -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in {b"\r\n", b"\n"}:
            break
        key, value = line.decode("utf-8").split(":", 1)
        headers[key.strip().lower()] = value.strip()
    content_length = int(headers.get("content-length", "0"))
    if content_length <= 0:
        return None
    body = sys.stdin.buffer.read(content_length)
    return json.loads(body.decode("utf-8"))

def handle_message(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    msg_id = message.get("id")
    params = message.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": list_tools()}}
    if method == "tools/call":
        result = call_tool(params.get("name", ""), params.get("arguments", {}))
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"pong": True}}
    if msg_id is None:
        return None
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unsupported method: {method}"},
    }

def self_test() -> None:
    payload = {
        "tools": [tool["name"] for tool in list_tools()],
        "sample_search": search_chunks("如何部署视觉模型到 PSoC Edge", top_k=3),
        "sample_grounded": build_grounded_answer_pack("GeneratedSource 为什么不能删除", top_k=3),
        "sample_symbols": search_symbols("IMAI_Init", top_k=3),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))

def main() -> None:
    parser = argparse.ArgumentParser(description="PSoC Edge + DEEPCRAFT MCP 检索服务")
    parser.add_argument("--self-test", action="store_true", help="执行本地自检")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    while True:
        message = read_message()
        if message is None:
            break
        response = handle_message(message)
        if response is not None:
            write_message(response)

if __name__ == "__main__":
    main()
