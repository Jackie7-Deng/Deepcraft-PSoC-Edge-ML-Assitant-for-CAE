# ML 工作流程指南

**更新日期**: 2026-03-08

---

## 1. 端到端 ML 开发流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DEEPCRAFT Studio                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐         │
│  │ 数据采集  │ → │ 数据标注  │ → │ 模型训练  │ → │ 模型评估  │         │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘         │
│                                        ↓                             │
│                              ┌──────────┐   ┌──────────┐            │
│                              │   量化    │ → │ 代码生成  │            │
│                              └──────────┘   └──────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        ModusToolbox                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐         │
│  │ 工程集成  │ → │ 编译构建  │ → │ 烧录调试  │ → │ 性能优化  │         │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. 阶段详解

### 2.1 数据采集

**目标**: 收集高质量训练数据

**步骤**:
1. 连接目标设备（PSoC Edge/PSoC 6）
2. 使用 DEEPCRAFT Studio 数据采集功能
3. 配置传感器参数（采样率、量程）
4. 采集多场景数据

**参考**:
- `README_DEEPCRAFT_Data_Collection.md`
- `docs/readmes/README_Device_Audio_Recorder.md` (音频)

**关键参数**:
| 传感器类型 | 采样率 | 精度 |
|------------|--------|------|
| IMU (加速度/陀螺仪) | 100-400 Hz | 16-bit |
| PDM 麦克风 | 16-48 kHz | 16-bit |
| 摄像头 | 15-30 fps | 8-bit 灰度/RGB |

---

### 2.2 数据标注

**目标**: 为数据打标签

**DEEPCRAFT Studio 功能**:
- 自动标注（部分场景）
- 手动标注工具
- 标签管理

---

### 2.3 模型训练

**目标**: 训练/选择适合边缘部署的模型

**支持的任务**:
| 任务类型 | 输入 | 输出 | 示例 |
|----------|------|------|------|
| 分类 | 时序/图像 | 类别概率 | 运动分类、人脸检测 |
| 回归 | 时序/图像 | 连续值 | 位置估计 |
| 检测 | 图像 | 边界框+类别 | 人脸检测 |

**模型选择建议**:
- **IMU 分类**: 1D CNN / LSTM
- **音频分类**: MFCC + CNN
- **视觉**: MobileNet / 轻量 CNN

---

### 2.4 模型评估

**关键指标**:
| 指标 | 说明 | 目标 |
|------|------|------|
| 准确率 | 分类正确率 | >90% |
| 精确率/召回率 | 类别平衡 | 视应用 |
| 推理时间 | 单次推理耗时 | <100ms |
| 模型大小 | Flash 占用 | <100KB |

---

### 2.5 量化

**目标**: 降低模型大小和推理时间

**量化类型**:
| 类型 | 精度 | 大小 | 精度损失 |
|------|------|------|----------|
| float32 | 32-bit | 100% | 无 |
| int16 | 16-bit | 50% | 小 |
| int8 | 8-bit | 25% | 中等 |

**DEEPCRAFT 量化配置**:
- 混合精度量化
- 层级量化控制

**参考**:
- `docs/application_notes/mtb_ml_user_guide.pdf` 量化章节

---

### 2.6 代码生成

**DEEPCRAFT Studio 生成**:
```
mtb_ml_gen/
├── mtb_ml_models/
│   └── *_tflm_model_float.c      # 模型权重
├── mtb_ml_regression_data/
│   └── *_tflm_*_data_float.c     # 测试数据
└── info/
    ├── *_model_metrics.json       # 模型指标
    ├── *_ops_metrics.json         # 算子统计
    └── *_tensor_arena_size.txt    # Arena 大小建议
```

**关键文件**:
- `*_tensor_arena_size.txt` - 内存分配依据

---

### 2.7 ModusToolbox 工程准备与集成

**ModusToolbox 集成步骤**:

1. 先确认目标 BSP / `TARGET` 与 toolchain，不要在平台边界不清的情况下继续集成。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`
2. 打开 Device Configurator，先清 `Notice List`，再检查 Pins / System / Peripherals / DMA / Clocks。`docs\MTB_docs\device-configurator.pdf#11` `docs\MTB_docs\device-configurator.pdf#49`
3. 保存配置，确认 `GeneratedSource` 已进入构建。`docs\MTB_docs\device-configurator.pdf#11`
4. 复制 `mtb_ml_gen/` 到工程目录。
5. 配置 `Makefile` 包含源文件，并同步核对模型名、目录、推理引擎等关键参数。`knowledge\faq.md:41-66`
6. 设置 tensor arena 大小。
7. 调用推理 API。
8. 用 `make build` / `make program` 做最小验证。`docs\MTB_docs\infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf#44`

**代码示例**:
```c
#include "mtb_ml_models/IMAGIMOB_MODEL_tflm_model_float.h"

// Tensor arena 配置
#define TENSOR_ARENA_SIZE  (XX * 1024)  // 根据生成的建议值

// 推理
mtb_ml_model_t model;
mtb_ml_model_init(&model, model_data, arena, TENSOR_ARENA_SIZE);
mtb_ml_model_run(&model, input, output);
```

**参考工程**:
- `Machine_Learning_Imagimob_MTBML_Deploy/source/inference.c`
- `knowledge\modustoolbox_tools_summary.md`

---

### 2.8 部署与调试

**烧录步骤**:
1. 选择目标 BSP
2. 编译工程
3. 烧录程序
4. 验证功能

**调试要点**:
- 串口打印推理结果
- GPIO 翻转测量时间
- 确认 NPU 使能（如适用）

---

## 3. 常见问题

### Q: Tensor arena 大小如何确定？
A: 参考 `mtb_ml_gen/info/*_tensor_arena_size.txt`，实际大小需要考虑对齐和运行时开销，建议预留 20% 余量。

### Q: int8 量化后精度下降明显怎么办？
A: 1) 检查量化校准数据是否覆盖所有场景；2) 考虑混合精度；3) 增加训练数据。

### Q: 如何启用 NPU 加速？
A: PSoC Edge E8x 系列支持 NPU，需要：
1. 正确配置 BSP
2. 使用支持的算子
3. 调用 NPU API

---

## 4. 性能优化检查清单

- [ ] 模型量化 (int8/int16)
- [ ] Tensor arena 大小优化
- [ ] NPU 使能（如适用）
- [ ] 输入预处理优化
- [ ] 内存对齐
- [ ] 批处理（如适用）

---

*详细排查请参考 `troubleshooting_playbook.md`*
