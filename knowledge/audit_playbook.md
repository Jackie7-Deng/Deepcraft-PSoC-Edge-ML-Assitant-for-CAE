# 审计操作手册

> 创建日期: 2026-03-08
> 用途: 可重复执行的知识库审计检查清单

---

## 1. 文件完整性审计

### 1.1 PDF 文档检查
```bash
# 检查 PDF 文件是否存在
ls -la docs/datasheets/*.pdf
ls -la docs/trm_aum/*.pdf
ls -la docs/application_notes/*.pdf
ls -la docs/kit_guides/*.pdf
```

**预期结果**：
- [ ] `docs/datasheets/psoc_edge_e8x_datasheet.pdf` 存在
- [ ] `docs/trm_aum/psoc_edge_e8x_architecture_rm.pdf` 存在
- [ ] `docs/trm_aum/psoc_edge_e8x_registers_rm.pdf` 存在
- [ ] `docs/application_notes/ml_modustoolbox_imagimob.pdf` 存在
- [ ] `docs/application_notes/mtb_ml_user_guide.pdf` 存在
- [ ] `docs/kit_guides/kit_pse84_eval_user_guide.pdf` 存在

### 1.2 Markdown 文档检查
```bash
# 检查 knowledge 目录
ls -la knowledge/*.md

# 检查 ingest 目录
ls -la ingest/html/*.md

# 检查 README 归档
ls -la docs/readmes/*.md
```

**预期结果**：
- [ ] `knowledge/` 目录包含 15+ 个 .md 文件
- [ ] `ingest/html/` 目录包含 10+ 个抓取的页面
- [ ] `docs/readmes/` 目录包含 15 个 README 文件

---

## 2. 元数据完整性审计

### 2.1 README YAML 头检查
每个 README 文件应包含 YAML 头部:

```yaml
---
title: <项目标题>
category: <类别>
subcategory: <子类别>
target_hardware: <目标硬件>
tags: [tag1, tag2, ...]
summary: |
  中文摘要
---
```

**审计命令**:
```powershell
# 检查所有 README 是否有 YAML 头
Get-ChildItem docs\\readmes\\README_*.md | ForEach-Object {
  $firstLine = Get-Content $_.FullName -TotalCount 1
  if ($firstLine -eq '---') {
    Write-Output \"✅ $($_.Name) has YAML header\"
  } else {
    Write-Output \"❌ $($_.Name) missing YAML header\"
  }
}
```

### 2.2 HTML 抓取文件检查
每个抓取的 HTML 文件应包含:
- `source_url`: 原始 URL
- `fetched_at`: 抓取日期
- `title`: 页面标题
- `tags`: 标签数组

**审计命令**:
```powershell
# 检查 HTML 文件的 YAML 头
Get-ChildItem ingest\\html\\*.md | ForEach-Object {
  if (Select-String -Path $_.FullName -Pattern 'source_url:' -Quiet) {
    Write-Output \"✅ $($_.Name) has source_url\"
  } else {
    Write-Output \"❌ $($_.Name) missing source_url\"
  }
}
```

---

## 3. 内容覆盖度审计

### 3.1 主题覆盖矩阵

| 主题 | PDF 覆盖 | Web 覆盖 | 代码示例 |
|------|----------|----------|----------|
| NPU/ML 加速 | ✅ TRM | ✅ edge_api.md | ✅ Face_ID_Demo |
| TFLM 部署 | ✅ ML User Guide | ✅ deploy_model*.md | ✅ MTBML_Deploy |
| 音频处理 | ✅ Voice Assistant | ✅ data_collection.md | ✅ Audio_Enhancement |
| 视觉/相机 | - | ✅ code_gen_vision.md | ✅ Deploy_Vision |
| 传感器 | ✅ Kit Guide | ✅ psoc_edge_e84_ai_kit.md | ✅ Data_Collection |
| 图形/GPU | - | ✅ graph_ux.md | ✅ LVGL_Demo |

### 3.2 关键函数/概念覆盖

**必须覆盖的概念**:
- [ ] IMAI_Init, IMAI_enqueue, IMAI_dequeue (Edge API)
- [ ] Tensor Arena 配置
- [ ] Vela 编译器
- [ ] Int8 量化
- [ ] Streaming Protocol v2
- [ ] Graph UX 数据采集

---

## 4. 链接有效性审计

### 4.1 内部链接检查
```powershell
# 简化版内部链接检查：优先人工复核 document_map 和 examples_catalog 中的重要链接
Get-Content knowledge\\document_map.md -TotalCount 120
Get-Content knowledge\\examples_catalog.md -TotalCount 120
```

### 4.2 外部 URL 检查
```powershell
# 检查 fetch_audit.json 中的 URL 状态
Get-Content ingest\\fetch_audit.json -TotalCount 120
```

---

## 5. 网页失败项审计

检查 `ingest/url_missing.txt` 与 `ingest/fetch_audit.json`：
- [ ] 所有失败 URL 已记录
- [ ] 每条失败原因已写清
- [ ] `fetch_audit.json` 中的失败状态与 `url_missing.txt` 一致

---

## 6. 审计报告生成

### 6.1 自动生成脚本
```powershell
$pdfCount = (Get-ChildItem docs -Recurse -Filter *.pdf -ErrorAction SilentlyContinue).Count
$mdCount = (Get-ChildItem . -Recurse -Filter *.md -ErrorAction SilentlyContinue).Count
$htmlCount = (Get-ChildItem ingest\\html -Filter *.md -ErrorAction SilentlyContinue).Count
$readmes = Get-ChildItem docs\\readmes\\README_*.md -ErrorAction SilentlyContinue
$withYaml = @($readmes | Where-Object { (Get-Content $_.FullName -TotalCount 1) -eq '---' }).Count

Write-Output \"# 审计报告\"
Write-Output \"- PDF 文档: $pdfCount\"
Write-Output \"- Markdown 文档: $mdCount\"
Write-Output \"- HTML 抓取: $htmlCount\"
Write-Output \"- README 总数: $($readmes.Count)\"
Write-Output \"- README 含 YAML: $withYaml\"
```

### 6.2 手动检查项
- [ ] 自检 Q&A 全部通过 (`knowledge/audit_selftest_qna.md`)
- [ ] 失败 URL 记录完整 (`ingest/url_missing.txt`)
- [ ] 示例目录最新 (`knowledge/examples_catalog.md`)
- [ ] 文档地图准确 (`knowledge/document_map.md`)

---

## 7. 审计频率建议

| 审计类型 | 频率 | 负责人 |
|----------|------|--------|
| 文件完整性 | 每月 | 自动 |
| 404 链接检查 | 每周 | 自动 |
| 内容覆盖度 | 每季度 | 人工 |
| 元数据完整性 | 每次更新后 | 自动 |

---

## 8. 问题追踪

发现问题后，记录到 `knowledge/audit_issues.md`:

```markdown
| 日期 | 问题描述 | 严重程度 | 状态 | 解决日期 |
|------|----------|----------|------|----------|
| YYYY-MM-DD | 描述 | 高/中/低 | 开放/已解决 | YYYY-MM-DD |
```

---

*最后更新: 2026-03-08*
