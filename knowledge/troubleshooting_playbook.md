# 排障手册

**更新日期**: 2026-03-10
**定位**: 给 PSoC Edge + DEEPCRAFT 助手提供统一的故障分诊顺序、必须追问的上下文，以及适合当前 Windows 工作环境的最小验证动作。

---

## 1. 先做症状分类

| 症状 | 常见范围 | 第一入口 |
|------|----------|----------|
| 构建失败 | BSP、依赖、工具链、路径 | README、构建日志、`knowledge/ml_workflow.md` |
| Device Configurator / `design.modus` 异常 | Notice List、GeneratedSource、引脚/时钟/DMA 配置 | `knowledge/modustoolbox_tools_summary.md`、MTB PDF |
| 烧录 / 下载失败 | 板卡连接、KitProg/OpenOCD、目标选择 | Kit README、用户日志 |
| 运行崩溃 / 卡死 | arena、内存、外设初始化、模型配置 | 源码、map 文件、日志 |
| 精度异常 | 预处理、量化、数据分布、标签 | 训练说明、生成代码、输入管线 |
| 性能异常 | NPU 路径、输入尺寸、arena、编译配置 | 平台说明、源码、构建配置 |
| 文档理解不一致 | 平台混淆、版本混淆、资料过期 | `knowledge/document_map.md`、README、PDF |

## 2. 必须追问的上下文

最少要确认以下信息：

- 平台：`PSoC Edge` 还是 `PSoC 6`
- 板卡 / BSP
- `TARGET` / `CONFIG` / `TOOLCHAIN`
- ModusToolbox 版本
- `Device Configurator` 是否可打开、`Notice List` 是否清空
- `GeneratedSource` 是否存在且仍在构建中
- DEEPCRAFT Studio 版本
- 工程名或工程路径
- 模型类型与量化方式
- NPU 是否启用
- 完整报错或关键日志

如果这些信息缺失，不要做确定性结论；应先给最小验证步骤，再列出仍需补充项。

## 3. Windows 环境优先验证命令

| 目的 | 推荐动作 |
|------|----------|
| 查看工程结构 | `Get-ChildItem` |
| 搜 README / 文档 | `Get-ChildItem -Recurse` |
| 搜关键字 | `Select-String` |
| 查看文件头部 | `Get-Content -TotalCount` |
| 检查路径是否存在 | `Test-Path` |

避免在本工作区默认排障建议中使用 `grep`、`find`、`cat`、`lsusb` 这类 Unix-first 命令。

## 4. 最小验证顺序

1. 先确认平台与示例工程
2. 再确认 BSP / `TARGET` / toolchain
3. 再找对应 README
4. 再看工作流文档、生成代码或 Device Configurator
5. 最后才进入更细的源码或寄存器 / 手册定位

推荐入口：

- `knowledge/document_map.md`
- `knowledge/examples_catalog.md`
- `knowledge/modustoolbox_tools_summary.md`
- `docs/readmes/README_*.md`
- `knowledge/ml_workflow.md`
- `knowledge/parameters_catalog.md`

## 5. ModusToolbox / Device Configurator 专项检查

### 5.1 工程创建 / 构建类问题

1. 先确认 `TARGET/BSP` 与当前板卡是否一致。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`
2. 再确认 `TOOLCHAIN` 以及 `CY_COMPILER_ARM_DIR` / `CY_COMPILER_LLVM_ARM_DIR` 是否正确。`knowledge\faq.md:8-38`
3. 若是迁移到新环境，优先怀疑环境变量或工具链路径，而不是先怀疑模型本身。

### 5.2 硬件配置类问题

1. 打开 Device Configurator，先看 `Notice List` 是否还有待处理项。`docs\MTB_docs\device-configurator.pdf#11`
2. 再检查 `Pins`、`System`、`Peripherals`、`DMA`、`Clocks`。
3. 保存后确认 `GeneratedSource` 仍存在，并参与构建。`docs\MTB_docs\device-configurator.pdf#11`

### 5.3 配置器混淆类问题

如果用户只说“我在 configurator 里改了”，先追问是 **Machine Learning configurator** 还是 **Device Configurator**，不要把中间件配置和器件级配置混为一谈。`docs\MTB_docs\New-to-ModusToolbox.pdf#2`

## 6. 标准输出模板

【症状分类】

【当前最可能原因】

【证据引用】

【最小验证步骤】

【仍需补充的信息】

## 7. 当前已知边界

- 当前工作区已经有 `scripts/semantic_search.py`、`scripts/symbol_search.py`、`mcp_servers/vector_search_server.py` 与索引脚本，可用于缩小范围，但它们不替代 README、PDF、构建日志和源码证据
- 对具体函数签名或寄存器细节，仍需回到源码、README 或 PDF
- 若没有直接证据，必须明确写 `未在当前知识库找到依据`

## 8. 场景化 runbook

### 8.1 固件编译失败

**优先判断**
- 是否混用了 PSoC 6 与 PSoC Edge 的 README / BSP / Makefile 假设。
- 是否踩中了 `GCC_ARM + RELEASE` 的已知限制。
- 是否缺少编译器环境变量、ML Pack 或对应 BSP。

