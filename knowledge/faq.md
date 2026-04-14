# 高频问答

**更新日期**: 2026-03-10
**定位**: 沉淀 PSoC Edge + DEEPCRAFT 相关的高频问题、可复用排障经验与官方依据，帮助助手优先给出更像工程师而不是纯导航器的回答。

---

## Q1：为什么语音项目在旧环境能编过，但在新环境里突然编译失败？

### 结论

优先检查编译器环境变量是否缺失或指向错误路径，尤其是 `CY_COMPILER_ARM_DIR` 与 `CY_COMPILER_LLVM_ARM_DIR`。语音与音频相关示例明确要求设置这些路径，否则构建系统可能找不到编译器。  

### 适用前提

- 语音助手、音频增强等依赖 Arm / LLVM 编译器的示例
- 新开发环境首次搭建、跨机器迁移、跨操作系统迁移

### 证据

- `docs/readmes/README_Voice_Assistant_Deployment.md:79-88`
- `docs/readmes/README_Audio_Enhancement.md:94-102`
- `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`

### 解释

这些 README 都要求在环境变量或 `common.mk` 中显式配置编译器安装路径。如果新环境没有设置对应变量，或变量仍指向旧机器路径，构建会在调用编译器时失败。  

### 建议动作

1. 先确认当前工具链是 Arm 还是 LLVM。
2. 检查 `CY_COMPILER_ARM_DIR` / `CY_COMPILER_LLVM_ARM_DIR` 是否存在。
3. 检查路径是否真实存在于当前机器。
4. 若是新环境迁移，确认没有遗留旧机器或旧系统路径。

### 工程经验

【推断/经验】你提供的近期案例说明：构建系统在新环境中引用了不存在的 `C:/Program Files/ARMCompiler6.16` 路径，导致编译器可执行文件找不到。这个现象与 README 中“必须显式配置编译器路径”的要求一致，因此应优先把它当作迁移失败时的第一检查项。

---

## Q2：替换 Imagimob / DEEPCRAFT 模型后，最容易漏改哪些配置？

### 结论

最容易漏改的是模型名、模型输出目录，以及推理引擎相关 Makefile 参数。仅替换模型文件而不更新这些参数，工程可能继续引用旧模型或旧输出路径。  

### 适用前提

- `Machine_Learning_Imagimob_MTBML_Deploy/`
- 使用 ModusToolbox ML Configurator 或 DEEPCRAFT / Imagimob 生成的新模型

### 证据

- `Machine_Learning_Imagimob_MTBML_Deploy/README.md:59-71`
- `knowledge/examples_catalog.md:9-20`

### 解释

README 明确写到，若改变默认模型设置，需要同步更新 `NN_MODEL_NAME`、`NN_MODEL_FOLDER`、`NN_INFERENCE_ENGINE` 等 Makefile 参数。示例目录也指出该工程的关键入口和生成代码路径，说明模型替换不只是“拷文件”，而是“模型 + 配置 + 输出目录”的整组变更。  

### 建议动作

1. 核对 ML Configurator 中的 project name 与输出目录。
2. 同步检查 `NN_MODEL_NAME`、`NN_MODEL_FOLDER`、`NN_INFERENCE_ENGINE`。
3. 确认工程实际引用的生成文件已切换到新模型目录。

---

## Q3：Edge API 为什么有时是 Function API，有时又变成 Queue API？

### 结论

Edge API 的形态取决于模型生成结果中是否存在 queue layers，以及是否启用了时间戳相关接口。不是所有模型都会生成完全相同的 API 组合。  

### 适用前提

- 使用 DEEPCRAFT / Imagimob 生成的 Edge 模型
- 查询 `IMAI_Init`、`IMAI_enqueue`、`IMAI_dequeue`、`IMAI_compute` 等接口

### 证据

- `ingest/html/edge_api.md:37-63`
- `ingest/html/edge_api.md:65-90`

### 解释

网页归档明确给出了 API 选择表：  
- 无 queue layers 时，通常是 Function API  
- 有 queue layers 时，会出现 Queue API 或 Queue No Time API  
同时文档还强调，如果用了 Queue API，通常每次 `IMAI_enqueue()` 后都应及时调用 `IMAI_Dequeue()`。  

