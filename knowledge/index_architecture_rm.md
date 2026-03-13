# PSoC Edge E8x 架构参考手册索引

**文档**: PSOC™ Edge E8x2, E8x3, E8x5, E8x6 Architecture Reference Manual
**版本**: 002-38331 Rev. *A
**日期**: 2025-11-18
**路径**: `docs/trm_aum/psoc_edge_e8x_architecture_rm.pdf`
**大小**: 11.6 MB

---

## 目录概览

### 1. 关于本文档（p.1）
- 1.3.1 简介（p.33）
- 1.3.2 详细特性（p.33）
- 1.3.2.1 架构（p.34）

### 2. CPU 子系统（CPUSS）（p.47）
- 2.3 Secure Enclave (p.48)
- 2.4 SYSCPUSS (p.49)
- 2.5 APPCPUSS (p.50)
- 2.5 NPUSS (p.51)

### 3. ML Capability (using NPUSS and APPCPUSS) (p.54) ⭐ ML核心章节
- 3.1 地址与内存映射（p.55）
- 3.1.2 等待周期与延迟（p.60）
- 3.2 总线基础结构（p.70）
- 3.6 总线主设备外设（p.79）
  - 3.6.1 HPDMA 与 DMA 控制器（p.79）
  - 3.6.2 U55 NPUSS (p.79) ⭐ NPU
  - 3.6.7 NNLite (p.80) ⭐ 神经网络加速
  - 3.6.8 Ethernet (p.80)

### 4. 处理器间通信（IPC）（p.81）
- 4.5 消息传递（p.85）

### 5-7. 存储子系统
- 5. SRAM 控制器（p.90）
- 6. 系统 SRAM（p.92）
  - 6.4 时钟（p.95）
  - 6.4.1 功耗模式（p.95）
- 7. 非易失性存储（NVM）/ RRAM（p.98）
  - 7.1.4 RRAM 控制器（p.102）
  - 7.1.6 功耗模式（p.104）

### 8. 中断与异常（p.105-136）
- 8.4 架构（p.108）
- 8.5 中断源（p.115）
- 8.11 中断与低功耗模式（p.135）

### 9. 故障监控（p.137）

### 10. 高性能 DMA（HPDMA - AXI DMAC）（p.162）
- 10.3 通道（p.163）
- 10.4 描述符（p.165）
- 10.5 描述符配置（p.169）

### 11. 直接存储器访问（DMA - DW）（p.177）

### 12-16. 系统资源
- 12. 触发多路复用器（p.xx）
- 13. 程序与调试接口（p.xx）
- 14. 保护单元（p.xx）
- 15. 加密加速器（p.xx）
- 16. 神经网络加速器（NNLite）（p.xx）⭐

### 17-18. 外设
- 17. 设备功耗模式（p.xx）
- 18. 系统资源子系统（SRSS）（p.xx）

---

## 主题 → 章节 → 页码 映射

### ML/NPU 相关 ⭐ (最高优先)

| 主题 | 章节 | 页码 | 说明 |
|------|------|------|------|
| **NPUSS 架构** | §2.5, §3.6.2 | p.51, p.79 | U55 NPU 子系统 |
| **ML Capability** | §3 | p.54 | ML 能力总览 |
| **NNLite** | §3.6.7 | p.80 | 神经网络加速器 |
| **Cortex-M55** | §3.2.2.4-5 | p.75 | APPCPU (带Helium) |
| **Ethos-U55** | §3.6.2 | p.79 | NPU 硬件 |

### 内存/Arena 相关

| 主题 | 章节 | 页码 | 说明 |
|------|------|------|------|
| **SRAM 架构** | §5, §6 | p.90-96 | SRAM 控制器与系统 SRAM |
| **Memory Map** | §3.1 | p.55 | 地址映射 |
| **Wait States** | §3.1.2, §6.1 | p.60, p.91 | 访问延迟 |
| **RRAM/NVM** | §7 | p.98-106 | 非易失性存储 |
| **Power Partition** | §5.3, §6.5 | p.90, p.96 | 功耗分区 |

### 启动/Flash 相关

| 主题 | 章节 | 页码 | 说明 |
|------|------|------|------|
| **NVM Regions** | §7.1.3 | p.99 | RRAM 区域划分 |
| **MAIN NVM** | §7.1.4.1 | p.100 | 主 Flash 区域 |
| **PROTECTED NVM** | §7.1.4.1.1 | p.101 | 受保护区域 |
| **OTP Region** | §7.1.4.1.2 | p.102 | 一次性编程区 |
| **Direct Read** | §8.1 | p.105 | 直接读取 |
| **Indirect Write** | §8.2 | p.106 | 间接写入 |

### 调试相关

| 主题 | 章节 | 页码 | 说明 |
|------|------|------|------|
| **Debug Interface** | §13 | - | 调试接口 |
| **Fault Monitoring** | §9 | p.137 | 故障监控 |
| **Exception Handling** | §8.4.2 | p.109 | 异常处理 |

### 时钟/电源相关

| 主题 | 章节 | 页码 | 说明 |
|------|------|------|------|
| **Power Modes** | §6.4.1, §7.1.6 | p.95, p.104 | 功耗模式 |
| **Device Power** | §17 | - | 设备功耗模式 |
| **SRSS** | §18 | - | 系统资源子系统 |
| **Low Power + IRQ** | §8.11 | p.135 | 低功耗中断 |

### DMA/中断相关

| 主题 | 章节 | 页码 | 说明 |
|------|------|------|------|
| **HPDMA** | §10 | p.162 | 高性能 DMA |
| **DMA (DW)** | §11 | p.177 | 标准 DMA |
| **Interrupt Sources** | §8.5 | p.115 | 中断源列表 |
| **IPC** | §4 | p.81 | 核间通信 |

---

## 常见问题 → 建议页码

| 问题 | 建议章节/页码 |
|------|--------------|
| NPU 如何加速 ML 推理？ | §3 (p.54), §3.6.2 (p.79) |
| Tensor Arena 放哪里？ | §3.1 (p.55), §6 (p.92) |
| 如何配置低功耗模式？ | §6.4.1 (p.95), §8.11 (p.135) |
| 双核如何通信？ | §4 IPC (p.81) |
| DMA 如何配置？ | §10 (p.162), §11 (p.177) |
| RRAM 写入流程？ | §7.1.4 (p.100) |
| 中断优先级配置？ | §8.7 (p.132) |
| HardFault 排查？ | §8.4.3 (p.113), §9 (p.137) |

---

## 检索关键词

### 英文
- NPUSS, Ethos-U55, NPU, Neural Processing Unit
- NNLite, Neural Network Accelerator
- APPCPUSS, Cortex-M55, Helium
- Tensor Arena, SRAM, Memory Map
- RRAM, NVM, Flash
- HPDMA, DMA, Descriptor
- IPC, Inter-Processor Communication
- Power Mode, Low Power, Sleep
- Exception, Fault, Interrupt

### 中文
- 神经处理单元, NPU
- 神经网络加速
- 张量区域, 内存映射
- 非易失性存储
- 直接内存访问
- 核间通信
- 低功耗模式
- 异常, 故障, 中断

---

*索引创建日期: 2026-03-08*
*注: 部分章节页码待补充完整 TOC 后更新*
