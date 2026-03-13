# ModusToolbox 工具链摘要

**更新日期**: 2026-03-11  
**定位**: 为 PSoC Edge + DEEPCRAFT 助手提供一个低 token 的 ModusToolbox 工具链入口，帮助回答工程创建、硬件配置、BSP、构建系统与集成排障问题。

---

## 1. 这三份指南分别解决什么问题

- `New-to-ModusToolbox.pdf` 适合新手快速建立整体心智：ModusToolbox 是 GUI 与非 GUI 工具、库和程序的组合，不只是一个 IDE；它还明确区分了 **BSP 级配置** 与 **Library 级配置**，其中 Machine Learning configurator 属于 library-level configurator。`docs\MTB_docs\New-to-ModusToolbox.pdf#1` `docs\MTB_docs\New-to-ModusToolbox.pdf#2`
- `infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf` 适合回答“工具包怎么构成、项目怎么创建、make 怎么驱动构建、manifest/BSP 怎么管理”这类工程问题。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#6` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#56`
- `device-configurator.pdf` 适合回答“硬件配置怎么做、为什么必须看 Notice List、GeneratedSource 为什么不能丢、Pins/Clocks/DMA 去哪里配”这类问题。`docs\MTB_docs\device-configurator.pdf#4` `docs\MTB_docs\device-configurator.pdf#11` `docs\MTB_docs\device-configurator.pdf#49`

## 2. 与当前 PSoC Edge + DEEPCRAFT 助手的交叉点

### 2.1 DEEPCRAFT 生成代码并不等于工程可直接工作

DEEPCRAFT / Imagimob 负责数据、训练、量化、代码生成；真正把生成物放进板级工程并构建、烧录、调试时，仍要落回 ModusToolbox 项目、BSP、Makefile、Device Configurator 和编译器环境变量。`knowledge\ml_workflow.md:117-160` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`

### 2.2 Machine Learning Configurator 不替代 Device Configurator

Machine Learning configurator 属于 **Library 级配置**，更关注中间件/ML 行为；Device Configurator 属于 **BSP 级/器件级硬件配置**，负责 pins、clocks、peripherals、DMA 等硬件初始化。两者解决的问题不同，不能互相替代。`docs\MTB_docs\New-to-ModusToolbox.pdf#2` `docs\MTB_docs\device-configurator.pdf#4`

### 2.3 回答 PSoC Edge 工程问题前，先确认工具链栈

如果不知道当前项目是哪个 BSP、使用什么 toolchain、是否启用了 Device Configurator、GeneratedSource 是否仍在构建中，很多构建/运行结论都会失真。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44` `docs\MTB_docs\device-configurator.pdf#11`

## 3. 工具链分层速览

| 层级 | 组件 | 作用 | 典型问题 |
|------|------|------|----------|
| 工程入口层 | Dashboard / Project Creator | 创建工程、选 BSP、拉依赖 | 应该从哪个 BSP 起步？ |
| 硬件配置层 | Device Configurator | 配 pins、clocks、peripherals、DMA，并生成 `GeneratedSource` | 为什么外设不工作？ |
| 中间件配置层 | Library configurators（含 Machine Learning） | 调整 ML / CAPSENSE / Bluetooth 等库配置 | 模型配置或中间件设置去哪改？ |
| 构建层 | `make` / `Makefile` / `TARGET` / `TOOLCHAIN` / `CONFIG` | 决定工程如何编译、链接、烧录 | 为什么 `make build` 失败？ |
| 资产发现层 | manifest / BSP / library metadata | 决定可见的 BSP、示例和中间件集合 | 为什么工具里看不到想要的 BSP / example？ |

证据：`docs\MTB_docs\New-to-ModusToolbox.pdf#2` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#6` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#56`

## 4. Device Configurator 必知事项

### 4.1 它是 PSoC MCU 项目的核心硬件配置工具

官方文档明确说明，Device Configurator 用于启用和配置 clocks、pins 以及标准 MCU peripherals；在 ModusToolbox 环境中，它是 tools package 的组成部分，而且在 PSoC MCU 这类设备上是必需工具。`docs\MTB_docs\device-configurator.pdf#4`

### 4.2 首次打开项目要先清 Notice List

官方给出的基本流程是：首次打开项目后，先解决 Notice List 里的待处理项，形成有效配置；然后在 Peripherals、Pins、System 等标签页配置硬件；保存后把 `GeneratedSource` 加入构建。`docs\MTB_docs\device-configurator.pdf#11`

### 4.3 `GeneratedSource` 不是可有可无的缓存目录