### 建议动作

1. 先看当前生成模型对应的 `model.h`。
2. 确认是否定义了 queue 相关宏。
3. 若存在 queue layers，不要按纯 `IMAI_compute()` 的心智模型使用整套接口。

---

## Q4：tensor arena 大小到底该看哪里？

### 结论

优先看 `mtb_ml_gen/info/` 下生成的 arena 信息文件，而不是凭经验拍一个固定值。  

### 适用前提

- `Machine_Learning_Imagimob_MTBML_Deploy/`
- 使用 MTB ML / TFLM 生成模型后需要确认内存占用

### 证据

- `Machine_Learning_Imagimob_MTBML_Deploy/mtb_ml_gen/info/IMAGIMOB_MODEL_tflm_float_tensor_arena_size.txt:1`
- `knowledge/examples_catalog.md:18-20`

### 解释

当前示例里已经有生成出的 arena 信息文件，内容直接给出了 `Used Arena Size` 和 `Required size`。这比从 README 或经验里猜内存更可靠。示例目录也把 tensor arena 大小配置列为常见问题，说明这是部署阶段的高频风险点。  

### 建议动作

1. 每次重新生成模型后，先检查 `mtb_ml_gen/info/*_tensor_arena_size.txt`。
2. 再核对工程中实际使用的 arena 常量是否与生成结果一致。
3. 若出现初始化失败或内存异常，优先回看该文件而不是先改其他推理逻辑。

---

## Q5：PSoC Edge 和 PSoC 6 的部署假设可以混用吗？

### 结论

不能直接混用。当前工作区同时包含 PSoC Edge E84 与 PSoC 6 / CY8CKIT-062S2-AI 示例，但两类平台的硬件能力、示例路径和部署关注点不同。  

### 适用前提

- 同时面对 Face ID Demo、MTBML Deploy、Voice / Audio 类示例
- 需要判断板卡、BSP、NPU、外设依赖是否一致

### 证据

- `knowledge/overview.md:18-20`
- `knowledge/examples_catalog.md:12-20`
- `knowledge/examples_catalog.md:22-32`

### 解释

`Machine_Learning_Imagimob_MTBML_Deploy/` 明确对应 PSoC 6，`PSOC_Edge_Machine_Learning_Face_ID_Demo/` 明确对应 PSoC Edge E84。平台混淆会导致 README、BSP、硬件依赖、NPU 路径和排障步骤全部错位。  

### 建议动作

1. 回答前先确认目标板卡与 BSP。
2. 先确定问题属于 PSoC Edge 还是 PSoC 6，再继续查资料。
3. 若用户只说“这个 demo”，优先追问工程名或路径。

---

## Q6：什么时候应该优先查 README，而不是直接查源码或 PDF？

### 结论

当问题与工程创建、工具链要求、支持板卡、外设依赖、构建前置条件相关时，应先查 README；当问题进入接口细节、函数行为或寄存器级排障时，再进入源码或 PDF。  

### 适用前提

- 工程无法构建
- 用户不确定该从哪个示例开始
- 用户只给了工程名，没有给出错误堆栈或源码位置

### 证据

- `Machine_Learning_Imagimob_MTBML_Deploy/README.md:15-30`
- `docs/readmes/README_Voice_Assistant_Deployment.md:73-90`
- `knowledge/document_map.md:10-19`

### 解释

README 往往已经集中说明了工具链、支持板卡、环境变量、模型入口、构建方式等高层前提；这些前提没确认前，过早进源码通常效率很低。文档地图也把 README 放在排障和示例导航的早期入口，而不是最后一步。  

### 建议动作

1. 先看目标工程 README 的 Requirements / Software setup / Using the code example。
2. 若 README 已明确限制，再决定是否进入源码或 PDF。
3. 只有当问题进入函数、宏、寄存器层面时，再继续向下钻取。

---

## Q7：Device Configurator 在 PSoC Edge / PSoC 6 工程里到底负责什么？

### 结论

它负责器件级硬件配置，包括 pins、clocks、peripherals、DMA 等，并且会生成项目实际要参与构建的配置代码；对 PSoC MCU 项目来说，它不是可有可无的辅助工具。  

