# DEEPCRAFT 网页补抓回填说明（以 `urls_checked.txt` 为基准）

**更新日期**: 2026-03-10  
**本轮权威源**: `ingest/urls_checked.txt`  
**抓取结果**: checked URL 130 条 / 唯一 URL 129 条 / 成功 128 条 / 失败 2 条 / 实际写入 html 127 个

---

## 1. 本轮口径

- 本轮以 `ingest/urls_checked.txt` 作为人工审核后的权威 URL 清单。
- 本轮不回头审核旧的 101 个 404 canonical 映射修正，直接以 checked 清单逐条访问现站点。
- 成功页面已覆盖写入 `ingest/html/*.md`，失败页面写入 `ingest/url_missing.txt`，详细状态写入 `ingest/fetch_audit.json`。
- 旧的 URL 发现清单、历史对比清单与过渡产物已经移除，不再作为当前知识链输入。

## 2. 本轮成功覆盖的主题摘要

### 2.1 安装 / 入门 / Graph UX / 开发板

本轮成功抓到 21 个入门相关页面，形成了从安装、概念入门到板卡接入的完整入口链：

- `install-download-studio` 明确了 Studio 的注册、邮件确认、下载安装流程，并特别提醒**不要以管理员权限运行安装程序**。
- `release-notes` 记录了 5.9 版本的重要变化，包括：高采样率/多特征轨道录制时可通过隐藏轨道改善时间轴性能、Node Explorer 新增搜索能力、YOLOv8n 目标检测训练入口。
- `graph-ux` 与 `graph-ux-overview` 说明 Graph UX 是以节点图方式串起数据、预处理、训练、评估和代码生成的交互入口。
- `starter-models-project-templates` 系列成为当前可访问的模板/加速器替代入口，补足了 Starter Models、Project Template 等新路径。
- `infineon-boards`、`other-boards`、`tensor-streaming-protocol` 系列把 PSoC Edge E84 AI Kit / Eval Kit、Infineon AI Evaluation Kit、PSoC 6 Wi-Fi Pioneer Kit，以及 Protocol v1 / 自定义固件烧写路径串起来，适合回答该用哪块板、怎么流数据、怎么接自定义固件这类问题。

### 2.2 数据准备 / 数据采集 / 预处理

本轮成功抓到 42 个数据准备页面和 1 个预处理页面，已经覆盖从采集、导入、标注、分布到增强的主链路：

- `data-collection` 主链把 Infineon 板卡采集、无板卡采集、Graph UX 采集都补齐了；子页面进一步细分了麦克风、IMU、磁力计、压力、湿度、雷达、多传感器等具体采集场景。
- `bring-your-data`、`bring-your-own-data`、`bring-your-own-data-object-detection` 说明了分类/回归与目标检测项目导入自有数据的路径差异。
- `add-data-to-project` 与 `add-project-object-detection` 说明已有项目如何继续加数据。
- `data-labeling`、`manual-labeling`、`ml-assisted-labeling`、`add-label`、`label-image-data` 覆盖了手工标注、模型辅助标注、图像标注与标签维护。
- `data-distribution`、`manage-labels`、`multiple-tracks` 进一步补齐数据集划分、标签管理、多轨数据组织。
- `data-augmentation` 给出了明确限制：**当前只支持 16 KHz 单声道音频增强**，并列出音量调整、模拟距离、添加背景声三类增强方式，同时强调增强文件与原始文件要保持同一数据集以防数据泄漏。
- `preprocessing` 说明数据分布之后需要配置 preprocessor track，并将预处理作为训练前的独立阶段。

### 2.3 训练 / 评估

本轮成功抓到 5 个训练页面、6 个评估页面，形成了从训练发起到多类评估方法的闭环：

- `model-training`、`generating-model`、`starting-tracking-training-jobs` 说明 Studio 的训练任务由云端执行，并支持自动化模型生成与训练任务追踪。
- `download-import-model-files` 说明训练完成后如何下载模型文件并把预测结果回导到项目中。
- `training-object-detection` 与 release notes 中的 YOLOv8n 入口相互印证，表明目标检测训练已纳入当前工作流。
- `model-evaluation` 和其子页覆盖 confusion matrix、可解释性（Window Visualization / Grad-CAM）、Graph UX 在线评估、回归评估、目标检测评估，适合回答怎么评价分类/回归/检测模型效果、如何做可解释性分析这类问题。

### 2.4 代码生成 / 部署 / Edge API

本轮成功抓到 4 个代码生成页面和 13 个部署页面，已经把训练完成后怎么落到 MCU/NPU这部分补齐：

