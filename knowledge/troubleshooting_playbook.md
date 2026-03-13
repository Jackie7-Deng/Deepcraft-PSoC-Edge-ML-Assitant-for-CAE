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
