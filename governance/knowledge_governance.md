# 知识治理规则

## 1. 资料分层

1. **一级证据层**：官方 PDF、README、源码、原始 Community/KBA/Case
2. **二级知识层**：`knowledge/*.md`
3. **三级经验层**：community digest、case 摘要、`【推断/经验】`

## 2. 优先级

`官方 PDF / 源码 > 官方 README > 本地知识页 > Community/KBA/Case > 推断`

## 3. 回灌规则

1. 新外部证据先进入 `community_digest.md`
2. 去重后再回灌 `faq.md` / `troubleshooting_playbook.md` / `parameters_catalog.md`
3. 回灌时必须保留来源 URL 或 Case 编号

## 4. 冲突处理

1. 若官方 PDF 与 community 冲突，以官方 PDF 为准
2. 若知识页与原始证据冲突，先修知识页
3. 若版本不一致，显式写出适用范围

## 5. 缺口处理

- 没有证据时不输出精确参数
- 优先把缺口改写成“还需要哪份资料 / 哪个命令输出”
- 推断内容必须标 `【推断/经验】`