- `code-gen-infineon-boards`、`code-gen-vision-models`、`code-gen-aurix-other-dev-boards` 把 PSoC 6 / PSoC Edge、视觉模型、AURIX / TRAVEO / XMC7200 / 其他开发板的代码生成路径分别说明清楚。
- `code-generation-using-graph-ux` 说明在 Graph UX 中可以从图工作流直接生成部署代码。
- `deployment`、`deploy-models-supported-boards`、`deploy-models-other-boards` 以及各个板卡子页，补齐了 Siren Detection、PSoC 6 / PSoC Edge、Vision model、AURIX、T2G、XMC7200 等落地路径。
- `custom-layers-functions` 与 `supported-layers` 说明可扩展层与受支持层/函数范围。
- `deployment/edge-api` 给出了生成代码后的关键接口说明：`model.c` / `model.h`、`IMAI_Init()`、`IMAI_enqueue()`、`IMAI_dequeue()` 以及带/不带时间戳的 Queue API 变体，是当前回答生成代码后固件如何调用模型的关键证据页。

### 2.5 教程 / 排障 / FAQ

本轮成功抓到 6 个教程页面与 4 个排障/FAQ 页面：

- Siren Detection 教程完整覆盖了数据准备、预处理、训练、部署四个步骤，适合作为 end-to-end 教学样例。
- 风机发电预测教程补充了一个非声学的回归型业务例子。
- `troubleshooting`、`installer-issues`、`data-collection-issues` 说明了安装卡死、PowerShell 环境、时间轴卡顿等常见问题的处理路径。
- `frequently-asked-questions` 则沉淀了混合模拟/数字数据、时间戳、构建条件等高频问题。

### 2.6 DEEPCRAFT Model Converter

本轮成功抓到 14 个 Model Converter 页面，已经把这条子产品线基本补齐：

- 主入口说明 Model Converter 可把 `.h5`、`.tflite`、`.pt2` 模型转为可部署的 `model.c` / `model.h`，面向 PSOC 6、PSOC Edge M55+U55、PSOC Edge M33+NNLite。
- GUI / CLI 两条工作流都围绕**生成代码  量化优化  桌面验证**三阶段展开。
- `supported-model-formats` 明确：**Keras 3 暂不支持**、需要 Keras 2 `.h5`；PyTorch 侧要求 **`torch==2.6.0+`** 导出 `.pt2`；量化支持 Int8x8 与 Int16x8（PyTorch 仅 Int8x8）。
- `deploy-model-using-code-example`、`supported-data-formats`、`supported-layers-operators`、`container-setup` 为集成、输入数据格式、支持算子范围与容器化环境提供了配套入口。
- `troubleshooting/lstm` 与 `troubleshooting/arena-memory` 把 LSTM 性能退化与 tensor arena 内存不足问题沉淀成了可复用经验。

### 2.7 Ready Models

本轮成功抓到 3 个 Ready Models 页面：

- Ready Models 被定义为可直接接入边缘设备的 production-ready AI/ML 模型。
- 一条路径是使用预编译 binary / hex 文件快速上板验证。
- 另一条路径是导入静态库并接入自定义应用，适合已有固件工程继续集成。

### 2.8 Legal / 合规

本轮成功抓到 8 个 Legal 页面：

- `legal` 入口汇总了评估许可、Studio 条款、费用、Model Converter 协议、隐私、FOSS、Ultralytics 许可等页面。
- `licensing-metrics-and-fees` 明确当前口径下：**Studio 开发/测试/评估免费，包含每月 3000 compute minutes；在 Infineon MCU / NPU 上的生产和商业部署也免费**；更高算力、专家服务、SLA 等为按需联系。
- 其余协议页则为后续回答许可、隐私、第三方软件责任边界提供直接入口。

## 3. 本轮失败项

本轮仅有以下 2 条 checked URL 失败，且均为现站点直接 404：

- `https://developer.imagimob.com/deepcraft-studio/getting-started/accelerators`
- `https://developer.imagimob.com/deepcraft-studio/getting-started/project-templates`

处理方式：

- 已写入 `ingest/url_missing.txt`
- 已在 `ingest/fetch_audit.json` 中逐条记录 `status`、`http_code`、`reason`
- 本轮不再对这 2 条旧路径继续做 canonical 映射追查

## 4. 这份回填文档怎么用

1. 先看本文件，快速获取按主题压缩后的网页知识。  
2. 需要确认页面是否真的抓到：查 `ingest/url_success.txt` / `ingest/url_missing.txt`。  
3. 需要原文证据：去 `ingest/html/*.md`。  
4. 需要逐条抓取状态与输出文件：查 `ingest/fetch_audit.json`。  
5. 需要全局入口：回到 `knowledge/deepcraft_web_catalog.md`。
