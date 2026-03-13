# PSoC Edge E8x 寄存器参考手册索引

**文档**: PSoC™ Edge E8x2, E8x3, E8x5, E8x6 Registers Reference Manual
**版本**: 002-38332 Rev. *A
**日期**: 2025-11-18
**路径**: `docs/trm_aum/psoc_edge_e8x_registers_rm.pdf`
**大小**: 60.4 MB

---

## 文档结构概述

寄存器参考手册包含 PSoC Edge E8x 全部外设与子系统的详细寄存器定义。由于文档体量较大（60.4 MB），本索引用于提供快速导航。

### 按子系统分类

---

## 1. CPU 子系统寄存器（CPUSS）

| 模块 | 寄存器组 | 基地址 | 说明 |
|------|----------|--------|------|
| SYSCPUSS | SYSCPUSS_* | - | 系统 CPU 子系统 |
| APPCPUSS | APPCPUSS_* | - | 应用 CPU 子系统 |
| NPUSS | NPUSS_* | - | 神经处理单元子系统 |
| Secure Enclave | SEC_* | - | 安全相关寄存器 |

---

## 2. ML / NPU 寄存器 ⭐

### Ethos-U55 NPU
| 寄存器 | 偏移 | 说明 |
|--------|------|------|
| NPU_* | - | Ethos-U55 控制与状态 |
| NPU_CMD_* | - | 命令队列寄存器 |
| NPU_IRQ_* | - | 中断配置 |

### NNLite 加速器
| 寄存器 | 偏移 | 说明 |
|--------|------|------|
| NNLITE_* | - | Neural Network Lite 控制 |
| NNLITE_CFG_* | - | 配置寄存器 |

---

## 3. 存储控制器寄存器

### SRAM 控制器
| 寄存器组 | 说明 |
|----------|------|
| SRAMC_* | SRAM 控制器配置 |
| SRAM_* | SRAM Bank 控制 |

### RRAM / NVM 控制器
| 寄存器组 | 说明 |
|----------|------|
| RRAMC_* | RRAM 控制器 |
| FLASHC_* | Flash 控制器 |
| NVM_* | 非易失性存储控制 |

---

## 4. 系统资源寄存器（SRSS）

### 时钟系统
| 寄存器组 | 说明 |
|----------|------|
| CLK_* | 时钟控制 |
| PLL_* | PLL 配置 |
| FLL_* | FLL 配置 |
| CLKPATH_* | 时钟路径选择 |

### 电源管理
| 寄存器组 | 说明 |
|----------|------|
| PWR_* | 电源控制 |
| PWRMODE_* | 电源模式配置 |
| LPMODE_* | 低功耗模式 |

### 复位系统
| 寄存器组 | 说明 |
|----------|------|
| RES_* | 复位控制 |
| RES_CAUSE_* | 复位原因状态 |

---

## 5. DMA 寄存器

### HPDMA（高性能 DMA）
| 寄存器组 | 说明 |
|----------|------|
| HPDMA_CH_* | 通道配置 |
| HPDMA_DESCR_* | 描述符寄存器 |
| HPDMA_IRQ_* | 中断控制 |

### DW_DMA（Datawire DMA）
| 寄存器组 | 说明 |
|----------|------|
| DW_CH_* | 通道寄存器 |
| DW_DESCR_* | 描述符配置 |

---

## 6. 通信外设

### UART
| 寄存器组 | 说明 |
|----------|------|
| UART_* | UART 控制 / 状态 |
| SCB_* | 串行通信模块 |

### SPI / I2C
| 寄存器组 | 说明 |
|----------|------|
| SPI_* | SPI 寄存器 |
| I2C_* | I2C 寄存器 |
| SCB_* | 共享 SCB 寄存器 |

---

## 7. Analog Peripherals

### ADC
| 寄存器组 | 说明 |
|----------|------|
| SAR_* | SAR ADC registers |
| PASS_* | Programmable Analog Subsystem |

