# ModusToolbox ML 用户指南摘要

**文档**: ModusToolbox™ ML User Guide
**路径**: `docs/application_notes/mtb_ml_user_guide.pdf`
**大小**: 1.04 MB

---

## 文档概述

ModusToolbox™ ML User Guide 提供在 ModusToolbox IDE 中使用机器学习功能的完整指南。

---

## 关键内容

### 1. ML 配置工具

| 工具 | 功能 |
|------|------|
| ML Configurator | 模型导入和配置 |
| ML Model Loader | 运行时模型加载 |
| Vela Compiler | NPU 优化编译 |

### 2. 支持的模型格式
- TensorFlow Lite (.tflite)
- ONNX (.onnx)
- Keras (.h5) - 通过转换

### 3. 项目结构

```
mtb_ml_project/
├── models/
│   └── model.tflite      # 导入的模型
├── Generated/
│   ├── model.c           # 生成的 C 代码
│   └── model.h           # 头文件
├── config/
│   └── ml_config.yml     # ML 配置
└── src/
    └── main.c            # 应用代码
```

### 4. ML Configurator 配置选项

| 配置项 | 选项 |
|--------|------|
| 目标设备 | PSoC 6, PSoC Edge, XMC, TRAVEO |
| 优化级别 | Float32, Int16, Int8 |
| NPU 支持 | Enable/Disable (U55) |
| 内存分配 | Auto/Manual |

### 5. Tensor Arena 配置

```c
// 自动生成的内存配置
#define TENSOR_ARENA_SIZE  (128 * 1024)  // 128 KB

__attribute__((section(".bss.tensor_arena")))
static uint8_t tensor_arena[TENSOR_ARENA_SIZE];
```

### 6. 优化流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  .tflite    │────▶│  Quantize   │────▶│  Vela       │
│  Float32    │     │  Int8/16    │     │  Compile    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 7. 性能优化技巧

| 技巧 | 说明 |
|------|------|
| 使用 Int8 量化 | 减少模型大小 4x |
| 启用 NPU | U55 加速 10-50x |
| 优化 Tensor Arena | 减少内存碎片 |
| 使用 CMSIS-NN | CPU 加速 3-5x |

### 8. 调试支持

- 层级输出可视化
- 性能分析器 (Profiling)
- 内存使用报告
- NPU 使用率统计

---

## API 快速参考

### 初始化和推理

```c
#include "cy_ml_api.h"

// 初始化
cy_rslt_t result = cy_ml_init(&config);

// 推理
cy_ml_invoke(input_tensor, output_tensor);

// 清理
cy_ml_deinit();
```

### 配置结构

```c
cy_ml_config_t config = {
    .model = model_data,           // 模型数据
    .model_size = model_size,      // 模型大小
    .tensor_arena = tensor_arena,  // 内存区域
    .arena_size = TENSOR_ARENA_SIZE,
    .enable_npu = true,            // 启用 NPU
};
```

---

## 检索关键词

### 英文
- ModusToolbox ML, ML Configurator
- Tensor Flow Lite, TFLite, ONNX
- Tensor Arena, Memory Allocation
- Vela Compiler, NPU Optimization
- Quantization, Int8, Float32
- CMSIS-NN, Neural Network

### 中文
- 机器学习配置器
- 张量区域, 内存分配
- 模型量化, 优化编译
- 神经网络加速

---

*摘要创建日期: 2026-03-08*
