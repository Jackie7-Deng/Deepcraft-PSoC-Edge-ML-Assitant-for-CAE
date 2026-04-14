# PSoC Edge DeepCraft AI 助手  Community / Case 经验沉淀

（本文件内容由 MCP 搜索后自动填充，见本次 MCP 验证步骤）

## Community 主题

## 社区主题 [1]：PSoC Edge 模型部署与外部存储布局

### 核心结论
- 当问题落到“模型放哪、固件放哪、运行时 buffer 放哪”时，社区的直接答复通常不是在帖子里展开，而是回指官方 whitepaper 的 memory placement 章节。
- `PSoC Edge MTBML model deploy` 这类 query 的搜索结果以 PDF、GitHub 示例和产品页为主，真正有工程价值的社区帖较少，因此应结合本地 README / kit guide / whitepaper 一起回答。
- 对 PSoC Edge E84 EVK，外部存储布局问题不宜仅凭套件丝印或器件列表推断，建议回到 memory placement 文档确认模型、镜像和运行时数据的放置策略。

### 典型帖子摘要
| 帖子标题/URL | 问题 | 解决方案 | 适用条件 |
|-------------|------|----------|---------|
| [Clarification on multiple external memories on PSOC™ Edge E84 EVK and their roles](https://community.infineon.com/t5/PSOC-Edge/Clarification-on-multiple-external-memories-on-PSOC-Edge-E84-EVK-and-their-roles/td-p/1187140) | 询问 Octal / Quad SPI Flash 的角色、ML 模型存储位置、固件和运行时 buffer 放哪 | 官方答复直接指向 whitepaper `benchmarking-the-psoc-edge-mcu` 的 `2.1.2 Memory placement` | PSoC Edge E84 EVK、需要回答模型/镜像/缓冲区放置问题 |

### 已知风险/注意事项
- 该主题的 community 搜索结果里，文档类结果明显多于讨论帖，单靠社区贴子很难得到完整内存布局答案。
- 社区贴本身没有给出具体 memory map 数值；若需精确地址或容量边界，应回到本地 kit guide / datasheet / architecture RM。

### 本次使用的 query 序列
1. `PSoC Edge MTBML model deploy`
2. `ModusToolbox ML Imagimob inference PSoC`

## 社区主题 [2]：ModusToolbox 构建失败与 flash overflow

### 核心结论
- 对“工程刚创建就 build failed”的通用问题，社区的首选动作是进入 `modus shell`，在含 `Makefile` 的工程目录执行 `make getlibs`，然后 `make clean && make build`。
- 对 PSoC 6 双核项目的 flash overflow，社区 KBA 明确给出三连改法：改 CM0+ linker 的 flash `LENGTH`、改 CM4 linker 的 `FLASH_CM0P_SIZE`、再改 `psoc6.h` 中的 CM4 app start address。
- 这类问题往往不是模型逻辑错误，而是依赖未拉齐或双核 flash 配置不一致。

### 典型帖子摘要
| 帖子标题/URL | 问题 | 解决方案 | 适用条件 |
|-------------|------|----------|---------|
| [ModusToolbox Build error](https://community.infineon.com/t5/PSOC-6/ModusToolbox-Build-error/td-p/636941) | 新建 ModusToolbox 工程后出现编译错误 | 在 `modus shell` 进入工程目录，先 `make getlibs`，再 `make clean && make build`；必要时分享工程继续看 | PSoC 6 / MTB 工程创建后缺库、依赖未同步 |
| [Flash overflow: Change the PSoC™ 6 CM0+ flash allocation in ModusToolbox™ 2.4](https://community.infineon.com/t5/Knowledge-Base-Articles/Flash-overflow-Change-the-PSoC-6-CM0-flash-allocation-in-ModusToolbox-2-4/ta-p/336607) | CM0+ 代码超出 flash，编译后又与 CM4 区域冲突 | 同步调整 CM0+ linker、CM4 linker 和 `psoc6.h` 的起始地址 | PSoC 6 双核工程、flash 分配不足或重分配 |

### 已知风险/注意事项
- `make getlibs` 只能解决缺库 / 依赖未拉齐问题，不能替代对 `TARGET/BSP`、toolchain 和 linker 脚本的检查。
- KBA 示例基于 ModusToolbox 2.4 与 CY8CKIT-062-BLE；迁移到其他工程时应先确认双核 flash 布局假设一致。

### 本次使用的 query 序列
1. `PSoC 6 ModusToolbox build error`
2. `MTB linker error flash overflow PSoC`

## 社区主题 [3]：Face ID 与多模型组合的工程边界

### 核心结论
- Face ID Demo 内部预编译库和 `ifx_face_id_inference()` 的细节，社区答复通常回指 GitHub README 与 `docs/design_and_implementation.md`，而不是在帖子里逐项解释内部模型结构。
- 把语音/关键词检测与 Face ID 组合到同一套 PSoC Edge E84 工程是“可行但未正式验证”的路径，核心瓶颈在共享核心与共享内存区域的管理。
- 用户实测把关键词模型放在 CM33、Face ID 放在 CM55 可以跑起来，但命中率可能显著下降，说明多模型组合时除了内存，还要警惕模型版本、EAP 版本和运行核心选择对精度的影响。

### 典型帖子摘要
| 帖子标题/URL | 问题 | 解决方案 | 适用条件 |
|-------------|------|----------|---------|
| [Support Request: PSOC Edge E84 Face ID Demo – ifx_face_id_inference Details and Custom Model Integration](https://community.infineon.com/t5/PSOC-Edge/Support-Request-PSOC-Edge-E84-Face-ID-Demo-ifx-face-id-inference-Details-and/td-p/1187681) | 想了解 `ifx_face_id_inference()` 内部模型、输入输出和自定义模型替换 | 官方回复直接指向 GitHub README 与 `docs/design_and_implementation.md` | Face ID Demo、需要了解预编译库与设计说明 |
| [combine the demo codes of voice assistant with the face ID recognition for PSOC Edge E84](https://community.infineon.com/t5/PSOC-Edge/combine-the-demo-codes-of-voice-assistant-with-the-face-ID-recognition-for-PSOC/td-p/1197475) | 想把 voice assistant 与 Face ID 放进同一工程，遇到 LLVM linker overflow | 官方说明“可行但未正式测试”，建议以 local voice code example 为 base，再叠加 Face ID，并做好 memory management | PSoC Edge E84，多模型 / 多核组合、内存溢出、命中率下降 |

### 已知风险/注意事项
- 社区对 Face ID 内部模型的公开信息有限；若用户要求内部网络结构、完整 API 实现或替换约束细节，仍需回到仓库 README 和 design 文档。
- 组合工程里出现的 `.cy_xip` / `.heap` / `m55_data_secondary` overflow 不能简单按单模型示例的 linker 假设处理。

### 本次使用的 query 序列
1. `PSoC Edge machine learning camera face detection`
2. `PSoC Edge Face ID demo`

## Case 主题

## 社区主题 [4]：Case System — MTB-ML / DEEPCRAFT 模型导入与部署异常（来源：Case System）

### 核心结论
- `MTB-ML tools` 导入自训练模型时报 `too many indices for array` 时，case 反馈显示先按 `ml-user-guider` 规范数据和模型格式后，可至少生成基础 `.c/.h` 文件。
- 即便基础转换通过，真实模型仍可能包含当前 Edge 工具链不支持的算子；这类问题不能只靠修改输入维度或路径解决。
- 对现成模型部署到 `PSOC_Edge_Machine_Learning_Imagimob_MTBML_Deploy`，官方 case 回复强调预处理代码来自 DeepCraft Studio，用于保证部署端输入与训练时一致。

### 典型帖子摘要
| 帖子标题/URL | 问题 | 解决方案 | 适用条件 |
|-------------|------|----------|---------|
| `IFX-250911-1842110` / PSOC Edge - 使用MTB - ML工具导入自己训练的模型跟数据时报错 | 导入模型时报 `IndexError: too many indices for array` | 先按 `ml-user-guider` 规范数据和模型格式；简单模型可转出 `.c/.h`，若仍失败，继续排查不支持算子 | PSoC Edge、MTB-ML、自训练模型导入 |
| `IFX-250728-1789988` / Deploy existing model to PSOC_edge | 现成模型部署到 Imagimob MTBML Demo 时，疑惑为什么还需要 DeepCraft 预处理代码 | case 回复说明预处理代码用于保证输入格式/尺度与训练数据一致，并给出 DeepCraft preprocessing 文档链接 | `PSOC_Edge_Machine_Learning_Imagimob_MTBML_Deploy`、现成模型接入 |
| `IFX-260325-2078302` / PSOC E84 PSOC_Edge_Machine_Learning_DEEPCRAFT问题 | Vision 部署只识别 index=0、屏幕闪烁、J30 双 Type-C 识别问题、国内代理拉到旧工程 | 当前可见记录只有问题描述，没有提取到明确闭环动作 | PSoC Edge E84、Vision / Data Collection / Project Creator 代理问题 |

### 已知风险/注意事项
- Case System 中部分记录只有问题描述，discussion 未完全提取到闭环过程，不能把“已关闭”直接当作“根因明确”。
- 支持算子矩阵、预处理生成细节仍应回到本地 ML 用户指南与 DeepCraft 文档交叉确认。

### 本次使用的 query 序列
1. `PSoC Edge ML inference accuracy`

## 社区主题 [5]：Case System — 编程 / 烧录失败与工具版本问题（来源：Case System）

### 核心结论
- 对 PSoC Edge E84 `Can't find target/cat1d.cfg` 类烧录失败，case 已给出明确经验：PSoC Edge EAP 需要 `ModusToolbox Programming tools 1.2.1`，并建议卸载 `1.3.1` 后再试。
- 对 PSoC 6 / SWD acquire 失败、`cannot read IDR` 这类问题，至少有 case 显示 MiniProg4 路径失败，但改用 J-Link 后成功，说明问题可能在 probe / acquire 路径而不在目标板供电。
- 因此烧录失败应先分离“工具版本 / target cfg 缺失”和“物理调试链 / probe acquire 失败”两类根因。

### 典型帖子摘要
| 帖子标题/URL | 问题 | 解决方案 | 适用条件 |
|-------------|------|----------|---------|
| `IFX-250322-1644913` / PSoC Edge E84 EVK Flashing Problem | `Can't find target/cat1d.cfg`，Program 失败 | 使用 `ModusToolbox Programming tools 1.2.1`，并卸载 `1.3.1`；用户回报“it works” | PSoC Edge E84、EAP、OpenOCD target 配置缺失 |
| `IFX-251020-1883737` / Programming PSOC6 via SWD with miniProg4 | `acquire_psoc request failed`、`cannot read IDR` | case 记录显示改用 J-Link 后可刷写，MiniProg4 未检测到 SWD 输入 | PSoC 6、自定义板、MiniProg4 / SWD acquire 失败 |

### 已知风险/注意事项
- 不同板卡 / EAP / Progtools 版本的要求可能不同，不能把 `1.2.1` 外推成全部 PSoC Edge 的唯一答案。
- Case 里对 MiniProg4 问题的最终根因并不充分，只能确定 J-Link 是已验证绕过路径。

### 本次使用的 query 序列
1. `PSoC 6 ModusToolbox programming failed KitProg`

## 社区主题 [6]：Case System — 资源与多模型组合的容量边界（来源：Case System）

### 核心结论
- 当搜索“RAM / flash size limitation”时，Case System 很容易返回更广义的 machine learning / PSoC Edge 记录，因此需要人工筛选真正相关的容量问题。
- 已检到的多模型 / 多工程相关 case 和 community 线程都指向同一类风险：模型组合、XIP 区与 secondary data region 会成为首要容量瓶颈。
- 当前 Case System 在该主题下能直接提取到的高价值记录较少，更多还是需要结合 community 线程和本地 linker / README 证据判断。

### 典型帖子摘要
| 帖子标题/URL | 问题 | 解决方案 | 适用条件 |
|-------------|------|----------|---------|
| `IFX-241211-1541757` / PSOC edge with the machine learning pack | 询问 PSoC Edge E81 是否兼容 ModusToolbox 与 machine learning pack | 反映用户常先卡在兼容性与资料入口，而不是具体内存数值 | PSoC Edge 早期评估、资料可得性 |
| `IFX-250804-1798945` / Machine learning example for Psoc e84 evk | 询问如何把模型转换为 U55 优化版本并集成上板 | 说明早期资料中 U55 优化 / 集成流程文档不足 | PSoC Edge E84、U55 优化部署 |

### 已知风险/注意事项
- 本主题两轮搜索没有提取到专门针对“RAM flash size limitation”的高质量闭环 case，说明 Case 侧对此类问题的召回不稳定。
- 若后续需要更强覆盖，建议继续扩展 query，或在本地知识库补充 linker map / memory placement 专题。

### 本次使用的 query 序列
1. `PSoC machine learning RAM flash size limitation`
