# DEEPCRAFT Ready Model 资料目录

**更新日期**: 2026-03-25  
**定位**: 汇总当前工作区内与 DEEPCRAFT Ready Models 相关的本地 PDF、网页镜像、许可页面与部署入口，作为回答申请方式、收费口径、测试路径、商业部署与板卡落地问题的统一入口。

---

**常见检索问题**:

- `Factory Alarm Detection` / `Factory Alarm detection` / `Factory Alarms and Sirens`
- `Gesture Recognition Ready Model`
- `Siren Detection Ready Model`
- `Ready Model 收费`
- `Ready Model 申请方式`
- `Ready Model PSoC 6 部署`
- `Ready Model PSoC Edge 部署`

## 1. 当前 Ready Model 证据链由哪些部分组成

| 层级 | 位置 | 用途 |
|------|------|------|
| 本地 PDF 报告 | `docs/ready_model_notes/*.pdf` | 本地归档的 Ready Model 测试报告原件 |
| 网页主入口 | `ingest/html/deepcraft-ready-models.md` | Ready Models 总览、模型列表、申请入口 |
| 网页测试入口 | `ingest/html/deepcraft-ready-models_testing-using-precompiled-binary-hex-files.md`、`ingest/html/deepcraft-ready-models_testing-using-static-library-custom-application.md` | 预编译 hex 验证与静态库集成路径 |
| 许可 / 收费 | `ingest/html/legal_licensing-metrics-and-fees.md` | 免费口径、3000 compute minutes、按需服务 |
| 深层导航 | `knowledge/deepcraft_web_catalog.md`、`knowledge/deepcraft_web_backfill_20260310.md` | 网页 Ready Models 主题导航 |

## 2. 当前本地已归档的 8 份 Ready Model 报告

| 模型 | 类型 | 本地 PDF |
|------|------|----------|
| Baby Cry Detection | 音频 | `docs/ready_model_notes/DEEPCRAFT Ready Model for Baby Cry Detection test report.pdf` |
| Cough Detection | 音频 | `docs/ready_model_notes/DEEPCRAFT Ready Model for Cough Detection test report.pdf` |
| Direction of Arrival (audio) | 音频 | `docs/ready_model_notes/DEEPCRAFT Ready Model for Direction of Arrival (audio) test report.pdf` |
| Factory Alarm Detection | 音频 | `docs/ready_model_notes/DEEPCRAFT Ready Model for Factory Alarm Detection test report.pdf` |
| Fall Detection | 运动 / IMU | `docs/ready_model_notes/DEEPCRAFT Ready Model for Fall Detection test report.pdf` |
| Gesture Recognition | 雷达 | `docs/ready_model_notes/DEEPCRAFT Ready Model for Gesture Recognition test report.pdf` |
| Siren Detection | 音频 | `docs/ready_model_notes/DEEPCRAFT Ready Model for Siren Detection test report.pdf` |
| Snore Detection | 音频 | `docs/ready_model_notes/DEEPCRAFT Ready Model for Snore Detection test report.pdf` |

## 3. 与网页镜像的对应关系

- Ready Models 总览页列出了 Baby Cry、Cough、Direction of Arrival、Factory Alarm、Siren、Snore、Gesture、Fall 等模型，并给出了对应测试报告链接。`ingest/html/deepcraft-ready-models.md`
- Ready Models 的验证路径分成两条：
  - 预编译 binary / hex，面向快速上板验证，当前本地证据明确覆盖 `PSOC 6 AI Evaluation Kit`。`ingest/html/deepcraft-ready-models_testing-using-precompiled-binary-hex-files.md`
  - 静态库接入自定义应用，适合已有固件工程继续集成。`ingest/html/deepcraft-ready-models_testing-using-static-library-custom-application.md`
- 许可页面给出了当前本地口径：Studio 开发 / 测试 / 评估免费，含每月 3000 compute minutes；在 Infineon MCU / NPU 上的生产和商业部署免费；专家服务 / 更多算力 / SLA 按需联系。`ingest/html/legal_licensing-metrics-and-fees.md`

## 4. 板卡与部署入口怎么对应

### 4.1 PSoC 6 / CY8CKIT-062S2-AI

- 当前本地网页镜像明确给出了 Ready Model `.hex` 快速验证路径。`ingest/html/deepcraft-ready-models_testing-using-precompiled-binary-hex-files.md`
- 若要接入自己的应用，可走静态库方式，并参考 `README_mtb-example-ml-imagimob-mtbml-deploy` 这类 PSoC 6 ML 工程。`docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md`

### 4.2 PSoC Edge E84

- 当前本地网页镜像明确列出了 PSoC Edge 的 `Deploy Model: Audio / Motion / Radar` 示例入口。`ingest/html/deepcraft-studio_deployment_deploy-models-supported-boards_deploy-model-PSOC-6-PSOC-Edge.md`
- 当前本地 README 也明确了 E84 的数据采集与部署示例入口，其中音频模型可挂到 `mtb-example-psoc-edge-ml-deepcraft-deploy-audio` 这一类工程。`docs/readmes/README_DEEPCRAFT_Data_Collection.md`
- 对于音频类 Ready Models（如 Factory Alarm / Siren / Baby Cry / Snore），当前更稳妥的知识路径是：先看本目录页，再结合网页的静态库集成说明与 PSoC Edge Audio Deploy 示例来回答。  

## 5. 当前检索与引用边界

- 当前索引链 **不会直接抽取 PDF 正文**；`docs/ready_model_notes/*.pdf` 主要通过本目录页进入检索结果。
- 如果只是要回答“有没有这个模型 / 叫什么 / 怎么申请 / 收费如何 / 走哪条部署路径”，优先从本页和网页镜像回答。
- 如果要给出更强证据，尤其是性能指标、测试条件、混淆矩阵或特定阈值，应再打开对应 PDF 原件补页码。若当前知识库未抽取该页内容，应明确写 `未在当前知识库找到依据`。

## 6. 推荐使用顺序

1. 先看 `knowledge/ready_models_catalog.md`，判断模型是否已被本地归档。
2. 再看 `ingest/html/deepcraft-ready-models.md`，确认官方网页总览与申请入口。
3. 若涉及测试方式，继续看：
   - `ingest/html/deepcraft-ready-models_testing-using-precompiled-binary-hex-files.md`
   - `ingest/html/deepcraft-ready-models_testing-using-static-library-custom-application.md`
4. 若涉及收费、评估、商业部署，再看 `ingest/html/legal_licensing-metrics-and-fees.md`
5. 若涉及具体模型表现，再回到 `docs/ready_model_notes/*.pdf` 对应原件。
