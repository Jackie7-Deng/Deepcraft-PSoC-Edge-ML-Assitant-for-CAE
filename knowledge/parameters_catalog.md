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
