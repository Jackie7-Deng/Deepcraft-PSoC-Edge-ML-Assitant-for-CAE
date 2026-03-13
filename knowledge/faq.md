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
