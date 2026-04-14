# PSoC Edge Memory / Linker / XIP 指南

**更新日期**: 2026-04-14  
**定位**: 回答 PSoC Edge 的 memory placement、默认 BSP 布局、linker/VMA-LMA、XIP/MMIO、功耗与性能权衡时的低 token 入口。

---

## 1. 这份指南解决什么问题

新增的两份本地资料把此前 memory placement 主要依赖 community 回指 whitepaper 的缺口补上了：

- `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf`
- `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf`

前者更像正式应用笔记，覆盖内部/外部 memory、默认 BSP 布局、linker、VMA/LMA、功耗与性能；后者更像客户培训材料，适合快速确认 memory map、TCM、SMIF 和代码/数据 placement 练习入口。  
`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#1` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#3`

## 2. 先记住的默认硬件事实

### 2.1 内部 memory 组成

- RRAM：up to 512 KB，适合掉电保留代码/数据，但读访问有 wait states。  
  `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#5` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#7`
- SRAM 0 / SRAM 1：总计 1 MB，位于低功耗域，运行时数据与高频访问代码优先考虑这里。  
  `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#5` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#10`
- System SRAM (SoCMEM)：5120 KB，位于高性能域，适合高带宽 runtime data / buffer。  
  `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#5` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#11` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#12`
- CM55 TCM：ITCM 256 KB、DTCM 256 KB，适合低延迟、确定性强的关键代码和数据。  
  `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#7` `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#14`

### 2.2 Power domain 视角

- PD0：always-on low-power domain。
- PD1：high-performance domain，可独立关断以省电。  
  `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#5`

这意味着：若用户问“某段内容在低功耗模式下还能不能保留”，先区分它在 PD0 还是 PD1，而不是只看它叫 SRAM 还是 SoCMEM。

## 3. 外部 memory、SMIF、XIP / MMIO

- PSoC Edge 最多有两个 SMIF：SMIF0 / SMIF1，具体是否可用与封装有关。  
- 每个接口最多可见 1 GB 地址空间，但 XIP window 是 64 MB。  
- 支持 XIP 与 MMIO，也支持 SDR / DDR、Quad / Octal / HyperBus 类外部 memory。  
  `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#15`

培训材料还给了一个很直接的例子：

- SMIF0：MMIO access to external QSPI flash
- SMIF1：XIP access to external OSPI PSRAM  
  `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#16`

## 4. 最容易踩坑的点：RWW 与 XIP

应用笔记明确提醒：某些外部 memory IC 不支持 Read While Write (RWW)。如果同一颗通过 SMIF 连接的外部 memory 正在执行写/擦，而系统又试图从它做 XIP 读访问，可能直接 fault。  
`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#8`

文档给出的缓解方向：

1. 把关键代码搬到内部 SRAM 或 SoCMEM。
2. 避免关键流程依赖同一颗正在写/擦的 XIP memory。
3. 双核场景做 CM33 / CM55 同步。
4. 固件升级流程不要让升级代码仍依赖同一颗 SMIF memory。

## 5. 默认 memory map 与 BSP 布局

### 5.1 默认地址视图

CTW 给出了默认地址映射：

- RRAM (NVM)：`0x0200_0000`
- SRAM：`0x2400_0000`
- SoCMEM：`0x2600_0000`
- CM55 ITCM：`0x0000_0000`
- CM55 DTCM：`0x2000_0000`
- SMIF0：`0x6000_0000`
- SMIF1：`0x6400_0000`  
  `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#17`

### 5.2 默认 EVK 使用习惯

CTW 还明确写到：

- EVK 默认启用了 SMIF0 上的 Quad SPI Flash
- Octal RAM 默认未启用
- DTCM 默认用于 CM55 stack
- ITCM 默认放 CM55 vector table、部分 driver 和 library source files  
  `docs/application_notes/infineon-psoc-edge-memory-usage-ctw-en.pdf#18`

### 5.3 外部 flash 镜像布局

AN239774 进一步给出默认 BSP / external flash 布局，包含如 `CM55 image`、`CM55 trailer` 等区域；trailer 用于 Edge Protect Bootloader 的安全升级管理。  
`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#23`

## 6. 回答 linker 问题时必须知道的三个点

### 6.1 VMA / LMA

当文档写成：

```ld
.section_name : { ... } > VMA_mem_reg AT > LMA_mem_reg
```

含义是：

- `> VMA_mem_reg`：运行地址
- `AT > LMA_mem_reg`：镜像装载地址  
  `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#24`

这正是“代码存放在 flash，但运行时搬到 SRAM/ITCM”的关键概念。

### 6.2 Memory region 不只在主 linker 里

PSoC Edge 的 memory region 还会通过 Device Configurator 生成：

`bsps/TARGET_<BSP>/config/GeneratedSource/cymem_<Toolchain>_<Core>.<Linker-Extension>`  
`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#25`

因此用户说“我改了 linker 但不生效”，第一反应应是：

1. `Memory` tab 改了没有？
2. `cymem_*` 生成文件更新了没有？
3. 主 linker include 到它了没有？  
   `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#38`

### 6.3 Toolchain 路径不同

AN239774 还区分了 GNU / Arm / IAR / LLVM_ARM 的 linker 文件位置和风格，不要把 GNU 的 `.ld` 经验直接套到其他 toolchain。  
`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#26` `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#27`

## 7. 性能与功耗取舍

应用笔记对优化建议很直接：

1. CM55 上优先用 ITCM / DTCM 处理低延迟、确定性强的访问。
2. 小而重复的操作可利用 cache。
3. ML inference 场景优先利用 U55 协处理器。
4. 外部 memory 接口优先更高带宽协议：Quad 优于 Dual，Octal 优于 Quad，DDR 优于 SDR。
5. 再配合合适的 compiler optimization flags。  
   `docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#34`

同时，若应用规模较大（图像处理、图形等），仅靠内部 memory 可能不够，需要结合外部 SMIF memory，但这会把性能、功耗和安全权衡带进来。  
`docs/application_notes/infineon-an239774-selecting-and-configuring-memories-power-performance-psoc-edge-applicationnotes-en.pdf#31`

## 8. 典型回答路由

| 用户问题 | 优先引用 |
|----------|----------|
| “默认 memory map 是什么？” | `...memory-usage-ctw-en.pdf#17-18` |
| “XIP / MMIO 有什么区别？” | `...memory-usage-ctw-en.pdf#15-16` |
| “为什么写 flash 时系统 fault？” | `...an239774...pdf#8` |
| “linker 改了没生效怎么办？” | `...an239774...pdf#24-25` `...#38` |
| “性能关键代码该放哪？” | `...an239774...pdf#34` |

## 9. 当前边界

- 这两份文档已经足以回答大多数 memory placement / linker / XIP 基础问题。
- 若用户追问**具体某个 BSP 生成出来的 region 名称、地址、长度**，仍要回到目标工程里的实际 linker 文件和 `GeneratedSource/cymem_*`。
- 若用户追问**某个 memory 器件的具体型号参数**，仍要回 kit guide / datasheet，不应只凭 CTW 摘要回答。
