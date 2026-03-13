# PSoC Edge E84 Evaluation Kit User Guide 索引

**文档**: KIT_PSE84_EVAL User Guide
**路径**: `docs/kit_guides/kit_pse84_eval_user_guide.pdf`
**大小**: 32.8 MB

---

## 文档结构概述

KIT_PSE84_EVAL 是 PSoC Edge E84 评估套件的用户指南，涵盖硬件配置、外设使用和快速入门。

---

## 1. Kit Overview

### 1.1 Kit Contents
- PSoC Edge E84 Evaluation Board
- USB cables
- Quick start guide

### 1.2 Key Features
| 特性 | 说明 |
|------|------|
| MCU | PSoC Edge E84 (E8x2/E8x3/E8x5/E8x6) |
| Memory | 512-Mbit QSPI Flash, 128-Mbit Octal RAM |
| Connectivity | Wi-Fi & Bluetooth (CYW55513) |
| Debug | KitProg3 (SWD) |
| Sensors | IMU, Magnetometer, Microphone |

---

## 2. Hardware Configuration

### 2.1 Connectors
| 连接器 | 功能 | 位置 |
|--------|------|------|
| J1 | KitProg3 USB | Debug/Programming |
| J2 | USB Device | Application USB |
| J3 | Power | External power input |
| J4-J6 | GPIO Headers | IO expansion |

### 2.2 Jumpers
| 跳线 | 默认 | 功能 |
|------|------|------|
| J10 | Open | Power source selection |
| J11 | Closed | Debug enable |

### 2.3 LEDs and Buttons
| 元件 | 颜色 | 功能 |
|------|------|------|
| LED1 | Green | Power/Status |
| LED2-LED4 | RGB | User LEDs |
| SW1 | - | Reset button |
| SW2 | - | User button |

---

## 3. On-Board Peripherals

### 3.1 Sensors
| 传感器 | 型号 | 接口 |
|--------|------|------|
| IMU | BMI323 | I2C/SPI |
| Magnetometer | BMM350 | I2C |
| Microphone | ICS-43434 | I2S/PDM |
| Radar | BGT60TR13C | SPI |

### 3.2 Connectivity
| 模块 | 型号 | 接口 |
|------|------|------|
| Wi-Fi/BT | CYW55513IUBGT | UART/SDIO |

### 3.3 Memory
| 类型 | 大小 | 接口 |
|------|------|------|
| QSPI Flash | 512 Mbit | QSPI |
| Octal RAM | 128 Mbit | Octal SPI |

---

## 4. Getting Started

### 4.1 Hardware Setup
1. Connect J1 (KitProg3 USB) to PC
2. Verify LED1 (green) is blinking
3. Wait for driver installation

### 4.2 Software Setup
1. Install ModusToolbox™ 3.8+
2. Install KitProg3 drivers
3. Verify device in Device Manager

### 4.3 First Program
1. Open ModusToolbox™
2. Create new project → Select KIT_PSE84_EVAL
3. Build and Program

---

## 5. KitProg3 Debugger

### 5.1 Modes
- **CMSIS-DAP**: Default debug mode
- **BULK**: High-speed programming mode

### 5.2 LED Indicators
| LED 状态 | 含义 |
|----------|------|
| Solid | Connected |
| Blinking | enumerating/ready |
| Off | Not powered |

### 5.3 Troubleshooting
| 问题 | 解决方案 |
|------|----------|
| Device not found | Reinstall drivers |
| Programming failed | Check mode switch |
| Debug connection lost | Reset KitProg3 |

---

## 6. Power Management

### 6.1 Power Sources
1. KitProg3 USB (J1)
2. USB Device (J2)
3. External power (J3)

### 6.2 Power Modes
| 模式 | 电流 | 唤醒源 |
|------|------|--------|
| Active | ~50 mA | - |
| Sleep | ~5 mA | GPIO, Timer |
| Deep Sleep | ~100 µA | GPIO |
| Hibernate | ~10 µA | Reset only |

---

## 7. Pin Assignments

### 7.1 Arduino Compatible Headers
| Header | Pin | Function |
|--------|-----|----------|
| D0-D13 | Digital | GPIO/PWM |
| A0-A5 | Analog | ADC inputs |
| SDA/SCL | I2C | I2C bus |
| MOSI/MISO/SCK | SPI | SPI bus |

### 7.2 Kit-Specific Pins
| Pin | Function | Notes |
|-----|----------|-------|
| P5.0 | User LED | Active high |
| P5.1 | User Button | Active low |
| P10.0 | IMU INT | Interrupt |

---

## 8. Schematics Reference

### 8.1 Power Schematic
- Section in PDF: Power Distribution
- Key components: LDO regulators, DC-DC converter

### 8.2 Sensor Connections
- Section in PDF: Sensor Subsystem
- Bus routing: I2C mux, SPI chip selects

---

## 检索关键词

### 英文
- KitProg3, CMSIS-DAP, Debug, Programming
- KIT_PSE84_EVAL, Evaluation Kit
- BMI323, BMM350, IMU, Magnetometer
- CYW55513, Wi-Fi, Bluetooth
- QSPI Flash, Octal RAM
- Power modes, Low power

### 中文
- 评估套件
- 调试器, 编程
- 惯性测量单元, 磁力计
- 无线网络, 蓝牙
- 闪存, 内存
- 功耗模式, 低功耗

---

## 与 E84 AI Kit 的关系

| 特性 | E84 Evaluation Kit | E84 AI Kit |
|------|-------------------|------------|
| 传感器 | IMU, Mag, Mic | IMU, Mag, Mic, Radar, Pressure, Humidity |
| Camera | 无 | OV7675 DVP |
| 重点 | 基础评估 | ML/AI 开发 |
| 文档 | 本索引 | ingest/html/psoc_edge_e84_ai_kit.md |

---

*索引创建日期: 2026-03-08*
*注: 此索引为结构概览。具体电路和配置请查阅完整 PDF 文档。*
