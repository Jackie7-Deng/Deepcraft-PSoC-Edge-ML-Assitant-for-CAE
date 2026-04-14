# Lightweight Index Chunk Schema

## 顶层字段

- `index_version`
- `built_at_utc`
- `root`
- `include_pdfs`
- `chunk_count`
- `file_count`
- `files_indexed`
- `chunks`

## `chunks[]` 字段

| 字段 | 说明 |
|------|------|
| `chunk_id` | 稳定块 ID |
| `source_path` | 相对路径 |
| `source_type` | `knowledge/init/config/pdf/code/tooling/other` |
| `title` | heading 或 PDF page title |
| `anchor` | `heading:*` / `page-*` / `lines:*` |
| `text` | chunk 正文 |
| `chunk_index` | 源文件内块序号 |
| `page` | PDF 页码，可空 |
| `start_line` / `end_line` | 文本文件行号，可空 |
| `keywords` | 提取关键词 |
| `content_hash` | chunk 内容 hash |
| `source_mtime_utc` | 源文件 mtime，ISO UTC |