### 适用前提

- ModusToolbox 工程
- 需要检查硬件初始化、外设资源映射、时钟或 DMA 配置

### 证据

- `docs\MTB_docs\device-configurator.pdf#4`
- `docs\MTB_docs\device-configurator.pdf#11`
- `knowledge\modustoolbox_tools_summary.md:27-44`

### 解释

官方文档明确写到，Device Configurator 用于启用和配置 clocks、pins 以及标准 MCU peripherals；在 ModusToolbox 环境中，它是 tools package 的组成部分，而且在 PSoC MCU 设备上是必需工具。文档还给出了标准流程：先清 Notice List，再配置硬件，保存，然后把 `GeneratedSource` 加入构建。  

### 建议动作

1. 确认当前问题是否属于硬件资源层而不是模型层。
2. 打开 Device Configurator 检查 Notice List。
3. 检查 Pins / System / Peripherals / DMA / Clocks 是否与工程假设一致。

---

## Q8：为什么 `GeneratedSource` 目录不能随手删掉或忽略？

### 结论

因为它承载的是配置生成后的代码产物；如果不把它纳入构建，Device Configurator 中做过的器件配置并不会真正进入固件。  

### 适用前提

- 工程里使用了 `design.modus` / Device Configurator
- 修改了时钟、引脚、外设、DMA 等配置

### 证据

- `docs\MTB_docs\device-configurator.pdf#11`
- `knowledge\modustoolbox_tools_summary.md:45-55`

### 解释

官方流程明确要求“保存配置后，把新创建的 `GeneratedSource` 文件夹加入构建”。这意味着它不是临时缓存，而是工程配置生效的桥梁。  

### 建议动作

1. 检查 `GeneratedSource` 是否存在。
2. 检查构建系统是否仍在编译其中的生成文件。
3. 如果外设配置改了但行为没变，优先怀疑这里。

---

## Q9：BSP 到底是什么，为什么回答前一定要先确认它？

### 结论

BSP 会决定目标板卡/套件、板级资源假设和构建目标；如果 BSP 不明确，很多关于外设、构建、烧录甚至示例兼容性的判断都会错位。  

### 适用前提

- 构建失败
- 板卡不匹配
- 不确定该从哪个例程/工程起步

### 证据

- `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`
- `docs\MTB_docs\New-to-ModusToolbox.pdf#2`
- `knowledge\parameters_catalog.md:8-17`

### 解释

官方 make 变量说明里已经把 `TARGET` 解释成目标 board/kit，也就是 BSP。新手指南也说明了 BSP 级配置与 library 级配置是不同层次。也就是说，BSP 不是“顺手选一下”的无关参数，而是整个工程路径的起点。  

### 建议动作

1. 回答前先确认 `kit_or_bsp`。
2. 构建异常时先看 `TARGET/BSP` 是否与工程和板卡一致。
3. 不要把 PSoC Edge 和 PSoC 6 的 BSP 假设混用。

---

## Q10：Machine Learning configurator 和 Device Configurator 是一回事吗？

### 结论

不是。Machine Learning configurator 更偏 library-level / 中间件层；Device Configurator 则是器件级硬件配置工具。  

### 适用前提

- 用户说“configurator 里改过了”，但没有说具体是哪一个 configurator
- 模型配置问题与硬件初始化问题容易混淆

### 证据

- `docs\MTB_docs\New-to-ModusToolbox.pdf#2`
- `docs\MTB_docs\device-configurator.pdf#4`
- `knowledge\modustoolbox_tools_summary.md:19-25`

### 解释

新手指南明确区分了 BSP 级配置和 Library 级配置，并把 Machine Learning configurator 列在 library-level configurators 里；而 Device Configurator 负责 pins、clocks、peripherals、DMA 等硬件对象。  

### 建议动作

1. 先问清用户改的是哪个 configurator。
2. 若症状是模型/中间件行为异常，优先看 library-level 配置。
3. 若症状是外设、时钟、DMA、引脚异常，优先看 Device Configurator。

## Q11：不同示例对 ModusToolbox / ML Pack 的版本要求是否一致？

