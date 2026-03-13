# DEEPCRAFT 语音助手用户指南摘要

**文档**: DEEPCRAFT™ Voice Assistant User Guide
**路径**: `docs/application_notes/deepcraft_voice_assistant_user_guide.pdf`
**大小**: 1.32 MB

---

## 文档概述

本用户指南介绍如何使用 DEEPCRAFT™ Studio 构建语音助手应用，包括关键词检测 (KWS) 和命令识别。

---

## 关键内容

### 1. 应用场景
- 智能家居控制
- 车载语音助手
- 工业设备语音控制
- 可穿戴设备语音唤醒

### 2. 开发流程

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  录制语音    │───▶│  标注数据    │───▶│  训练模型    │
│  关键词样本  │    │  分类标签    │    │  KWS 模型    │
└──────────────┘    └──────────────┘    └──────────────┘
                                              │
                                              ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  部署到      │◀───│  生成 C 代码 │◀───│  评估模型    │
│  PSoC Edge   │    │  优化量化    │    │  准确率测试  │
└──────────────┘    └──────────────┘    └──────────────┘
```

### 3. 音频配置

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 采样率 | 16 kHz | 语音识别标准 |
| 位深 | 16-bit | PCM 格式 |
| 帧长 | 25 ms | 特征提取窗口 |
| 帧移 | 10 ms | 窗口重叠 |
| MFCC 数量 | 13-40 | 特征维度 |

### 4. 支持的麦克风类型
- PDM 数字麦克风
- I2S MEMS 麦克风
- 模拟麦克风 + ADC

### 5. 预处理流程

```
Raw Audio → Pre-emphasis → Framing → Windowing → FFT → MFCC → Model
```

### 6. 部署参数

| 参数 | 典型值 |
|------|--------|
| 模型大小 | 50-200 KB |
| 推理延迟 | 10-50 ms |
| RAM 使用 | 10-30 KB |
| 检测延迟 | <500 ms |

### 7. 代码示例

```c
// 音频缓冲和推理
#define FRAME_SIZE 160  // 10ms @ 16kHz
#define WINDOW_SIZE 400 // 25ms @ 16kHz

float audio_buffer[WINDOW_SIZE];
float mfcc_features[13 * NUM_FRAMES];

void process_audio(void) {
    // 1. 读取音频数据
    read_mic_data(audio_buffer);

    // 2. 提取 MFCC 特征 (在模型预处理中)
    // 3. 推理
    float output[NUM_KEYWORDS];
    IMAI_enqueue(mfcc_features);
    IMAI_dequeue(output);

    // 4. 检测结果
    int detected = argmax(output);
    if (output[detected] > THRESHOLD) {
        execute_command(detected);
    }
}
```

---

## 关键词设计建议

| 类型 | 示例 | 建议 |
|------|------|------|
| 唤醒词 | "Hey Assistant" | 3-4 音节 |
| 命令词 | "Turn on light" | 短促清晰 |
| 否定词 | Background noise | 用于训练 |

---

## 检索关键词

### 英文
- Voice Assistant, Keyword Spotting, KWS
- Wake Word Detection, Command Recognition
- MFCC, Audio Preprocessing
- PDM Microphone, I2S Audio
- Speech Recognition, Voice Control

### 中文
- 语音助手, 关键词检测
- 唤醒词, 命令识别
- 音频预处理, 特征提取
- 语音控制

---

*摘要创建日期: 2026-03-08*
