# 参数目录

**更新日期**: 2026-03-10
**定位**: 汇总部署、排障与对话分诊时最关键的参数 / 上下文字段，帮助助手知道应该追问什么、去哪里验证，以及缺失会带来什么风险。

---

## 1. 平台与工具链参数

| 参数 | 为什么重要 | 优先验证位置 | 缺失风险 |
|------|------------|--------------|----------|
| `target_platform` | 决定是否按 PSoC Edge 或 PSoC 6 路径回答 | `knowledge/examples_catalog.md`、项目路径 | 平台混淆 |
| `kit_or_bsp` | 决定板级外设与部署方式 | README、Kit Guide、项目说明 | 外设 / BSP 建议失真 |
| `target_make_var` | 决定当前构建实际落到哪个 board / kit | `Makefile`、构建命令 | 构建目标误判 |
| `toolchain` | 决定是 Arm / LLVM / GCC 哪条构建链 | `Makefile`、环境变量 | 编译问题定位偏移 |
| `modus_toolbox_version` | 影响构建、BSP、ML Pack 兼容性 | 用户描述、README | 无法判断版本差异 |
| `device_configurator_state` | 决定硬件配置是否真的有效 | `design.modus`、Notice List、GeneratedSource | 硬件配置失效 |
| `generated_source_present` | 决定 Device Configurator 输出是否进入构建 | 工程目录、构建清单 | 配置修改不生效 |
| `compiler_env_var` | 决定是否能找到编译器 | 环境变量、README | 新环境迁移后直接编译失败 |
| `deepcraft_studio_version` | 影响训练、量化、代码生成流程 | 用户描述、网页资料 | 误判工具行为 |
| `project_path_or_example` | 决定后续该读取哪个 README / 源码 | 用户描述、工作区路径 | 无法给出具体建议 |

## 2. 模型与部署参数

| 参数 | 为什么重要 | 优先验证位置 | 缺失风险 |
|------|------------|--------------|----------|
| `model_task_type` | 分类 / 检测 / 回归路径不同 | 项目说明、README | 排障路径错误 |
| `input_shape_or_resolution` | 影响内存占用与前处理 | 生成代码、项目说明 | 无法判断 arena 压力 |
| `quantization` | 影响大小、精度与性能 | 训练配置、生成文件 | 误判性能或精度 |
| `npu_enabled` | 影响 PSoC Edge 性能分析 | 平台说明、项目配置 | 误判推理路径 |
| `tensor_arena_size` | 影响初始化与运行稳定性 | 生成文件、源码常量 | 崩溃定位困难 |
| `sram_flash_usage` | 影响链接与运行稳定性 | map 文件、构建输出 | 无法判断资源瓶颈 |

## 3. 采集与运行参数

| 参数 | 为什么重要 | 优先验证位置 | 缺失风险 |
|------|------------|--------------|----------|
| `sensor_modality` | IMU / 音频 / 视觉路径完全不同 | README、用户描述 | 走错工作流 |
| `sample_rate_or_fps` | 影响前处理、模型输入和性能 | 采集配置、README | 无法复现实验 |
| `preprocessing` | 常是精度偏差根因 | 训练侧说明、源码 | 容易误判为模型问题 |
| `error_log` | 决定症状分类 | 用户提供材料 | 只能给出泛化回答 |

## 4. 快速验证入口

- 工作区导航：`knowledge/document_map.md`
- ModusToolbox 工具链：`knowledge/modustoolbox_tools_summary.md`
- 示例选择：`knowledge/examples_catalog.md`
- 工作流：`knowledge/ml_workflow.md`
- 排障：`knowledge/troubleshooting_playbook.md`
- README 归档：`docs/readmes/README_*.md`

*原则：不确定默认值时，不臆测；先要求用户提供当前配置。*

## 5. 平台能力与资源参数（基于当前本地资料）

| 参数 | 当前本地依据 | 优先验证位置 | 备注 |
|------|--------------|--------------|------|
| `e8x_npu_class` | E8x2 无 NPU、E8x3/E8x5 为 NNLite、E8x6 为 Ethos-U55 | `knowledge/summary_datasheet.md`、`docs/datasheets/psoc_edge_e8x_datasheet.pdf` | 回答前先确认具体器件，不要把 E8x6 的能力泛化到全家族。 |
| `e8x_onchip_memory` | PSoC Edge E8x 摘要写有 SRAM up to 2 MB / RRAM-Flash up to 4 MB | `knowledge/summary_datasheet.md`、`docs/datasheets/psoc_edge_e8x_datasheet.pdf` | 若用户问具体料号，请回到 datasheet。 |
| `e84_eval_external_memory` | KIT_PSE84_EVAL 索引写有 512-Mbit QSPI Flash、128-Mbit Octal RAM | `knowledge/index_kit_guide.md`、`docs/kit_guides/kit_pse84_eval_user_guide.pdf` | Face ID / Vision / Motion 的多工程 XIP 路径都与外部存储布局有关。 |
| `face_id_flash_layout` | Face ID Demo 的三个 project 都烧录到 external QSPI flash，并以 XIP 运行 | `docs/readmes/README_Machine_Learning_Face_ID_Demo.md` | 适用于 Face ID Demo，不要外推到所有 PSoC Edge 示例。 |
| `npu_peak_perf` | 【待补充：建议查阅 `docs/datasheets/psoc_edge_e8x_datasheet.pdf` 与 `docs/trm_aum/psoc_edge_e8x_architecture_rm.pdf`】 | Datasheet / Architecture RM | 当前知识库未整理出统一的 NPU 峰值吞吐数字，回答时不要臆测。 |