### 结论

不一致，必须按具体工程回答。当前本地资料至少能确认三条不同口径：PSoC 6 Imagimob MTBML Deploy 需要 ModusToolbox 3.1+ 与 ML Pack 2.0+；Face ID Demo 需要 ModusToolbox 3.6+；KIT_PSE84_EVAL 用户指南把板卡软件准备写成 ModusToolbox 3.8+。因此，不能把某个示例的版本要求当成整个 PSoC Edge / PSoC 6 体系的统一要求。

### 适用前提

- 用户问最低需要哪个 ModusToolbox 版本
- 用户在不同示例之间切换，或把 PSoC 6 与 PSoC Edge 资料混在一起

### 证据

- `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:45-53`
- `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:44-49`
- `knowledge/index_kit_guide.md:89-98`

### 解释

PSoC 6 Imagimob 示例明确把工具链前提写成 ModusToolbox 3.1+ 和 ML Pack 2.0+；Face ID Demo 把示例要求写成 ModusToolbox 3.6+；而套件级用户指南又给出了 3.8+ 的安装口径。这说明版本要求和示例套件文档工具安装指南三种证据层有关，回答时必须先确认用户实际在跑哪个工程。

### 建议动作

1. 先确认工程路径与 README。
2. 再确认是否还需要安装 ML Pack。
3. 如果用户只说PSoC Edge 工程，不要直接给唯一版本号，而应说明按具体示例 README 为准。

---

## Q12：Face ID Demo 运行前必须准备哪些硬件？

### 结论

Face ID Demo 至少要确认三类硬件条件：目标板卡属于 `KIT_PSE84_EVAL_EPC2` / `KIT_PSE84_EVAL_EPC4` / `KIT_PSE84_AI`，显示端接 4.3 英寸 DSI LCD，摄像头端接受支持的 USB 摄像头；若是 `KIT_PSE84_EVAL`，还要确认 `BOOT SW` 为 HIGH/ON 且 `J20/J21` 处于 NC。

### 适用前提

- 首次上板运行 Face ID Demo
- 用户说工程能编过，但屏幕/摄像头没起来

### 证据

- `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:57-72`
- `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:73-92`
- `knowledge/examples_catalog.md:24-35`

### 解释

README 明确列出了支持套件、显示屏、摄像头与跳线/开关前提。当前示例目录也把 Face ID Demo 的硬件依赖写成摄像头模块、LCD 显示屏。因此，如果屏幕无画面、摄像头无输入或程序启动后行为异常，第一步应先核对硬件链而不是直接怀疑模型。

### 建议动作

1. 先确认板卡型号与 `TARGET`。
2. 再确认摄像头接在 USB host 口、DSI 显示线已接好。
3. 若是 `KIT_PSE84_EVAL`，补查 `BOOT SW`、`J20`、`J21`。

---

## Q13：为什么 Face ID Demo 或 DEEPCRAFT 视觉/运动示例在 GCC_ARM RELEASE 下容易编译失败？

### 结论

当前本地 README 明确记录了一个共同限制：Face ID Demo、DEEPCRAFT Vision 与 DEEPCRAFT Motion 示例都可能在 `GCC_ARM` 的 `RELEASE` 模式下因 CMSIS-DSP 的 Helium 指令不被识别而构建失败。

### 适用前提

- 目标工程是 PSoC Edge E84 的 Face ID / Deploy Vision / Deploy Motion
- 症状表现为 RELEASE 才失败，Debug 能通过或 armclang 能通过

### 证据

- `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:51-56`
- `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md:45-53`
- `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md:50-59`

### 解释

三个 README 都把同类限制写成显式 Note，说明这不是个别工程的偶发现象，而是当前工具链/库组合下的已知限制。如果用户只贴build failed，应优先追问是不是 `GCC_ARM + RELEASE`，不要直接把问题归因到模型或 BSP。

### 建议动作

1. 先确认 `CONFIG` 与 `TOOLCHAIN`。
2. 如果是 `GCC_ARM + RELEASE`，优先尝试 Debug、`ARM` 或 `LLVM_ARM` 路径。
3. 回答时明确这是 README 已知限制，而不是通用 C 代码错误。

