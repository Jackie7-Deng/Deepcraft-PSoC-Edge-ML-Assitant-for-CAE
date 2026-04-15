# MCP Observability

## 每条回归必须落盘的字段

- `session_id`
- `case_id`
- `mode`
- `query`
- `elapsed_ms`
- `stop_reason`
- `result_count`
- `result_quality_score`
- `queries_tried`
- `top_titles`
- `error`

## Stop Reason 约定

- `results_found`
- `empty_results`
- `query_errors_only`
- `runner_exception`

## 日志位置

- `governance/mcp_regression_last_run.json`
- `governance/mcp_regression_events.jsonl`
