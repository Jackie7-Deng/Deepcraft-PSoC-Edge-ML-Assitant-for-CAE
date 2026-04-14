# 工作区资料清单

**更新日期**: 2026-04-14  
**定位**: 盘点当前工作区内可作为证据层的 `docs/` 与 `code/` 资料，并标出工作区外但可按需进入的补充路径。

---

## 1. `docs/` 总览

- 当前 `docs/` 共 `49` 个文件。
- 扩展名分布：`.md=15`、`.pdf=29`、`.brd=1`、`.DSN=1`、`.tgz=1`、`.xlsx=1`、`.zip=1`
- `docs/` 根目录当前保留 `1` 个直接文档文件。

### 1.1 `docs/` 根目录文件

- `docs/机器震动异常检测模型训练指南.md`

### 1.2 子目录清单

### `docs/application_notes/` (7 files)

- `docs/application_notes/deepcraft_voice_assistant_user_guide.pdf`
- `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf`
- `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf`
- `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf`
- `docs/application_notes/ml_modustoolbox_imagimob.pdf`
- `docs/application_notes/mtb_ml_user_guide.pdf`
- `docs/application_notes/psoc_edge_smart_glasses.pdf`

### `docs/datasheets/` (1 file)

- `docs/datasheets/psoc_edge_e8x_datasheet.pdf`

### `docs/deepcraft/` (0 files)

- 当前目录为空

### `docs/kit_guides/` (11 files)

- `docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf`
- `docs/kit_guides/kit_pse84_eval_user_guide.pdf`
- `docs/kit_guides/KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_schematic.pdf`
- `docs/kit_guides/KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_schematic.DSN`
- `docs/kit_guides/KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_Layout.pdf`
- `docs/kit_guides/KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_Layout.brd`
- `docs/kit_guides/PSOC_Edge_E84_AI_Board_assembly_drawing.pdf`
- `docs/kit_guides/PSOC_Edge_E84_AI_Board_fabrication_drawing.pdf`
- `docs/kit_guides/PSOC_Edge_E84_AI_Board_PCBA_BoM.xlsx`
- `docs/kit_guides/PSOC_Edge_E84_AI_Board_gerbers.zip`
- `docs/kit_guides/KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_ODB_files.tgz`

### `docs/MTB_docs/` (3 files)

- `docs/MTB_docs/device-configurator.pdf`
- `docs/MTB_docs/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf`
- `docs/MTB_docs/New-to-ModusToolbox.pdf`

### `docs/readmes/` (15 files)

- `docs/readmes/README_AnomalousVibrationDetection.md`
- `docs/readmes/README_Audio_Enhancement.md`
- `docs/readmes/README_DEEPCRAFT_Data_Collection.md`
- `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md`
- `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md`
- `docs/readmes/README_Device_Audio_Recorder.md`
- `docs/readmes/README_device_File_system_FreeRTOS.md`
- `docs/readmes/README_Empty_Application.md`
- `docs/readmes/README_Graphics_using_VGLite_API.md`
- `docs/readmes/README_LVGL_Smartwatch_Demo.md`
- `docs/readmes/README_Machine_Learning_Face_ID_Demo.md`
- `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md`
- `docs/readmes/README_UART_transmit_and_receive_with_DMA.md`
- `docs/readmes/README_Voice_Assistant_Deployment.md`
- `docs/readmes/README_Waveshare_Display_Driver.md`

### `docs/ready_model_notes/` (8 files)

- `docs/ready_model_notes/DEEPCRAFT Ready Model for Baby Cry Detection test report.pdf`
- `docs/ready_model_notes/DEEPCRAFT Ready Model for Cough Detection test report.pdf`
- `docs/ready_model_notes/DEEPCRAFT Ready Model for Direction of Arrival (audio) test report.pdf`
- `docs/ready_model_notes/DEEPCRAFT Ready Model for Factory Alarm Detection test report.pdf`
- `docs/ready_model_notes/DEEPCRAFT Ready Model for Fall Detection test report.pdf`
- `docs/ready_model_notes/DEEPCRAFT Ready Model for Gesture Recognition test report.pdf`
- `docs/ready_model_notes/DEEPCRAFT Ready Model for Siren Detection test report.pdf`
- `docs/ready_model_notes/DEEPCRAFT Ready Model for Snore Detection test report.pdf`

### `docs/release_notes/` (2 files)

- `docs/release_notes/mt3.6_release_notes.pdf`
- `docs/release_notes/mt3.7_release_notes.pdf`

### `docs/trm_aum/` (2 files)

- `docs/trm_aum/psoc_edge_e8x_architecture_rm.pdf`
- `docs/trm_aum/psoc_edge_e8x_registers_rm.pdf`

---

## 2. `code/` 总览

- 当前 `code/` 共 `0` 个文件。
- 扩展名分布：当前未发现已提交源码文件。
- 当前 `code/` 目录仍主要作为后续源码沉淀入口，而不是现有证据主层。

### `code/examples/` (0 files)

- 当前目录为空

### `code/generated/` (0 files)

- 当前目录为空

### `code/libs/` (0 files)

- 当前目录为空

---

## 3. 工作区外补充路径

### `C:\Users\DengJi\ModusToolbox\`

- 这是 **工作区外的补充证据路径**
- 适用问题：本机 ModusToolbox 安装、pack、manifest、compiler、tool path、生成工程或本地工具版本
- 默认不要把该路径当作全局知识库扫全量；仅当用户问题明确落到 MTB 本机环境时再进入

---

## 4. 推荐使用顺序

1. 先看 `knowledge/document_map.md` 缩小问题范围。
2. 涉及平台规格、memory、板级接口时，优先看 `docs/datasheets/`、`docs/kit_guides/`、`docs/trm_aum/`。
3. 涉及具体工程创建、构建、烧录、运行步骤时，优先看 `docs/readmes/README_*.md` 与 `docs/release_notes/*.pdf`。
4. 涉及 ML 工作流和模型部署时，优先结合 `docs/application_notes/`、`docs/readmes/`、`knowledge/ml_workflow.md` 与 `ingest/html/*.md`。
5. 若问题落到本机工具链，再按需进入 `C:\Users\DengJi\ModusToolbox\`。

---

## 5. 当前明显空位

- `docs/deepcraft/` 当前仍为空，如后续要归档更多官网导出内容，可继续回填该目录或沿用 `ingest/html/`
- `code/examples/`、`code/generated/`、`code/libs/` 当前为空，说明当前仓库仍以 README、PDF、网页镜像与示例目录为主，而不是源码归档层
- 当前虽然已经补入 `mt3.6` / `mt3.7` release notes，但仍未形成覆盖所有 BSP / ML Pack / DEEPCRAFT Studio 组合的完整兼容矩阵
