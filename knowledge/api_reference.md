# API 入口导览

**更新日期**: 2026-03-10
**定位**: 当前工作区的 API / 集成入口导览页，用来告诉助手应该先去哪里找接口线索，而不是伪造完整 SDK 手册。

---

## 1. MTB ML / 生成代码入口

| 场景 | 优先位置 | 说明 |
|------|----------|------|
| 模型生成代码 | `mtb_ml_gen/`（位于示例工程内） | 用于查看生成模型、arena 建议与推理入口 |
| 示例推理代码 | `Machine_Learning_Imagimob_MTBML_Deploy/source/` | 用于查看集成方式与调用模式 |
| Face ID 应用代码 | `PSOC_Edge_Machine_Learning_Face_ID_Demo/application_code/` | 用于查看 PSoC Edge 视觉示例入口 |

## 2. 先看哪类文档

- `docs/application_notes/mtb_ml_user_guide.pdf`：TFLM / MTB ML 使用说明
- `docs/application_notes/ml_modustoolbox_imagimob.pdf`：DEEPCRAFT / Imagimob 到 ModusToolbox 的流程
- `knowledge/ml_workflow.md`：工作流摘要
- `knowledge/examples_catalog.md`：示例与路径导航

## 3. 当前边界

- 本文件是接口入口导航，不是完整 SDK API 字典
- 若用户问到具体函数签名，而当前知识库没有直接依据，应明确写：`未在当前知识库找到依据`
- 后续相关维护类文档默认使用中文编写
