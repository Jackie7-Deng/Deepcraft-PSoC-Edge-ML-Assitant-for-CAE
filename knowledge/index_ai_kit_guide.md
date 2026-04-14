# KIT_PSE84_AI 文档入口

**更新日期**: 2026-04-14  
**定位**: 当问题涉及 `KIT_PSE84_AI` 的接口、外设、板级设计文件、摄像头/显示/传感器链路时，先从这里缩小范围。

---

## 1. 主文档

- 用户指南：`docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf`

该文档明确说明它是 **KIT_PSE84_AI PSOC Edge E84 AI Kit guide**，用于说明 kit contents、out-of-box application 和板卡使用方式。  
`docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#1`

---

## 2. 这块板的高价值定位

用户指南在引言页给出的关键板级能力包括：

- Raspberry Pi compatible **MIPI-DSI displays**
- analog and digital microphones
- AIROC `CYW55513IUBGT` Wi-Fi + Bluetooth
- `512-Mbit Quad-SPI NOR Flash`
- `128-Mbit Octal-SPI HYPERRAM`
- on-board `KitProg3`
- JTAG / SWD debug headers
- expansion I/O
- 6-axis IMU
- 3-axis magnetometer
- barometric pressure sensor
- humidity sensor
- RADAR sensor
- 1.8V / 3.3V 电源域

`docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#6`

---

## 3. 如果问题属于哪个方向，优先看哪里

| 问题方向 | 优先文档 |
| --- | --- |
| 套件总览 / 开箱 / 硬件能力 | `infineon-kit-pse84-ai-user-guide-usermanual-en.pdf` |
| 板级连接 / 引脚 / 信号名 | `infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#10` |
| 板卡俯视 / 元件位置 | `infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#15` |
| 原理图 | `docs/kit_guides/KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_schematic.pdf` 或 `.DSN` |
| Layout | `docs/kit_guides/KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_Layout.pdf` 或 `.brd` |
| 制造 / 装配 | `docs/kit_guides/PSOC_Edge_E84_AI_Board_fabrication_drawing.pdf`、`PSOC_Edge_E84_AI_Board_assembly_drawing.pdf` |
| BoM | `docs/kit_guides/PSOC_Edge_E84_AI_Board_PCBA_BoM.xlsx` |
| Gerber / ODB | `docs/kit_guides/PSOC_Edge_E84_AI_Board_gerbers.zip`、`KIT_PSE84_AI_PSOC_Edge_E84_AI_Board_ODB_files.tgz` |

---

## 4. 当前最值得先记住的板级事实

- 这块板是 **PSoC Edge E84 AI Kit**，重点在多媒体、ML 和连接性，不是普通最小系统板。  
  `docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#6`
- 板上同时具备外部 Flash 与外部 RAM，因此回答 XIP、模型放置、显示/摄像头链路时，应优先联动：
  - `knowledge/memory_layout_guide.md`
  - `knowledge/parameters_catalog.md`
  - 本用户指南  
- 用户指南目录已经明确有 audio、radar、IMU、magnetic、humidity、Wi-Fi/BT、I/O expansion 等专题章节。  
  `docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#4` `docs/kit_guides/infineon-kit-pse84-ai-user-guide-usermanual-en.pdf#5`

---

## 5. 当前回答边界

- 本页只做**入口导航**，不展开原理图细节和每个网络名
- 如果问题已经落到具体电路、走线或 pin net，请直接打开对应 schematic / layout 文档，而不是凭摘要猜测