---

## Q14：切换 DEEPCRAFT 运动模型时，最容易漏改哪些参数？

### 结论

最容易漏改的是 CPU 运行核心、量化类型和 IMU 传感器通道配置，也就是 `ML_DEEPCRAFT_CPU`、`NN_TYPE` 和 `IMU_ENABLE_SENSOR`。如果使用跨板卡迁移的数据，还要注意 `SENSOR_REMAPPING` 是否保持与训练假设一致。

### 适用前提

- `README_DEEPCRAFT_Deploy_Motion.md` 对应的 PSoC Edge 运动部署工程
- 需要替换模型、切换 CM33/CM55 或调整 IMU 轴数据

### 证据

- `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md:87-104`
- `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md:128-133`

### 解释

该示例把模型推理位置、量化配置和 IMU 传感器选择都放在 `common.mk` / `proj_cmxx/Makefile` 中，不是替换模型文件就完事。README 还特别提到 BMI270 默认对齐到 CY8CKIT-062S2-AI 的姿态，如果训练和部署板卡姿态不一致，推理结果会偏移。

### 建议动作

1. 替换模型前先记录 `common.mk` 与两个 Makefile 的当前值。
2. 确认模型是 `float` 还是 `int8x8`。
3. 如果跨板卡复用数据，检查 `SENSOR_REMAPPING`。

---

## Q15：DEEPCRAFT 数据采集示例为什么连上板后，Studio 还是收不到数据？

### 结论

优先检查三件事：是否使用了专门的数据传输 USB 口、主机端是否是 Windows、以及板上 LED1 是否在报 USB/UART/I2C/SPI/Memory 等错误码。当前 README 还明确说明 DEEPCRAFT Studio 当前只支持 Windows。

### 适用前提

- `README_DEEPCRAFT_Data_Collection.md` 对应的 E84 数据采集工程
- 用户现象是串口日志正常，但 Studio 无法看到流数据或采集过程中断

### 证据

- `docs/readmes/README_DEEPCRAFT_Data_Collection.md:30-32`
- `docs/readmes/README_DEEPCRAFT_Data_Collection.md:42-43`
- `docs/readmes/README_DEEPCRAFT_Data_Collection.md:85-94`
- `docs/readmes/README_DEEPCRAFT_Data_Collection.md:150-189`

### 解释

该示例区分了 KitProg3 调试口与 USB-device 数据传输口。README 还提供了 LED1 的错误闪烁表，可以把数据没到 Studio进一步分流成 USB 连接错误、UART 错误、I2C/SPI 错误或内存错误。

### 建议动作

1. 先确认主机是 Windows。
2. 检查数据线是否接在 README 指定的 USB-device 口，而不是只接了 KitProg3。
3. 如果仍失败，记录 LED1 错误模式再继续排障。

---

## Q16：烧录失败时，第一优先应该看什么？

### 结论

优先看 `KitProg3` 连接、板卡模式/跳线和所选烧录路径是否匹配当前工程。KIT_PSE84_EVAL 用户指南把Device not found / Programming failed / Debug connection lost分别对应到驱动、模式开关和调试器复位检查；PSoC 6 Imagimob README 则把标准烧录路径写成 Quick Panel 的 `Program (KitProg3_MiniProg4)` 或 `make program`。

### 适用前提

- `make program` 失败
- IDE 里 Program/Debug 配置失败
- 板卡枚举但无法烧录

### 证据

- `knowledge/index_kit_guide.md:101-120`
- `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md:208-255`
- `docs/readmes/README_Machine_Learning_Face_ID_Demo.md:132-139`

### 解释

本地资料把烧录路径和板卡准备分成两层：一层是 Program/Debug 命令，另一层是 KitProg3/板卡状态。如果只盯着 IDE 报错而不检查驱动、USB 连接口和模式开关，通常很难快速定位。

### 建议动作

1. 先确认板卡是否通过 KitProg3 USB 接到 PC。
2. 对 PSoC Edge 先核对 BOOT/J20/J21 等板级前提。
3. 重新尝试 Quick Panel Program 或 `make program`，必要时重装驱动或复位 KitProg3。

