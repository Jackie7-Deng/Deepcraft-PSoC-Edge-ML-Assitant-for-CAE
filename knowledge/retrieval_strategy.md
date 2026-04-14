# PSoC Edge DeepCraft AI 检索策略

**更新日期**: 2026-03-31  
**定位**: 规定本地知识库优先的检索顺序，以及何时、如何触发 Community / Case 外部搜索。

---

## 1. 默认模式：本地知识库优先

1. 先区分 **PSoC Edge E8x** 与 **PSoC 6 / CY8CKIT-062S2-AI**。
2. 先走 `knowledge/`：`overview.md`、`document_map.md`、`faq.md`、`parameters_catalog.md`、`troubleshooting_playbook.md`。
3. 再走一级证据：`docs/readmes/README_*.md`、`docs/**/*.pdf`、`ingest/html/*.md`、示例工程源码。
4. 只有当本地证据不足，或用户明确要求查 Community / Case 现场经验时，才进入 MCP 外部搜索。

> 原则：Community / Case 是补充证据，不是官方规格来源。

## 2. 本地优先的入口选择

| 问题类型 | 第一入口 | 第二入口 |
|----------|----------|----------|
| 平台区分 / 总览 | `knowledge/overview.md` | `knowledge/examples_catalog.md` |
| 参数 / 版本 / 工具链 | `knowledge/parameters_catalog.md` | `docs/readmes/README_*.md`、`knowledge/summary_mtb_ml_user_guide.md` |
| 编译 / 烧录 / 导入失败 | `knowledge/troubleshooting_playbook.md` | 目标 README、`knowledge/index_kit_guide.md` |
| ML 部署 / 模型替换 | `knowledge/ml_workflow.md` | `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md`、DEEPCRAFT 部署 README |
| Face ID / Vision / Camera | `knowledge/examples_catalog.md` | `docs/readmes/README_Machine_Learning_Face_ID_Demo.md`、`README_DEEPCRAFT_Deploy_Vision.md` |
| 外部搜索 / 社区经验 | 本文件 | `knowledge/community_digest.md` |

## 3. 三轮关键词扩展策略

该策略与 `scripts/search_utils.py` 保持一致，适用于 Community / Case 搜索前的 query rewrite。

> 核心要求：**不要把用户原句整段直接丢进搜索框。**

### 第一轮：芯片词 / Demo 名称 + 主症状词

优先组合：
- 芯片 / 平台词：`PSoC Edge`、`PSoC 6`、`KIT_PSE84_EVAL`、`CY8CKIT-062S2-AI`
- Demo / 场景词：`Face ID`、`MTBML Deploy`、`DEEPCRAFT Deploy Vision`、`DEEPCRAFT Data Collection`
- 主症状词：`build failed`、`programming failed`、`wrong prediction`、`low accuracy`

示例：
- `PSoC Edge Face ID build failed`
- `PSoC 6 MTBML wrong prediction`

### 第二轮：补充工具链词 / ML 框架词

在第一轮不够准时，再补：
- 工具链词：`ModusToolbox`、`GCC_ARM`、`KitProg3`、`OpenOCD`
- ML 框架词：`Imagimob`、`MTBML`、`TensorFlow Lite`、`TFLM`、`NPU`
- memory / converter 词：`memory placement`、`SMIF`、`XIP`、`tensor arena`、`Model Converter`

示例：
- `PSoC Edge Face ID build failed GCC_ARM`
- `PSoC 6 MTBML wrong prediction Imagimob`

### 第三轮：补充平台词 / 外设词

若还需要缩小范围，再补：
- 平台词：`Windows 11`、`Ubuntu`、`VS Code`
- 外设词：`camera`、`OV7675`、`PDM microphone`、`IMU`、`USB camera`、`DSI display`
- 版本词：`ModusToolbox 3.6`、`ModusToolbox 3.7`

示例：
- `PSoC Edge Face ID build failed GCC_ARM Windows 11`
- `PSoC Edge camera inference failed OV7675`

## 4. PSoC Edge 专属搜索优先级

在构造 query 或人工阅读搜索结果时，默认按下面顺序判断：

1. **先查 ML 框架词**：先确认问题属于 `Imagimob`、`MTBML`、`DEEPCRAFT`、`TFLM`、`NPU` 哪条链。
2. **再查症状词**：编译失败、烧录失败、推理错误、精度低、摄像头无画面、Face enrolment 失败等。
3. **最后补工具链词**：`ModusToolbox`、`GCC_ARM`、`LLVM_ARM`、`KitProg3`、`OpenOCD`。

这样可以先把问题归入正确的 ML / 部署链，再避免被通用构建噪声结果带偏。

## 5. 问题压缩与链路式搜索

- 如果用户说的是“去搜索此问题”，先从当前上下文压出短 query，再搜
- 外部搜索不应只有一次请求，而应更像工程师调试：
  1. 先搜最短 query
  2. 看最相关的 2~3 条
  3. 读正文
  4. 归纳共性
  5. 必要时再改写下一轮 query

## 6. 什么时候触发外部搜索

默认以**手动触发为主**，典型条件如下：

- 用户明确要求查 community / case / 历史经验
- 本地 README、PDF、网页镜像都没有覆盖到该症状
- 需要补现场经验、兼容性边角问题、已知缺陷绕行路径
- 需要核对是否已有相似 case / 社区帖子可以复用给客户

如果本地已经有充分证据，应优先直接回答，而不是先去搜外部网页。

## 7. `search -> select -> read` 分离

- `community_search` / `case_search`：只负责结果列表
- `community_read_article` / `case_read`：只负责读正文
- 读到外部正文后，先摘要成：
  - 问题
  - 现象
  - 调试过程
  - 解决建议
  - 未决项

## 8. 组合式防循环

- 同一 query / URL 最多重复访问 2~3 次
- 如果自动化真的需要展开链接，单轮最多打开 10~20 个
- search / read 都应受 timeout 限制
- 连续 3~5 次没有拿到新证据时停止

## 9. 词表维护说明

- 词表主文件：`scripts/search_utils.py`
- 当新增板卡、示例、模型名、框架名、工具链名时，应优先补进对应 term 列表。
- 如果项目从旧领域迁移过来，必须先清除旧领域默认词（如 USB Serial / FX3 / CX3 旧词），避免把旧经验污染到新检索。
- Community / Case 搜索后，如果某条经验高频复用，应沉淀回：
  - `knowledge/community_digest.md`
  - `knowledge/faq.md`
  - `knowledge/troubleshooting_playbook.md`

## 10. 与 MCP 的配合边界

- `.vscode/mcp.json` 负责把浏览器型 MCP Server 接入当前工作区。
- `mcp_servers/infineon_browser_server.py` 负责统一暴露 Community / Case 工具。
- `scripts/community_search_playwright.py` 继续保留网络层拦截方案（`page.on("response")`），避免退回脆弱的 DOM 解析。
- 如果外部搜索不可用，应先记录障碍，再回退到本地知识与已沉淀的 `community_digest.md`。
- 若问题已经落到本机 ModusToolbox 安装或 pack 状态，可按需进入 `C:\Users\DengJi\ModusToolbox\`，但默认不要把该路径当作全量知识库。