### DAC
| 寄存器组 | 说明 |
|----------|------|
| DAC_* | DAC control registers |
| CTDAC_* | Continuous Time DAC |

---

## 8. Timer/Counter Registers

| 寄存器组 | 说明 |
|----------|------|
| TCPWM_* | Timer Counter PWM |
| TIMER_* | General purpose timers |
| COUNTER_* | Counter registers |

---

## 9. GPIO Registers

| 寄存器组 | 说明 |
|----------|------|
| GPIO_* | GPIO port registers |
| GPIO_PRT* | Port-specific registers |
| HSIOM_* | I/O matrix |
| SIO_* | Special I/O |

---

## 10. Security Registers

| 寄存器组 | 说明 |
|----------|------|
| CRYPTO_* | Cryptographic accelerator |
| HASH_* | Hash engine |
| PKI_* | Public Key Infrastructure |
| SEC_* | Security configuration |

---

## 常用寄存器快速查找

### ML 推理相关 ⭐

| 功能 | 寄存器 | 位置参考 |
|------|--------|----------|
| NPU 使能 | NPUSS_CTRL | NPUSS section |
| NPU 中断状态 | NPUSS_INTR | NPUSS section |
| NNLite 配置 | NNLITE_CFG | NNLite section |
| Tensor Arena | SRAM configuration | SRAMC section |

### 内存相关

| 功能 | 寄存器 | 位置参考 |
|------|--------|----------|
| SRAM 等待状态 | SRAMC_WAIT | SRAMC section |
| RRAM 写保护 | RRAMC_PROT | RRAMC section |
| Flash 状态 | FLASHC_SR | FLASHC section |

### 时钟/电源相关

| 功能 | 寄存器 | 位置参考 |
|------|--------|----------|
| 系统时钟 | CLK_SYSTEM | SRSS CLK section |
| 低功耗模式 | PWRMODE_KEY | SRSS PWR section |
| 唤醒源 | WAKEUP_EN | SRSS section |

---

## 检索关键词

### 英文
- NPUSS, Ethos-U55, NPU registers
- NNLite, Neural Network Accelerator
- SRAMC, RRAMC, FLASHC
- HPDMA, DW_DMA, Channel, Descriptor
- GPIO, HSIOM, Port
- CLK, PLL, FLL, Clock
- PWR, Power Mode, Low Power
- UART, SCB, SPI, I2C
- SAR, ADC, DAC, PASS
- TCPWM, Timer, Counter
- CRYPTO, HASH, Security

### 中文
- 神经处理单元寄存器
- 神经网络加速器
- 内存控制器
- 直接内存访问
- 通用输入输出
- 时钟电源管理
- 通信外设
- 模拟外设
- 定时器
- 安全加密

---

## 与 Architecture RM 的关系

Architecture RM (11.6 MB) 提供功能描述和架构说明
Registers RM (60.4 MB) 提供详细的寄存器位域定义

**交叉参考**:
| Architecture RM 章节 | 对应 Registers RM 寄存器组 |
|---------------------|--------------------------|
| §3.6.2 U55 NPUSS | NPUSS_* |
| §3.6.7 NNLite | NNLITE_* |
| §5 SRAM Controller | SRAMC_* |
| §7 RRAM/NVM | RRAMC_*, FLASHC_* |
| §10 HPDMA | HPDMA_* |
| §8 Interrupts | INTR_* |

---

## 注意事项

1. **寄存器访问权限**: 某些寄存器需要特定特权级别
2. **保留位**: 写入保留位应为 0
3. **同步访问**: 某些寄存器需要同步访问序列
4. **保护机制**: 部分寄存器有写保护机制

---

*索引创建日期: 2026-03-08*
*注: 此索引为结构概览。具体寄存器地址和位域定义请查阅完整 PDF 文档。*
*建议使用 PDF 阅读器的搜索功能定位具体寄存器名称。*