---

## Q17：[来源：community] ModusToolbox 工程刚创建就 build error，第一步该做什么？

### 结论

先进入 `modus shell`，切到包含 `Makefile` 的工程目录，执行 `make getlibs`，再执行 `make clean && make build`。社区把这一步作为依赖未拉齐场景的首选动作。

### 适用前提

- PSoC 6 / ModusToolbox 工程刚创建
- 错误像是缺库、缺依赖、工程未完整初始化

### 证据

- `knowledge/community_digest.md`
- `https://community.infineon.com/t5/PSOC-6/ModusToolbox-Build-error/td-p/636941`

### 解释

社区答复没有先让用户改源码，而是先补依赖并重建。这说明很多“刚创建就编不过”的问题，本质上是 getlibs 没做完或工程目录不完整。

### 建议动作

1. 在 `modus shell` 中进入工程目录。
2. 执行 `make getlibs`。
3. 再执行 `make clean && make build`。

---

## Q18：[来源：community] PSoC 6 双核工程 flash overflow 时应该改哪些地方？

### 结论

至少同步检查三处：CM0+ linker 的 flash `LENGTH`、CM4 linker 的 `FLASH_CM0P_SIZE`，以及 `psoc6.h` 中的 CM4 application start address。

### 适用前提

- PSoC 6 双核工程
- 编译报 flash overflow，或者改了 CM0+ 分配后又和 CM4 区域冲突

### 证据

- `knowledge/community_digest.md`
- `https://community.infineon.com/t5/Knowledge-Base-Articles/Flash-overflow-Change-the-PSoC-6-CM0-flash-allocation-in-ModusToolbox-2-4/ta-p/336607`

### 解释

社区 KBA 明确说明只改单个 linker 文件不够，必须把双核共享的 flash 边界保持一致，否则会从“CM0+ 不够”变成“CM4 冲突”。

### 建议动作

1. 先改 CM0+ linker 的 flash 长度。
2. 再让 CM4 linker 的 `FLASH_CM0P_SIZE` 对齐。
3. 最后检查 `psoc6.h` 起始地址。

---

## Q19：[来源：community] Face ID Demo 的 `ifx_face_id_inference()` 内部实现和模型结构在哪里看？

### 结论

社区当前公开答复是回到 GitHub 仓库的 README 和 `docs/design_and_implementation.md`，而不是在帖子正文中展开预编译库内部细节。

### 适用前提

- PSoC Edge Face ID Demo
- 想了解内部模型数量、输入输出格式、预处理 / 后处理或自定义模型替换路径

### 证据

- `knowledge/community_digest.md`
- `https://community.infineon.com/t5/PSOC-Edge/Support-Request-PSOC-Edge-E84-Face-ID-Demo-ifx-face-id-inference-Details-and/td-p/1187681`
- `docs/readmes/README_Machine_Learning_Face_ID_Demo.md`

### 解释

这说明社区层面对 Face ID 预编译库公开信息有限；若用户需要内部实现细节，优先读本地仓库文档，而不是指望社区贴提供完整 API 设计说明。

### 建议动作

1. 先读 Face ID 示例 README。
2. 再读仓库 `docs/design_and_implementation.md`。
3. 若仍需内部实现细节，明确说明当前公开资料有限。

---

## Q20：[来源：community] 把 voice assistant 和 Face ID 合进一个 PSoC Edge E84 工程可行吗？

### 结论

可行，但社区明确说“未正式测试”。首要瓶颈是共享核心和共享内存区的管理，尤其是 `m55_data_secondary`、`.cy_xip`、`.heap` 相关溢出。

### 适用前提

- PSoC Edge E84
- 需要同时跑关键词检测和 Face ID

### 证据

- `knowledge/community_digest.md`
- `https://community.infineon.com/t5/PSOC-Edge/combine-the-demo-codes-of-voice-assistant-with-the-face-ID-recognition-for-PSOC/td-p/1197475`

### 解释

社区建议以 local voice code example 为 base 再叠加 Face ID。用户回复还表明，把关键词检测放到 CM33、Face ID 放到 CM55 后虽然能运行，但识别命中率仍可能掉到 10%~15%，所以这不是单纯“编过就算成功”的问题。