## 6. ML 框架与生成链参数

| 参数 | 当前本地依据 | 优先验证位置 | 备注 |
|------|--------------|--------------|------|
| `supported_model_formats` | 当前本地资料至少能确认 `.h5`、`.tflite`、`.pt2`，并可结合 ML 用户指南理解导入链 | `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#3` `docs/application_notes/mtb_ml_user_guide.pdf` | 如果用户问 BYOM / converter 输入格式，优先看新加入的 Model Converter PDF。 |
| `ml_tooling_stack` | ML Configurator、ML Model Loader、Vela Compiler | `knowledge/summary_mtb_ml_user_guide.md` | 这是工具栈，不等于所有工具在所有板卡上都默认启用。 |
| `model_converter_interfaces` | Model Converter 同时支持 GUI 与 CLI | `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#3` `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#4` | 回答“是否必须用 GUI”时不要臆测。 |
| `model_converter_targets` | 当前 PDF 直接写有 PSoC 6、PSoC Edge M33/NNLite、PSoC Edge M55/U55 | `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#3` `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#6` | 适用于当前 Model Converter 客户资料口径。 |
| `model_converter_host_os` | Windows、Linux、Mac | `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#3` `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#6` | 可回答 host OS 支持边界。 |
| `mtbml_inference_engine` | Imagimob PSoC 6 示例的 `NN_INFERENCE_ENGINE` 支持 `tflm` / `tflm_less` | `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md` | 仅适用于该示例工程及其衍生 Makefile。 |
| `motion_model_quantization` | Deploy Motion README 写明示例默认模型只支持 `int8x8` | `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md` | 替换模型时必须同步核对 `NN_TYPE`。 |
| `supported_operators_matrix` | 【待补充：建议查阅 `ingest/html/deepcraft-model-converter_additional-resources.md` 与对应 supported operators 页面镜像】 | `ingest/html/*.md` | 当前知识库还没把支持算子矩阵整理成固定表。 |

## 7. 示例级版本要求参数

| 参数 | 当前本地依据 | 优先验证位置 | 备注 |
|------|--------------|--------------|------|
| `mtb_version_imagimob_psoc6` | ModusToolbox 3.1+，ML Pack 2.0+ | `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md` | 这是 PSoC 6 Imagimob MTBML Deploy 的要求。 |
| `mtb_version_face_id` | ModusToolbox 3.6+，BSP 1.1.0+ | `docs/readmes/README_Machine_Learning_Face_ID_Demo.md` | 这是 Face ID Demo 的工程要求。 |
| `mtb_version_deepcraft_edge_examples` | Data Collection / Deploy Motion / Deploy Vision 都写成 ModusToolbox 3.6+，BSP 1.0.0+ | `docs/readmes/README_DEEPCRAFT_Data_Collection.md`、`docs/readmes/README_DEEPCRAFT_Deploy_Motion.md`、`docs/readmes/README_DEEPCRAFT_Deploy_Vision.md` | 适用于这些 PSoC Edge 示例，不应外推到全部代码例程。 |
| `kit_software_setup_reference` | KIT_PSE84_EVAL 用户指南的软件准备项写为 ModusToolbox 3.8+ 与 KitProg3 drivers | `knowledge/index_kit_guide.md` | 套件级安装口径，回答具体示例时仍要回到 README。 |
| `mtb_3_6_release_behavior` | 3.6 增强了 PSoC Edge 相关 Device Configurator，并明确 LLVM / connected kits / `make program -j` 已知问题 | `docs/release_notes/mt3.6_release_notes.pdf#3` `docs/release_notes/mt3.6_release_notes.pdf#4` `docs/release_notes/mt3.6_release_notes.pdf#15` | 适合回答“3.6 相比旧版本多了什么 / 哪些坑仍在”。 |
| `mtb_3_7_release_behavior` | 3.7 新增 memory report tool，并调整 Device Configurator / pack / 代理与 `.mtb` 依赖问题 | `docs/release_notes/mt3.7_release_notes.pdf#3` `docs/release_notes/mt3.7_release_notes.pdf#4` `docs/release_notes/mt3.7_release_notes.pdf#6` `docs/release_notes/mt3.7_release_notes.pdf#15` | 当前 memory / getlibs / proxy 问题应优先联想到该版本变化。 |
| `version_compatibility_matrix` | 当前已补 `knowledge/version_compatibility_guide.md` 作为统一入口 | `knowledge/version_compatibility_guide.md` | 已有初版入口，但仍不是所有工具组合的完整矩阵。 |

## 8. 传感器 / 接口参数

