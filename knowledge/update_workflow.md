# 知识库更新工作流

> 创建日期: 2026-03-08
> 用途: 可持续的知识库维护流程

---

## 1. 日常更新流程

### 1.1 新增 DEEPCRAFT 文档
当 DEEPCRAFT 官方文档更新时：

```powershell
# 步骤 1：人工整理并确认权威 URL 清单
# 编辑 ingest\\urls_checked.txt

# 步骤 2：执行整链刷新
python scripts\\refresh_html_mirror.py

# 步骤 3：检查成功 / 失败清单
Get-Content ingest\\url_success.txt -TotalCount 40
Get-Content ingest\\url_missing.txt -TotalCount 40

# 步骤 4：更新索引与校验
python scripts\\run_ingest_pipeline.py

# 步骤 5：如新增主题，补写 knowledge\\deepcraft_web_backfill_20260310.md
```

### 1.2 新增 PDF 文档
当收到新的 PDF 文档时：

```text
# 步骤 1：确定 PDF 类型
# - Datasheet → docs/datasheets/
# - TRM/AUM → docs/trm_aum/
# - Application Note → docs/application_notes/
# - Kit Guide → docs/kit_guides/

# 步骤 2：重命名文件（规范化）
# 在资源管理器或 PowerShell 中移动到 docs\\<category>\\normalized_name.pdf

# 步骤 3：创建索引文件
# knowledge/index_<document>.md

# 步骤 4：更新 document_map.md
# 添加新文档条目

# 步骤 5：更新 workspace_inventory.md
# 添加到文件清单
```

### 1.3 新增示例代码
当有新的 ModusToolbox 示例时：

```powershell
# 步骤 1：复制 README 到归档目录
Copy-Item "C:\\path\\to\\new\\example\\README.md" "docs\\readmes\\README_<New_Example>.md"

# 步骤 2：添加 YAML 头
# 参考现有 README 格式

# 步骤 3：更新 examples_catalog.md
# 添加新示例条目

# 步骤 4：检查关联文档
# 确保相关知识点已覆盖
```

---

## 2. 周度维护任务

### 2.1 链接有效性检查
```bash
# 检查失败链接
python -c "
import json
with open('ingest/fetch_audit.json') as f:
    audit = json.load(f)
    for _, info in audit.get('fetch_status', {}).items():
        if info.get('status') != 'success':
            print(f'❌ {info.get(\"source_url\")}: {info.get(\"reason\", \"unknown\")}')
"

# 查看失败清单
Get-Content ingest\\url_missing.txt -TotalCount 80
```

### 2.2 文档一致性检查
- [ ] `workspace_inventory.md` 文件计数与实际一致
- [ ] `document_map.md` 路径有效
- [ ] `examples_catalog.md` 链接可访问

---

## 3. 月度审计任务

### 3.1 完整性审计
运行 `audit_playbook.md` 中的所有检查项。

### 3.2 内容更新
1. **检查 DEEPCRAFT Studio 版本更新**
   - 访问 https://developer.imagimob.com/deepcraft-studio/release-notes
   - 重新运行 `python scripts\\refresh_html_mirror.py`

2. **检查 ModusToolbox 版本**
   - 确认所有示例的 ModusToolbox 版本号
   - 更新过时的版本信息

3. **检查硬件更新**
   - 新的开发板型号
   - 新的传感器支持

### 3.3 生成审计报告
```powershell
# 运行自动审计
New-Item -ItemType Directory -Force temp | Out-Null
# 当前工作区尚未提供正式 audit_report 脚本；建议将审计结果整理后再写回知识库
```

---

## 4. 季度深度审计

### 4.1 内容覆盖度评估
- 对照 DEEPCRAFT 官方文档目录
- 识别缺失的主题
- 规划补充内容

### 4.2 代码示例验证
- 编译验证所有示例
- 更新构建步骤
- 记录已知的编译问题

### 4.3 用户体验评估
- 运行 `audit_selftest_qna.md` 中的问题
- 确保所有问题可回答
- 更新过时的答案

---

## 5. 版本发布流程

### 5.1 发布前检查
```powershell
# 1. 完整性检查
Get-ChildItem docs\\datasheets, docs\\trm_aum, docs\\application_notes

# 2. 验证 README YAML
Get-ChildItem docs\\readmes\\README_*.md | ForEach-Object {
  python -c "import pathlib; p = pathlib.Path(r'$($_.FullName)'); txt = p.read_text(encoding='utf-8'); print('OK', p.name if txt.startswith('---') else 'MISSING', p.name)"
}

# 3. 验证 HTML 抓取
Get-Content ingest\\fetch_audit.json -TotalCount 80
```

### 5.2 版本标记
```bash
# 创建版本标签
git tag -a v1.0.0 -m "Knowledge base release 1.0.0"

# 生成变更日志
git log v0.9.0..v1.0.0 --oneline > CHANGELOG.md
```

---

## 6. 问题修复流程

### 6.1 发现问题
1. 在 `audit_issues.md` 记录问题
2. 标注严重程度
3. 分配负责人

### 6.2 修复问题
1. 创建修复分支
2. 应用修复
3. 验证修复效果
4. 合并到主分支

### 6.3 关闭问题
1. 更新 `audit_issues.md` 状态
2. 记录解决日期
3. 更新相关文档

---

## 7. 备份与恢复

### 7.1 备份策略
```bash
# 每周备份
tar -czf backup_$(date +%Y%m%d).tar.gz \
  docs/ knowledge/ ingest/ scripts/ .claude/

# 存储到远程
# scp backup_*.tar.gz user@remote:/backup/path/
```

### 7.2 恢复流程
```bash
# 恢复到特定日期
tar -xzf backup_20260301.tar.gz

# 验证恢复
./scripts/audit_report.sh
```

---

## 8. 自动化建议

### 8.1 CI/CD 集成
```yaml
# .github/workflows/audit.yml
name: 每周审计
on:
  schedule:
    - cron: '0 0 * * 0'  # 每周日
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run audit
        run: ./scripts/audit_report.sh
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: audit-report
          path: knowledge/audit_report_*.md
```

### 8.2 自动抓取
```bash
# crontab 配置
0 2 * * * cd /path/to/knowledge && python scripts/run_ingest_pipeline.py --with-fetch
```

---

*最后更新: 2026-03-08*