### 建议动作

1. 先做内存布局评估。
2. 优先以 voice 示例为 base 集成。
3. 分别验证编译通过、运行稳定和命中率。

---

## Q21：[来源：case] PSoC Edge E84 烧录时报 `Can't find target/cat1d.cfg` 应先查什么？

### 结论

优先检查 `ModusToolbox Programming tools` 版本。Case 记录给出的已验证路径是：PSoC Edge EAP 使用 `1.2.1`，并卸载 `1.3.1` 后问题消失。

### 适用前提

- PSoC Edge E84 EVK
- OpenOCD / Program 阶段报 `Can't find target/cat1d.cfg`

### 证据

- `knowledge/community_digest.md`
- `IFX-250322-1644913`

### 解释

这类报错不是典型的用户代码错误，而更像是工具包版本与 target 配置不匹配。Case 中用户最终确认“it works”，说明这是已验证可复现的处理路径。

### 建议动作

1. 先记录当前 Progtools 版本。
2. 对照是否为 EAP 场景。
3. 必要时切回 `1.2.1` 并卸载 `1.3.1`。

---

## Q22：[来源：case] MTB-ML 导入或部署自训练模型异常时，最先该怀疑什么？

### 结论

优先怀疑两类问题：数据 / 模型格式不符合 ML 用户指南要求，或者模型里含有当前 Edge 工具链不支持的算子。对现成模型部署，还要检查是否缺少与训练流程配套的 DeepCraft 预处理代码。

### 适用前提

- PSoC Edge
- MTB-ML / DeepCraft / Imagimob 模型导入或部署报错

### 证据

- `knowledge/community_digest.md`
- `IFX-250911-1842110`
- `IFX-250728-1789988`

### 解释

Case 记录显示，先按 `ml-user-guider` 规范格式后，可以至少生成基础 `.c/.h`；但真实模型仍可能因为不支持的算子而无法完整部署。另一条 case 还说明，DeepCraft 生成的预处理代码不是多余部分，而是保证部署端输入与训练数据一致的关键。

### 建议动作

1. 先按 ML 用户指南核对模型和数据格式。
2. 再检查模型是否使用了不支持的算子。
3. 对现成模型部署，确认预处理代码是否与模型一起迁移。

---

## Q23：PSoC Edge 的 memory placement 问题现在优先查哪份本地资料？

### 结论

优先查两份刚接入的本地 memory 资料：AN239774 负责“内部/外部 memory、默认 BSP 布局、linker/VMA/LMA、性能与功耗权衡”，CTW 负责“内存类型、默认地址映射、Lab 风格的 code/data placement 示例”。这两份文档已经足以替代之前 community 里只回指 whitepaper 的空缺。

### 适用前提

- 用户问模型放哪、固件放哪、buffer 放哪
- 用户问 XIP / SoCMEM / ITCM / DTCM / SMIF 的默认布局

### 证据

- `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#19`
- `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#23`
- `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#17`
- `knowledge/memory_layout_guide.md`

### 解释

AN239774 已经明确写了 default memory configuration、external flash layout 和 linker 机制；CTW 则把默认地址和 EVK 默认启用的 SMIF 设备用训练材料形式重新整理了一遍。

### 建议动作

1. 先看 `knowledge/memory_layout_guide.md`。
2. 需要精确页码时再跳回对应 PDF 页。
3. 遇到 community 只给“去看 whitepaper”的答复时，直接切回本地 memory 文档链。

---

## Q24：为什么在 SMIF 写/擦期间从 XIP 执行代码会出问题？

### 结论

因为部分外部 memory IC 不支持 Read While Write (RWW)。当同一颗通过 SMIF 连接的外部 memory 正在写/擦时，如果还从该 memory 做 XIP 读访问，系统可能直接 fault。

### 适用前提

- 固件升级
- 外部 flash 日志写入
- 双核共享外部 flash / RAM

### 证据

- `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#8`

### 解释

应用笔记给出的缓解动作很明确：把关键代码搬到 SRAM / SoCMEM；避免关键流程依赖 XIP；在双核场景下做 core synchronization。

### 建议动作