`GeneratedSource` 承担的是配置生成后的初始化代码与相关输出；如果它没有进入构建，硬件配置就不会真正反映到固件里。`docs\MTB_docs\device-configurator.pdf#11`

### 4.4 问题通常出在资源标签页和提示窗格

`Pins`、`System`、`Peripherals`、`DMA`、`Peripheral-Clocks` 等资源标签页负责核心硬件配置，而 `Notice List` 和 `Code Preview` 则适合定位“配置不合法”或“生成结果与预期不符”的问题。`docs\MTB_docs\device-configurator.pdf#26` `docs\MTB_docs\device-configurator.pdf#49`

## 5. BSP、Makefile 与构建系统

### 5.1 ModusToolbox 不是单体 IDE

官方文档明确说明，ModusToolbox 是一个现代、可扩展的开发环境，工具和库更像一组“mini-products”，有各自的发布节奏与依赖关系。回答工具链问题时，不要把它简化成“某个 IDE 的设置问题”。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#6` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#16`

### 5.2 `make build` 的关键变量不能想当然

官方给出的 `make` 变量里，`TARGET` 用于指定目标板卡/套件（即 BSP），`TOOLCHAIN`、`CONFIG` 等变量则决定工具链与构建配置。也就是说，回答构建问题前，至少要搞清楚 `TARGET/BSP` 和 `TOOLCHAIN`。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`

### 5.3 manifest 会影响你“能看到什么”

ModusToolbox 默认从官方服务器找 manifest；如果团队使用自定义 manifest，那么 BSP、code examples、middleware 的可见范围都会跟着改变。这类问题不能只从当前工程目录本身去推断。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#56`

## 6. 与 DEEPCRAFT / Imagimob 工作流的推荐衔接

### 6.1 DEEPCRAFT 生成代码之后，如何集成到 ModusToolbox 工程

如果用户直接问“DEEPCRAFT 生成代码之后怎么接到 ModusToolbox 工程里”，应把问题拆成两半看：

1. **模型与生成物层**：确认 `mtb_ml_gen/`、模型名、输出目录、推理入口是否正确。`knowledge\ml_workflow.md:117-160` `knowledge\faq.md:41-66`
2. **工程与工具链层**：确认 `TARGET/BSP`、Device Configurator、`GeneratedSource`、Makefile、toolchain 是否一致。`docs\MTB_docs\device-configurator.pdf#11` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`

1. 在 DEEPCRAFT / Imagimob 里完成数据、训练、量化、代码生成。`knowledge\ml_workflow.md:33-135`
2. 回到 ModusToolbox，先确认项目所用 BSP、Toolchain 与编译入口。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`
3. 用 Device Configurator 检查 pins、clocks、peripherals、DMA，并先清掉 Notice List。`docs\MTB_docs\device-configurator.pdf#11`
4. 确认 `GeneratedSource` 已进入工程构建。`docs\MTB_docs\device-configurator.pdf#11`
5. 再集成 `mtb_ml_gen/` 或其他生成代码，并检查 Makefile / 生成目录 / arena / 推理入口。`knowledge\ml_workflow.md:117-160` `knowledge\faq.md:41-66`

## 7. 高频排障检查点

- **构建器/编译器找不到**：优先检查 `TOOLCHAIN` 与 `CY_COMPILER_ARM_DIR` / `CY_COMPILER_LLVM_ARM_DIR`，不要只看最后一条报错。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44` `knowledge\faq.md:8-38`
- **硬件配置改了却不生效**：优先检查 Notice List 是否已清、`GeneratedSource` 是否重新生成并参与构建。`docs\MTB_docs\device-configurator.pdf#11`
- **板卡/项目路径看起来对，但行为还是不对**：优先确认 `TARGET/BSP`，不要把 PSoC Edge 与 PSoC 6 的项目假设混用。`knowledge\faq.md:128-153` `docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`
- **明明是 ML 问题，却去 Device Configurator 里找参数**：先分清这是 library-level configurator 还是 device-level configurator 的问题。`docs\MTB_docs\New-to-ModusToolbox.pdf#2`

## 8. 推荐检索路径

1. 先看 `knowledge\modustoolbox_tools_summary.md`，快速判断问题属于哪一层。
2. 再根据问题类型进入：
   - 工程入口 / BSP / `make`：`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf`
   - 硬件配置 / `GeneratedSource` / Notice List：`docs\MTB_docs\device-configurator.pdf`
   - 新手心智模型 / configurator 分层：`docs\MTB_docs\New-to-ModusToolbox.pdf`
3. 如果问题已经落到具体工程，再继续进入 `knowledge\ml_workflow.md`、`knowledge\faq.md`、`knowledge\troubleshooting_playbook.md` 和对应 README / 源码。
