# PSoC Edge E8x 数据手册摘要

**文档**: PSoC™ Edge E8x Datasheet
**路径**: `docs/datasheets/psoc_edge_e8x_datasheet.pdf`
**大小**: 4.14 MB

---

## 文档概述

PSoC Edge E8x 系列数据手册提供芯片的电气特性、封装信息和引脚定义。

---

## 关键规格

### 1. 器件系列

| 型号 | CPU | NPU | 目标应用 |
|------|-----|-----|----------|
| E8x2 | Cortex-M33 | - | 入门级 |
| E8x3 | Cortex-M33 | NNLite | ML 推理 |
| E8x5 | Cortex-M55 | NNLite | 高性能 ML |
| E8x6 | Cortex-M55 + Ethos-U55 | U55 | 边缘 AI |

### 2. 电气特性

| 参数 | 最小 | 典型 | 最大 | 单位 |
|------|------|------|------|------|
| VDD | 1.71 | 1.8 | 1.89 | V |
| VDDIO | 1.71 | 3.3 | 3.6 | V |
| 工作温度 | -40 | 25 | 85 | °C |
| Active 电流 | - | - | 150 | mA |
| Sleep 电流 | - | 5 | - | mA |
| Deep Sleep | - | 100 | - | µA |

### 3. 存储器配置

| 类型 | 大小 | 说明 |
|------|------|------|
| SRAM | Up to 2 MB | 分区支持低功耗 |
| RRAM/Flash | Up to 4 MB | 非易失性存储 |

### 4. 时钟规格

| 时钟源 | 频率范围 |
|--------|----------|
| ECO (External Crystal) | 8-32 MHz |
| IMO (Internal Main) | 8 MHz |
| PLL | Up to 400 MHz |
| FLL | Up to 100 MHz |

### 5. 外设清单

- **通信**: UART, SPI, I2C, I2S, CAN
- **模拟**: 12-bit ADC, 12-bit DAC
- **定时器**: TCPWM, RTC, WDT
- **安全**: AES, SHA, TRNG
- **连接**: SDIO, USB

### 6. 封装信息

| 封装 | 引脚数 | 尺寸 |
|------|--------|------|
| TFBGA | 289 | 10x10 mm |
| WLCSP | 196 | 5.5x5.5 mm |

---

## 关键查找表

### 引脚功能速查
| 功能类别 | 引脚组 | 电源域 |
|----------|--------|--------|
| GPIO | P0-P13 | VDDIO |
| Analog | P6, P7 | VDDA |
| Debug | SWD, SWO | VDD |
| USB | D+, D- | VBUS |

### 功耗模式参考
| 模式 | 唤醒时间 | 电流 |
|------|----------|------|
| Active | - | 50-150 mA |
| Sleep | <10 µs | 5 mA |
| Deep Sleep | <100 µs | 100 µA |
| Hibernate | >1 ms | 10 µA |

---

## 检索关键词

### 英文
- Datasheet, Electrical Characteristics, DC Specs
- Operating Conditions, Temperature Range
- Pin Configuration, Ball Map
- Power Consumption, Current Draw
- Package, TFBGA, WLCSP

### 中文
- 数据手册, 电气特性
- 工作条件, 温度范围
- 引脚配置, 封装
- 功耗, 电流消耗

---

*摘要创建日期: 2026-03-08*