1. 先确认目标 memory IC 是否支持 RWW。
2. 升级或写 flash 时，把关键流程迁到内部 memory。
3. 若是双核，增加 CM33 / CM55 的互锁与同步。

---

## Q25：PSoC Edge 的 linker memory region 改了却不生效，先查哪里？

### 结论

先查 Device Configurator 自动生成的 `cymem_<Toolchain>_<Core>` 文件，而不是只盯主 linker。PSoC Edge 的 memory region 定义会先落到 `bsps/TARGET_<BSP>/config/GeneratedSource/` 下的 generated linker 文件，再被默认 linker include。

### 适用前提

- 改了 memory region / custom section
- 链接结果与预期 region 不一致
- 不确定问题在 Device Configurator 还是 toolchain linker

### 证据

- `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#25`
- `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#38`

### 解释

应用笔记明确说明 memory region 在 Device Configurator 的 `Memory` tab 里定义，生成文件随后参与主 linker 过程。如果 generated file 没更新或没被 include，再改主 linker 很容易越改越乱。

### 建议动作

1. 先确认 `GeneratedSource/cymem_*` 是否已更新。
2. 再确认主 linker 是否 include 了该文件。
3. 最后才继续改 section 和 region 对应关系。

---

## Q26：如果用户问“我该装 ModusToolbox 3.6 还是 3.7”，应该怎么回答？

### 结论

不要直接给单一版本号。先按**具体工程 README**确认最低要求，再用 3.6 / 3.7 release notes 判断工具行为差异。当前本地资料能明确：3.6 已包含 PSoC Edge 相关 Device Configurator 增强与 LLVM 路径；3.7 新增 `memoryreport`，并补充了代理、`.mtb` 依赖 tag、BSP Assistant 等已知问题的 workaround。

### 适用前提

- 用户在不同示例之间切换
- 用户问升级值不值得
- 用户已经遇到 build / getlibs / memory / proxy 相关问题

### 证据

- `knowledge/version_compatibility_guide.md`
- `docs/release_notes/mt3.6_release_notes.pdf#4`
- `docs/release_notes/mt3.6_release_notes.pdf#15`
- `docs/release_notes/mt3.7_release_notes.pdf#3`
- `docs/release_notes/mt3.7_release_notes.pdf#6`
- `docs/release_notes/mt3.7_release_notes.pdf#15`

### 解释

版本问题通常有两层：一层是“当前工程 README 最低支持什么”，另一层是“当前 tools package 会不会引入或修复你现在碰到的问题”。如果把这两层混成一句“请装最新版”，经常会答偏。

### 建议动作

1. 先确认具体工程。
2. 再看该工程对应 README 的最低要求。
3. 若问题落在 memory report、proxy、`make getlibs`、BSP Assistant 或 LLVM，再回到 release notes 判断 3.6 / 3.7 差异。

---

## Q27：DEEPCRAFT Model Converter 现在本地能确认支持哪些输入和目标设备？

### 结论

根据新加入的 Customer Connector PDF，当前本地证据可确认 Model Converter 支持 `.h5`、`.tflite`、`.pt2` 输入格式，目标设备至少包括 `PSoC 6`、`PSoC Edge M33/NNLite` 和 `PSoC Edge M55/U55`，并同时提供 GUI 与 CLI。

### 适用前提

- 用户问 BYOM
- 用户问是否必须用 GUI
- 用户问某类模型能不能转到 PSoC 6 / PSoC Edge

### 证据

- `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#3`
- `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#4`
- `docs/application_notes/infineon-deepcraft-model-converter-customer-connector-en.pdf#6`
- `knowledge/ml_workflow.md`

### 解释

这份 PDF 属于比网页摘要更直接的产品资料，因此回答格式、目标器件、GUI/CLI 与 desktop validation 这类问题时，应优先引用它，而不是只引用社区经验。

### 建议动作

1. 先确认模型格式是 `.h5` / `.tflite` / `.pt2` 哪一种。
2. 再确认目标是 PSoC 6 还是 PSoC Edge 的哪条部署链。
3. 需要集成上板时，再回到 `knowledge/ml_workflow.md` 和目标工程 README。
