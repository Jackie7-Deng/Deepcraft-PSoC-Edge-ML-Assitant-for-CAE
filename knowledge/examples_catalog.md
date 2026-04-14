# 示例工程目录

**更新日期**: 2026-03-25

---

> 说明：示例 README 已统一以 `docs/readmes/` 下的归档副本作为引用入口。

## 1. 机器学习

### 1.1 MTBML Deploy - Imagimob 模型部署
| 属性 | 值 |
|------|-----|
| **工程路径** | `Machine_Learning_Imagimob_MTBML_Deploy/` |
| **README** | `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md` |
| **目标硬件** | CY8CKIT-062S2-AI (PSoC 6) |
| **功能描述** | 演示如何将 Imagimob/DEEPCRAFT 训练的模型部署到 ModusToolbox 工程 |
| **ML 类型** | IMU 分类 + PDM 音频分类 |
| **量化格式** | float32 (可配置 int8) |
| **关键入口** | `source/main.c`, `source/inference.c` |
| **生成代码** | `mtb_ml_gen/mtb_ml_models/IMAGIMOB_MODEL_tflm_model_float.c` |
| **常见问题** | tensor arena 大小配置、模型版本兼容性 |

### 1.2 Face ID Demo - 人脸识别
| 属性 | 值 |
|------|-----|
| **工程路径** | `PSOC_Edge_Machine_Learning_Face_ID_Demo/` |
| **README** | `docs/readmes/README_Machine_Learning_Face_ID_Demo.md` |
| **目标硬件** | KIT_PSE84_EVAL_EPC2 (PSoC Edge E84) |
| **功能描述** | 人脸检测与识别演示，使用 NPU 加速 |
| **ML 类型** | 视觉 - 人脸检测/识别 |
| **关键入口** | `application_code/source/` |
| **硬件依赖** | 摄像头模块、LCD 显示屏 |
| **设计文档** | `docs/design_and_implementation.md` |

---

## 2. DEEPCRAFT 集成示例

### 2.1 数据采集
| README | 描述 |
|--------|------|
| `docs/readmes/README_DEEPCRAFT_Data_Collection.md` | DEEPCRAFT Studio 数据采集指南 |

### 2.2 运动模型部署
| README | 描述 |
|--------|------|
| `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md` | IMU/运动传感器模型部署 |

### 2.3 视觉模型部署
| README | 描述 |
|--------|------|
| `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md` | 摄像头/视觉模型部署 |

---

## 3. 音频相关

### 3.1 音频增强
| README | 描述 |
|--------|------|
| `docs/readmes/README_Audio_Enhancement.md` | 音频增强/降噪处理 |

### 3.2 设备音频录制
| README | 描述 |
|--------|------|
| `docs/readmes/README_Device_Audio_Recorder.md` | PDM/I2S 音频录制 |

### 3.3 语音助手
| README | 描述 |
|--------|------|
| `docs/readmes/README_Voice_Assistant_Deployment.md` | 语音助手唤醒词/命令词 |

### 3.4 异常振动检测
| README | 描述 |
|--------|------|
| `docs/readmes/README_AnomalousVibrationDetection.md` | 基于振动/声音的异常检测 |

补充训练资料：`docs/机器震动异常检测模型训练指南.md`

---

## 4. 图形界面

### 4.1 LVGL Smartwatch Demo
| README | 描述 |
|--------|------|
| `docs/readmes/README_LVGL_Smartwatch_Demo.md` | LVGL 智能手表 GUI 演示，支持 AMOLED 圆屏 |

### 4.2 VGLite API
| README | 描述 |
|--------|------|
| `docs/readmes/README_Graphics_using_VGLite_API.md` | VGLite 2D 图形 API |

### 4.3 显示驱动
| README | 描述 |
|--------|------|
| `docs/readmes/README_Waveshare_Display_Driver.md` | Waveshare 4.3" DSI 显示屏驱动库 |

---

## 5. 系统功能

### 5.1 空应用模板
| README | 描述 |
|--------|------|
| `docs/readmes/README_Empty_Application.md` | 基础工程模板 |

### 5.2 UART DMA
| README | 描述 |
|--------|------|
| `docs/readmes/README_UART_transmit_and_receive_with_DMA.md` | UART DMA 收发 |

### 5.3 文件系统
| README | 描述 |
|--------|------|
| `docs/readmes/README_device_File_system_FreeRTOS.md` | FreeRTOS + 文件系统 |

---

## 6. 快速参考表

| 示例类型 | 推荐入口 | 硬件要求 |
|----------|----------|----------|
| ML 入门 | MTBML_Deploy | CY8CKIT-062S2-AI |
| NPU 加速 | Face_ID_Demo | KIT_PSE84_EVAL |
| 音频采集 | Audio_Recorder | 需要 PDM 麦克风 |
| 视觉应用 | Face_ID_Demo | 需要摄像头 |
| 图形 UI | LVGL_Smartwatch_Demo | 需要 LCD |

---

*更新日期: 2026-03-25*