**最小检查顺序**
1. 先看示例 README 的版本要求：PSoC 6 Imagimob MTBML 需要 ModusToolbox 3.1+ 与 ML Pack 2.0+；Face ID / Deploy Motion / Deploy Vision 需要 ModusToolbox 3.6+；KIT_PSE84_EVAL 用户指南的软件安装口径是 ModusToolbox 3.8+。`docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:45-53` `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:44-49` `knowledge/index_kit_guide.md:89-98`
2. 再确认 `CONFIG` / `TOOLCHAIN`，尤其是是否为 `GCC_ARM + RELEASE`。Face ID / Deploy Motion / Deploy Vision README 都记录了 Helium 指令导致的已知构建失败。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:51-56` `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md:50-59` `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md:45-53`
3. 若是语音/音频旧示例迁移，继续检查 `CY_COMPILER_ARM_DIR` / `CY_COMPILER_LLVM_ARM_DIR`。`knowledge/faq.md:8-38`

**仍需补充的信息**
- 完整构建命令
- `TARGET` / `BSP` / `TOOLCHAIN` / `CONFIG`
- 首个报错片段

### 8.2 模型推理结果异常

**典型症状**
- 推理输出明显不对
- 模型能跑但结果漂移
- 更换模型后行为与训练集不一致

**最小检查顺序**
1. 先核对模型文件和预处理文件是否配套。Imagimob 示例要求同时更新 `NN_MODEL_NAME`、`NN_MODEL_FOLDER`、`NN_INFERENCE_ENGINE`，并保持 `imu_model.c/h` 或 `pdm_model.c/h` 与模型一致。`docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:91-101` `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:298-300`
2. 再看 `tensor_arena` 或生成信息文件；当前工作流指南和 FAQ 都明确要求优先看 `mtb_ml_gen/info/*_tensor_arena_size.txt`。`knowledge/ml_workflow.md:117-149` `knowledge/faq.md:101-125`
3. 对 IMU / Motion 任务，检查姿态与训练假设是否一致，以及 `SENSOR_REMAPPING` 是否开启。`docs/readmes/README_DEEPCRAFT_Deploy_Motion.md:115-132` `docs/readmes/README_DEEPCRAFT_Data_Collection.md:143-149`
4. 对 Vision 任务，先确认摄像头类型、输入分辨率与 `CAMERA_TYPE` / `CAMERA_WIDTH` / `CAMERA_HEIGHT` 等 Makefile 配置。`docs/readmes/README_DEEPCRAFT_Deploy_Vision.md:81-89` `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:108-125`

### 8.3 Face ID 识别率低 / 注册失败

**优先判断**
- 问题是检测不到脸，还是能检测但注册姿态不达标，还是已注册但识别成 unknown。

**最小检查顺序**
1. 先确认硬件链：USB 摄像头、DSI LCD、板卡跳线都符合 README。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:63-92`
2. 再确认 UI 是否已经进入 enrolment mode；至少采到 3 个 pose 才能提前保存，默认可设置为 3/5/9 poses。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:108-125` `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:158-189`
3. 如果界面提示 face too close to edges，先调整脸部位置；README 明确把靠边视为注册失败场景。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:182-189`
4. 识别速度与 UI 帧率不同：模型推理约 30 FPS，但整机应用约 10 FPS，README 把原因归为内存约束。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:25-37`

### 8.4 ModusToolbox 工程导入失败

**优先判断**
- 问题发生在 Project Creator 创建阶段，还是导入后缺库 / 工作区打不开。

**最小检查顺序**
1. 尽量按 README 推荐路径创建工程：Project Creator GUI 或 `project-creator-cli`。`docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:105-160`
2. 在 Windows 上使用 `modus-shell` 执行命令行创建，不要直接用普通 `cmd`。`docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:137-160`
3. 重新核对 `--board-id` / `TARGET` 是否属于该示例支持清单。`docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:63-72` `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:57-62`
4. 如果创建后缺库，回看 README 对 `git clone` 和 `make getlibs` 的说明。`docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:139-160`

### 8.5 烧录失败

**优先判断**
- 是板卡未被识别，还是识别了但 Program 失败，还是 Program 成功但应用不启动。

**最小检查顺序**
1. 对 PSoC Edge E84 先核对硬件前提：`BOOT SW` 为 HIGH/ON，`J20/J21` 为 NC。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:63-72` `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md:61-69` `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md:68-76`
2. 再确认是否通过 KitProg3 USB 口接到 PC，并使用对应 Program 配置或 `make program`。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:130-139` `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:226-255`
3. 如果是套件识别问题，参考 KIT_PSE84_EVAL 用户指南的三类建议：Device not found  reinstall drivers；Programming failed  check mode switch；Debug connection lost  reset KitProg3。`knowledge/index_kit_guide.md:101-120`
4. 如果 Program 成功但应用无输出，再回看 UART 口、外设连接与示例操作步骤。`docs/readmes/README_Machine_Learning_Face_ID_Demo.md:134-145` `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md:120-148`

### 8.6 Memory / linker / XIP 相关异常

**典型症状**
- `flash overflow` / `RAM overflow` / `.heap`、`.cy_xip`、`m55_data_secondary` 溢出
- 固件升级或日志写入期间，从 XIP 代码路径突然 fault
- 明明改了 memory region，但 linker 结果没有变化

**最小检查顺序**
1. 先分清问题是在默认 memory map、external flash layout，还是运行时 XIP / MMIO 路径。`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#19` `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#23`
2. 若涉及 `> VMA ... AT > LMA ...`、代码放 SRAM/ITCM/外部 flash，先回到 VMA/LMA 说明，不要只看 section 名字。`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#24`
3. 若改的是 Device Configurator memory region，优先检查 `bsps/TARGET_<BSP>/config/GeneratedSource/cymem_<Toolchain>_<Core>.*` 是否已更新并被主 linker include。`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#25` `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#38`
4. 若问题发生在 SMIF 写/擦期间，优先怀疑 memory IC 不支持 RWW，避免从同一 SMIF 执行关键 XIP 代码。`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#8`
5. 对 CM55 性能或实时性问题，先评估 ITCM / DTCM / cache / U55 路径，再决定是否继续把代码或数据留在 RRAM / 外部 memory。`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#34`