| 参数 | 当前本地依据 | 优先验证位置 | 备注 |
|------|--------------|--------------|------|
| `face_id_camera_display` | Face ID Demo 支持 USB Camera（OV7675 / OS02F10 / Logitech C920）与 4.3-inch MIPI DSI LCD | `docs/readmes/README_Machine_Learning_Face_ID_Demo.md` | KIT_PSE84_AI 还要求 Type-A 到 Type-C 转接器接 USB 摄像头。 |
| `vision_camera_type` | Deploy Vision 支持 USB Camera，AI Kit 还支持 DVP Camera，切换需修改 `CAMERA_TYPE` | `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md` | 非列出 USB 摄像头需核对 VID/PID。 |
| `kit_pse84_ai_multimedia_if` | AI Kit 用户指南确认有 MIPI-DSI、analog/digital microphones、Wi-Fi/BT、Quad-SPI NOR Flash、Octal-SPI HYPERRAM、KitProg3、JTAG/SWD、IMU、磁力计、压力、湿度、RADAR | `docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#6` | 回答 AI Kit 板级接口时应先看该用户指南，而不是只引用网页。 |
| `kit_pse84_eval_sensor_if` | BMI323 IMU (I2C/SPI)、BMM350 (I2C)、ICS-43434 (I2S/PDM)、BGT60TR13C (SPI) | `knowledge/index_kit_guide.md` | 这是 KIT_PSE84_EVAL 板级接口，不等于所有 PSoC Edge 板卡。 |
| `deepcraft_collection_sensors` | Data Collection 示例支持 BMI270、BMM350、IM73D122V01、DPS368、SHT40、BGT60TR13C，并通过 USB 向 Studio 传输 | `docs/readmes/README_DEEPCRAFT_Data_Collection.md` | 若同时开所有传感器，README 建议先用默认/最低频率。 |
| `psoc6_imagimob_sensor_path` | PSoC 6 Imagimob 示例的人体动作模型走 IMU，哭声模型走 PDM/PCM | `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md` | 对应的预处理和模型文件命名也不同。 |
| `sensor_interface_global_matrix` | 当前已能分别从 `KIT_PSE84_EVAL` 与 `KIT_PSE84_AI` 用户指南回答主要接口，但跨全部板卡的统一矩阵仍未完成 | `knowledge/index_kit_guide.md` `knowledge/index_ai_kit_guide.md` | 当前可以分 kit 回答，仍不建议臆造“全平台统一接口表”。 |

## 9. Memory / linker / XIP 参数

| 参数 | 当前本地依据 | 优先验证位置 | 备注 |
|------|--------------|--------------|------|
| `rram_capacity` | RRAM up to 512 KB；最小读写粒度 128-bit + 25-bit ECC | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#5` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#7` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#8` | 适合掉电后保留代码/数据，但读访问有 wait states。 |
| `sram_capacity_and_retention` | SRAM 0/1 共 1 MB，Deep Sleep 保留粒度 64 KB | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#5` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#10` | SRAM 无 wait states，适合 runtime data 与高频访问代码。 |
| `socmem_capacity` | System SRAM (SoCMEM) 5120 KB；10 partitions × 512 KB | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#5` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#11` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#12` | 位于 PD1，高性能但不适合在 PD1 关闭时保存关键内容。 |
| `cm55_tcm_size` | ITCM 256 KB、DTCM 256 KB | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#7` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#14` | DTCM 默认常用于 CM55 stack；ITCM 默认常放 vector table 和部分关键代码。 |
| `smif_xip_window` | 每个 SMIF 可访问 1 GB 地址空间，XIP 窗口 64 MB | `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#15` | 回答外部 flash / RAM 映射问题时先确认是 address space 还是 XIP window。 |
| `smif_transfer_modes` | 支持 XIP 与 MMIO；支持 SDR / DDR；支持 Quad / Octal / HyperBus | `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#15` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#16` | 速度与协议选择直接影响性能。 |
| `smif_rww_limitation` | 外部 memory 若不支持 RWW，则写/擦期间从同一 SMIF XIP 读会 fault | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#8` | 固件升级、日志落 flash、双核共享 SMIF 时必须优先检查。 |
| `default_memory_map` | 默认 map 含 RRAM / SRAM / SoCMEM / ITCM / DTCM / SMIF0 / SMIF1 别名 | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#19` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#17` | 回答地址映射问题时优先引用该页。 |
| `default_external_layout` | 默认外部 flash 布局含 CM55 image / trailer；EVK 默认 Quad SPI Flash 启用，Octal RAM 默认未启用 | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#23` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#18` | 适用于 KIT_PSE84_EVAL_EPC2 BSP 默认布局。 |
| `generated_linker_file` | Device Configurator 生成的 memory 定义文件位于 `bsps/TARGET_<BSP>/config/GeneratedSource/cymem_<Toolchain>_<Core>.<ext>` | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#25` `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#38` | 遇到 memory region 对不上时先查生成文件，而不是只盯主 linker。 |
| `linker_vma_lma` | `> VMA_mem_reg AT > LMA_mem_reg` 用于区分运行地址与装载地址 | `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#24` | 回答“放在 flash 里但运行在 SRAM/ITCM”时的关键概念。 |
