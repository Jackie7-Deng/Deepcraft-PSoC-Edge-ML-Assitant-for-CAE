# ModusToolbox 与 DEEPCRAFT 机器学习应用说明摘要

**文档**: ML with ModusToolbox™ and DEEPCRAFT™ Studio
**路径**: `docs/application_notes/ml_modustoolbox_imagimob.pdf`
**大小**: 1.92 MB

---

## 文档概述

本应用笔记介绍 ModusToolbox™ 和 DEEPCRAFT™ Studio 的集成工作流，用于在 Infineon MCU 上开发和部署 ML 模型。

---

## 关键内容

### 1. 工作流概述

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  DEEPCRAFT      │    │  Code           │    │  ModusToolbox   │
│  Studio         │───▶│  Generation     │───▶│  Deployment     │
│  (Training)     │    │  (model.c/h)    │    │  (Application)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2. DEEPCRAFT Studio 功能
- 数据采集和标注
- 自动模型训练 (Auto ML)
- 模型评估和优化
- C 代码生成

### 3. ModusToolbox 集成
- ML Configurator 工具
- Tensor Arena 配置
- 优化选项 (Vela 编译器)
- 目标板选择

### 4. 代码生成步骤

| 步骤 | 操作 | 输出 |
|------|------|------|
| 1 | 训练模型 | .h5 / .tflite |
| 2 | 选择目标 | PSoC Edge E8x |
| 3 | 配置优化 | 量化级别 |
| 4 | 生成代码 | model.c, model.h |

### 5. 部署到目标板

```c
// 在 ModusToolbox 项目中使用生成的代码
#include "model.h"

void app_main(void) {
    IMAI_Init();  // 初始化模型

    while(1) {
        // 获取传感器数据
        float sensor_data[IMAI_DATA_IN_COUNT];
        read_sensor(sensor_data);

        // 推理
        float output[IMAI_DATA_OUT_COUNT];
        IMAI_enqueue(sensor_data);

        if(IMAI_dequeue(output) == IMAI_RET_SUCCESS) {
            process_result(output);
        }
    }
}
```

### 6. 优化选项

| 选项 | 说明 | 影响 |
|------|------|------|
| Float32 | 最高精度 | 最大内存 |
| Int16 | 平衡 | 中等内存 |
| Int8 | 最小内存 | 可能精度损失 |
| Vela | NPU 加速 | U55 专用 |

---

## 关键 API 参考

| 函数 | 用途 |
|------|------|
| `IMAI_Init()` | 初始化模型 |
| `IMAI_enqueue()` | 输入数据 |
| `IMAI_dequeue()` | 获取结果 |
| `IMAI_compute()` | 直接计算 |
| `IMAI_finalize()` | 释放资源 |

---

## 检索关键词

### 英文
- ModusToolbox, ML Configurator
- DEEPCRAFT Studio, Imagimob
- Code Generation, model.c, model.h
- Tensor Arena, Vela Compiler
- Edge API, IMAI_*

### 中文
- 模型部署, 代码生成
- 机器学习配置器
- 张量区域, 编译优化
- 边缘 API

---

*摘要创建日期: 2026-03-08*
