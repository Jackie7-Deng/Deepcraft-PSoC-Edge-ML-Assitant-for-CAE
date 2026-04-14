# ModusToolbox / BSP / ML 版本兼容入口

**更新日期**: 2026-04-14  
**定位**: 回答“该用哪个 ModusToolbox 版本、3.6/3.7 有什么变化、版本问题该先看哪里”时的低 token 入口。

---

## 1. 先记住：版本口径不是单一数字

当前工作区至少同时存在三类版本口径：

| 场景 | 当前可确认口径 | 证据 |
| --- | --- | --- |
| PSoC 6 Imagimob MTBML Deploy | ModusToolbox 3.1+，ML Pack 2.0+ | `docs/readmes/README_mtb-example-ml-imagimob-mtbml-deploy.md` |
| Face ID Demo | ModusToolbox 3.6+，BSP 1.1.0+ | `docs/readmes/README_Machine_Learning_Face_ID_Demo.md` |
| DEEPCRAFT Data Collection / Deploy Motion / Deploy Vision | ModusToolbox 3.6+，BSP 1.0.0+ | `docs/readmes/README_DEEPCRAFT_Data_Collection.md` `docs/readmes/README_DEEPCRAFT_Deploy_Motion.md` `docs/readmes/README_DEEPCRAFT_Deploy_Vision.md` |
| KIT_PSE84_EVAL 套件软件准备 | ModusToolbox 3.8+ 与 KitProg3 drivers | `docs/kit_guides/kit_pse84_eval_user_guide.pdf`、`knowledge/index_kit_guide.md` |

**结论**：先按“具体工程 README”回答，再用 release notes 补工具包行为变化，不能把某个示例的版本要求外推成整个 PSoC Edge / PSoC 6 体系的唯一答案。

---

## 2. ModusToolbox 3.6 对当前仓库最相关的点

### 2.1 它是 tools package 的完整版本，且与旧版本并行安装

- 3.6.0 是完整 release，包含之前 patch，并且**不会替换已有安装版本**，而是并行安装。  
  `docs/release_notes/mt3.6_release_notes.pdf#1`

### 2.2 对 PSoC Edge 直接相关的工具变化

- Project Creator 会把**已连接的 KitProg3 板卡**自动放到 kit 列表前面。  
- Device Configurator 在 3.6 中增加了 **PSoC Edge family** 相关的 memory / peripheral security 配置增强。  
- LLVM 继续受支持；若走 LLVM，需要把 `TOOLCHAIN=LLVM_ARM`，并设置 `CY_COMPILER_LLVM_ARM_DIR`。  
  `docs/release_notes/mt3.6_release_notes.pdf#3` `docs/release_notes/mt3.6_release_notes.pdf#4`

### 2.3 3.6 自带工具版本入口

- Dashboard 3.6.0
- Device Configurator 5.50.0
- GNU make build system 2.6.0
- Project Creator 2.50.0
- QSPI Configurator 4.60.0  
  `docs/release_notes/mt3.6_release_notes.pdf#5`

### 2.4 工具链支持口径

- Setup program 可装 GCC 11.3 与 GCC 14
- 也支持 Arm Compiler 6+、IAR EW 9+、LLVM 18.1.3+  
  `docs/release_notes/mt3.6_release_notes.pdf#6`

### 2.5 当前更实用的已知问题

- 多核应用在命令行直接 `make program -j` 可能出现编程流程不同步；当前 workaround 是先 `make build -j`，再 `make qprogram`。  
- 如果通过 BSP Assistant 改了 MCU / SOC / SIP，调试配置里的 svd 路径可能缺失，官方建议到应用目录执行 `make getlibs`，再重新 `make eclipse` 或 `make vscode`。  
  `docs/release_notes/mt3.6_release_notes.pdf#15`

---

## 3. ModusToolbox 3.7 对当前仓库最相关的点

### 3.1 新增 memory report tool

- 3.7 新增 **memory report tool**，会在成功 build 后输出完整内存使用报告，且会生成 **text + json** 文件。  
  这对当前仓库的 memory placement / linker / XIP / arena 排障很有直接价值。  
  `docs/release_notes/mt3.7_release_notes.pdf#3` `docs/release_notes/mt3.7_release_notes.pdf#4`

### 3.2 Device Configurator 与工具包变化

- Device Configurator 新增 Notes 字段编辑 / 保存，以及在参数描述里做搜索。  
- CAPSENSE Configurator and Tuner 已从 tools package 移出，改为单独 pack。  
  `docs/release_notes/mt3.7_release_notes.pdf#3`

### 3.3 3.7 自带工具版本入口

- Dashboard 3.7.0
- Device Configurator 5.60.0
- memoryreport 1.0.0
- GNU make build system 2.6.1
- Project Creator 2.60.0
- QSPI Configurator 4.70.0  
  `docs/release_notes/mt3.7_release_notes.pdf#4`

### 3.4 工具链支持口径

- GCC 11.3 / GCC 14
- Arm Compiler 6+
- IAR EW 9+
- LLVM 18.1.3+  
  `docs/release_notes/mt3.7_release_notes.pdf#5`

### 3.5 当前更实用的已知问题

- 在 3.x 中，代理 / 防火墙没配好时，不只是 Project Creator / Library Manager，**所有工具**都可能报 URL 访问失败。  
- `.mtb` 直接依赖若写 `latest-x.y`，可能在 `make getlibs` 时被间接依赖覆盖；官方建议用固定的 `release-x.y.z` tag。  
- BSP Assistant 命令行建 BSP 时不一定会把 `BSP_COMPONENTS` 写回 Makefile；当前 workaround 是优先用 GUI 建 BSP。  
- 若 BSP Assistant 建 BSP 时提示配置错误，官方建议立刻进入 Device Configurator 清 Notice List。  
  `docs/release_notes/mt3.7_release_notes.pdf#6` `docs/release_notes/mt3.7_release_notes.pdf#15`

---

## 4. 当前仓库里回答版本问题的推荐顺序

1. **先看具体工程 README**
2. **再看 kit guide 的安装口径**
3. **最后用 3.6 / 3.7 release notes 判断工具行为变化或已知问题**

如果问题已经落到“本机到底装了哪些 tools / packs / manifests / compiler”，再引导去：

- `C:\Users\DengJi\ModusToolbox\`

注意：这是**工作区外的补充证据路径**，不是默认知识源。

---

## 5. 当前回答时最容易踩的坑

- 不要把 `Face ID Demo 3.6+` 说成所有 PSoC Edge 工程都只能用 3.6
- 不要把 `KIT_PSE84_EVAL 3.8+` 的安装口径说成所有示例的最低版本要求
- 不要把 tools package release notes 里的“支持某工具链”误说成“所有应用默认支持该工具链”
- 不要忽略 `make getlibs`、`BSP_COMPONENTS`、代理设置这类工具层问题
