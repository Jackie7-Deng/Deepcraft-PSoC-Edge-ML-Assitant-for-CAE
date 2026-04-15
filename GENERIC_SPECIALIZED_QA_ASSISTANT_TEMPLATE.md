# 专属问答 AI 助手通用训练模板

> 目标：把一堆原始资料训练成一个有边界、会查证、会引用、可持续演进的专属问答助手。  
> 适用：Copilot、Claude Code、Trae等Agent，或任何 `Agent + 本地知识库 + 可选工具/MCP` 组合。

---

## 1. 先建立正确目标

你训练的不是会背文档的 AI，而是一个：

- 知道自己是谁
- 知道能回答什么、不能回答什么
- 知道先去哪里找证据
- 找不到证据时会承认不知道
- 新资料进入后能持续吸收

一句话：

> **要训练的是 evidence-first assistant，而不是 document-repeater。**

---

## 2. 推荐的总方法

任何专属助手，建议至少拆成 5 层：

### 2.1 初始化层

负责建立行为合同，而不是塞知识：

- 身份
- 领域边界
- 知识来源优先级
- 回答规则
- 引用规则
- 禁止编造规则
- 知识地图

### 2.2 路由层

把问题分流到正确的处理路径：

- 参数查询
- 故障诊断
- 代码定位
- 客户回复
- 外部搜索

### 2.3 结构化知识层

把 PDF、源码、FAQ、Q&A、工程经验整理成 AI 易用的 Markdown：

- overview
- faq
- troubleshooting
- parameters
- code_map
- community_digest

### 2.4 检索层

至少准备：

- 符号检索
- 关键词检索
- 文本分块检索
- 向量语义检索（可后做）
- 可选 MCP / 工具接口

推荐再明确区分两种 RAG：

- **轻量 RAG**：本地分块索引 + 关键词/同义词/领域词扩展 + 混合打分
- **重量 RAG**：向量库 + embedding + rerank + 增量索引治理

默认建议：

- 第一批专属助手先做**轻量 RAG**
- 等语料明显变大、问法明显变乱，再考虑重量 RAG

### 2.5 持续学习层

负责把新资料纳入系统：

- 导入新 PDF / 源码 / Q&A
- 抓 community / KBA / 工程经验
- 摘要与去重
- 更新 FAQ / digest / 索引

---

## 3. 一定要保留两级知识

不要只保留整理后的 Markdown，也不要只堆原始资料。

### 一级证据层

- 官方 PDF
- 原始源码
- 原始 readme
- 原始社区帖 / case 记录 / KBA

### 二级知识层

- FAQ
- 排障手册
- 参数目录
- 代码地图
- community digest

正确关系：

> **一级证据保证真实性，二级知识保证可回答性。**

---

## 4. 推荐最小目录结构

```text
project/
 .github/
    copilot-instructions.md
    instructions/
       external-search.instructions.md
 CLAUDE.md
 AGENTS.md
  prompts/
     main.md
  knowledge/
     overview.md
    source_inventory.md
    code_map.md
    faq.md
    troubleshooting_playbook.md
    parameters_catalog.md
     community_digest.md
 governance/
    TODO.md
    issues_log.md
    knowledge_governance.md
    mcp_regression_suite.md
    mcp_regression_suite.json
    mcp_observability.md
    rag_regression.md
  docs/
  indexes/
  ingest/
  scripts/
```

说明：

- `.github/copilot-instructions.md`：如果主要面向 VS Code Copilot，这是**首选工作区初始化入口**
- `.github/instructions/*.instructions.md`：按任务触发的专项规则，例如 external search / customer reply / code review
- `CLAUDE.md`：canonical init doc
- `AGENTS.md`：兼容其他支持 open standard / agent hierarchy 的客户端
- `prompts/main.md`：手动入口
- `knowledge/*.md`：面向回答的二级知识层
- `governance/`：治理、回归、问题登记、训练过程产物，建议集中放置，避免根目录越堆越乱
- `indexes/`：检索索引
- `ingest/`：新资料缓冲区
- `scripts/`：初始化、增量更新、验证脚本

补一句实战原则：

> **索引是导航层，不是证据层。最终引用仍应回到原始文件或原始 PDF 页。**

---

## 5. 哪些文件最关键

如果你的主要目标是 **Copilot / VS Code 工作区自动初始化**，不要只写 `CLAUDE.md`，还应同时写 `.github/copilot-instructions.md`。

经验上：

- Copilot 会在**新会话的首个用户请求**里自动带入 `.github/copilot-instructions.md`
- 但它**不会**在“用户还没输入任何内容”时主动开口

### 5.1 `CLAUDE.md`

.github/copilot-instructions.md同理

职责：

- 定义身份
- 定义边界
- 定义知识优先级
- 定义回答规则
- 给出知识地图

不要做的事：

- 不要塞整本 FAQ
- 不要复制大量源码细节
- 不要把所有知识都堆进去

### 5.2 `prompts/main.md`

职责：

- 给不支持自动初始化的 Agent 手动粘贴使用
- 保留统一输出结构
- 明确无证据时怎么说

### 5.3 `knowledge/overview.md`

职责：

- 建立系统全局坐标系
- 明确产品/协议/版本边界
- 告诉 AI 当前有哪些资料、哪些没覆盖

### 5.4 `knowledge/faq.md`

职责：

- 沉淀高频问题标准答案
- 统一口径
- 每条 FAQ 都要写适用前提和证据来源

### 5.5 `knowledge/troubleshooting_playbook.md`

职责：

- 做排障决策树
- 规定先问什么信息
- 规定不同症状先查哪些文件/模块

### 5.6 `knowledge/parameters_catalog.md`

职责：

- 记录关键宏、参数、默认值、端点、buffer、模式开关
- 非常适合回答这个值在哪里默认是多少之类的问题

### 5.7 `knowledge/code_map.md`

职责：

- 告诉 AI 每个源文件大致干什么
- 缩短代码导航时间

### 5.8 `knowledge/community_digest.md`

职责：

- 把高频 community/Q&A/历史 case 的经验沉淀下来
- 标出来源 URL 或 case 编号
- 标出适用条件

---

## 6. 外部搜索 / MCP 到底怎么设计

### 6.1 默认建议

默认先做：

- **本地知识库模式**
- 外部搜索先人工触发，不自动切换

原因：

- 本地知识稳定、可控、便于审计
- 外部经验往往是案例性质，不一定适用于所有版本/产品
- 自动切换很容易把证据不足和经验搜索混在一起

### 6.2 什么时候不需要 MCP Server

如果当前流程是：

- 工程师先看本地知识回答
- 觉得不够好时，自己手动去 community / case 搜

那么：

> **此阶段不一定需要专门的 MCP Server。**

### 6.3 什么时候需要 MCP Server

当你希望 Agent 自己直接访问外部系统时，再考虑搭 MCP Server。典型条件：

- 目标系统需要登录 / cookie / token
- 目标系统是私有 case 平台
- 你希望统一查询接口，而不是手工搜索
- 你希望把搜索、清洗、去重、摘要都交给 Agent 完成

一句话：

> **是否需要 MCP Server，不取决于有没有外部网站，而取决于Agent 是否要被授权直接、稳定、可控地访问它。**

### 6.4 实用建议

- 阶段 1：只做本地知识库
- 阶段 2：补轻量 RAG，再做人工触发的外部搜索策略
- 阶段 3：若确定要集成 private community/case，再做 MCP Server 或受控抓取层

这里的“轻量 RAG”建议指：

- 对 `knowledge/*.md`、源码、readme、关键 PDF 做分块
- 存本地 JSON 索引
- 用关键词 + 同义词 + 领域词扩展做混合召回
- 不急着上向量库

实战上还可以再做一个默认值：

- **默认先索引 Markdown / code / readme**
- **PDF 作为可选增强构建**

这样更符合“轻量”二字，也能避免第一次建索引就被大 PDF 拖慢。

### 6.5 一个更稳的现实做法

如果目标网站会 `403`、需要登录、或者普通抓取不稳定，优先考虑：

- **真实浏览器会话 + 自动化脚本**
- 再在其外层封装 MCP 工具

原因：

- 很多企业网站会基于 cookie、登录态、浏览器指纹、脚本执行环境做限制
- 直接 HTTP 抓取经常失败，但“复用人工已登录浏览器”往往可行
- 这样更接近工程师真实使用方式，也更容易逐步验证

推荐链路：

> **Agent -> MCP Tool -> Browser Automation -> 已登录的真实浏览器 -> community / case**

补一句最容易混淆的话：

- **MCP Client** = 你实际提问的入口（如 VS Code 里的 Copilot / Cursor）
- **MCP Server** = 被 Client 调用的工具后台
- 真正执行搜索的，往往是 MCP Server 后面的浏览器自动化脚本

### 6.6 外部搜索前，先做“关键词扩展”

不要把用户原句原封不动丢进 community/case 搜索框。

补一条非常实用的默认规则：

- **最终送进搜索框的 query，默认应是英文短关键词，词与词之间用空格，不要用 `+`，也不要直接送整句自然语言。**

建议先做一层：

- 芯片词：`FX3 / CX3 / CYUSB3014 / CYUSB306x`
- 协议词：`UVC / U3V / MIPI CSI-2 / Slave FIFO`
- 症状词：`no image / no stream / image shift / code 71 / re-enumeration / freeze`
- 变体词：同义词、简写、常见错误写法

目的：

- 企业 case 搜索引擎通常很弱
- 好的 query 规划，常常比 DOM 自动化本身更重要
- 关键词扩展是让外部搜索稳定可复用的关键层

再补两条实战经验：

- 用户在对话里常说的不是短 query，而是“去搜索此问题”。这时应先把**当前上下文中的真实问题**压缩成短关键词，再搜索。
- 短 query 不等于只搜一次，应该是：**短 query -> 看命中结果 -> 再调整关键词 -> 再搜下一轮**。
- 如果用户原句是中文、长句或问句，先压缩成英文 seed query，再扩展第二轮和第三轮。

推荐优先级：

1. 先提取：芯片词 + 协议词 + 主症状词
2. 再补：host / OS / hub / sensor / FPGA / format 等上下文词
3. 先搜最短一版
4. 命中不准时，再扩展第二轮和第三轮

### 6.6.1 外部搜索不要只做“一次查询”

更像真实工程师调试的流程应该是：

1. 先从当前问题压出 1 个最短 query
2. 看结果页里最相关的 2~3 条
3. 读正文
4. 归纳共性原因
5. 若还不够，再基于新线索改写下一轮 query

也就是说：

> **外部搜索更像链路式调试，而不是一次性全文检索。**

### 6.7 外部正文不要直接整段喂给模型

更稳的做法是先做一层摘要器，把外部经验整理成：

- 问题
- 现象
- 调试过程
- 解决建议
- 未决项

原因：

- case/community 原文通常很长、重复、聊天式
- 直接塞给模型，噪声大、token 高、容易抓错重点
- 先摘要，再交给问答 Agent，会明显更稳

对于 `case` 这类企业系统，再补一条：

- 搜索结果页常先停在 `Top results / Hub` 汇总视图，真正有用的信息往往在 `Cases` 这种专题 tab/grid 里，应该先切到目标结果表，再抽 `Subject / Description / Case number` 继续向下读。

### 6.8 外部检索要有“组合式防循环”

如果 Agent 能自己做 external search，就不要只靠一个 timeout。

更稳的做法是组合 4 类保护：

- **URL visit counter**：同一 URL / target 最多允许访问 `2~3` 次
- **link budget**：单轮 external search 最多打开 `10~20` 个结果链接
- **time budget**：给 search / read 分别设置总超时，例如 `30~60s` / `60~120s`
- **stale navigation limit**：连续 `3~5` 次导航没有产生新证据时停止

推荐原则：

- 不要让 Agent 因为“还能点下一个链接”就一直漫游
- stop 时必须返回：
  - 已拿到的最佳证据
  - 还缺什么
  - 为什么停止
  - 下一步建议

验收建议：

- 用缩小后的预算值做 deterministic smoke test
- 分别验证：
  - link budget stop
  - search timeout stop
  - read timeout stop
  - stale-navigation stop
  - same-target reread stop

### 6.9 强制 `search -> select -> read` 分离

外部搜索最容易失控的原因之一，是把“搜索”和“读正文”混在一个工具里。

更稳的默认结构是：

1. `search`
2. `select`
3. `read`
4. `summarize`

补一个很实用的实现经验：

- 返回结果时，`query` 最好表示**实际执行的 seed query**
- 如果还想保留用户原始输入，单独放进 `original_input` / `diagnostics`
- 否则上层 Agent 很容易误判“脚本是不是还在直接搜用户整句”

原因：

- 可控：搜索阶段只拿标题、摘要、URL
- 可审计：你知道到底读了哪几篇正文
- 可限流：容易对“打开正文”动作单独计数
- 可调试：DOM 漂移时能区分“结果页坏了”还是“详情页坏了”

经验上，Community / KBA / Case 都适用这一原则。

### 6.10 企业站点优先复用已登录浏览器

面对 SSO、企业 case 系统、反爬、动态脚本页面时，最稳的现实策略通常不是“写更复杂的 HTTP 爬虫”，而是：

- 启动或复用一个**已登录的真实浏览器**
- 通过 CDP / Playwright / browser automation 复用该会话

推荐实践：

- 固定一个远程调试端口，例如 `http://127.0.0.1:9222`
- **优先复用**已登录会话
- 只有会话不可用时，再自动拉起浏览器
- 尽量使用固定 profile，避免每次重新登录

一句话：

> **浏览器会话复用往往比“更聪明的抓取器”更重要。**

### 6.11 把“慢查询 / 代表场景”做成固定回归集

DOM 漂移、搜索变慢、提取稀疏，这些问题如果只靠临时记忆，很快会复发。

建议至少维护一份手工可跑的回归集，包含：

- 代表性成功 query
- 已知慢 query
- 必须触发 stop-rule 的缩放预算场景
- 至少一个 case path 场景（如果系统可登录）

每条都写清：

- 目的
- query / target
- 预期
- 哪些失败是已知可接受的

原则：

- 不一定马上做 CI
- 先有 checklist，比“靠人回忆”强很多

### 6.12 轻量 RAG 的最小可用交付，不只是“有个索引”

很多项目说自己“做了 RAG”，其实只是把一堆文本塞进索引文件，没有形成可审计的交付。

更稳的最小交付建议至少包含：

- 一份 `chunk_schema.md`
- 一份真实落盘的本地索引文件
- 一份固定查询回归集，例如 `rag_regression.md`
- 明确写出：**index != evidence**

`chunk schema` 至少要回答：

- `source_path`
- `source_type`
- `title / heading`
- `page_range` 或等价定位信息
- `anchor`
- `text`
- `hash`
- `mtime`

这样做的价值是：

- 之后换脚本实现时，索引消费者不必跟着重写
- 你能判断“命中的是哪一段、来自哪一页、是不是旧块”
- 回归用例能直接验证“是否命中了正确来源”，而不是只看“好像搜到了什么”

一句话：

> **轻量 RAG 的最小可交付物应该是：schema + index + regression，而不是一段“我们有检索能力”的描述。**

### 6.13 轻量多代理，先落成“单进程管线 + 仲裁器”

不要一上来就做复杂多 agent 并发系统。

很多问答项目先做下面这条固定链路，就已经能拿到大部分收益：

1. `Extract`
2. `Retrieve`
3. `Critic`
4. `Synthesize`

其中最关键的新增件通常不是“再多一个 agent”，而是：

- 一个明确的评分 spec
- 一个可执行的 `evidence_arbitrator`

仲裁器的最小职责：

- 对候选证据打分
- 标出冲突
- 指出还缺哪一个最小鉴别信息

这样做的好处是：

- 比纯人工“感觉哪个更靠谱”更稳定
- 比真多 agent 系统更便宜、更容易验证
- 以后即使升级到并行 agent，也仍能复用这个仲裁层

一句话：

> **轻量多代理的第一步，通常不是 orchestration framework，而是固定管线 + 仲裁器。**

### 6.14 外部检索稳定性 = 回归集 + 可观测 + stop rules

external search 稳不稳定，往往不取决于“脚本能不能打开页面”，而取决于：

- 有没有固定回归集
- 有没有可落盘的可观测字段
- 有没有明确定义 stop rules

推荐最小组合：

- `governance/mcp_regression_suite.md` 或 `governance/mcp_regression_suite.json`
- `run_mcp_regression.py`
- `governance/mcp_observability.md`
- 每次 session 的 JSONL 事件日志

至少要能落盘这些结果：

- 每条回归用例的 `status`
- `elapsed`
- `stop reason`
- `result_count`
- 关联的日志文件路径

这样，当“这周能搜到、下周搜不到”时，你才有审计线索，而不是只剩下口头印象。

### 6.15 证据缺口时，不要只写“缺资料”

当官方资料缺一块时，更稳的做法通常不是卡住，而是把缺口先转成：

- 可执行自检命令
- 需要用户提供的最小命令输出
- 明确的 `【Inference】` 边界

典型例子：

- `Get-Command openocd`
- `where openocd`
- `fw-loader --help`
- `openocd --version`

这些命令输出本身，就是新的一级证据输入。

推荐做法：

1. 先保存一份 host self-check 原始记录
2. 再把它沉淀到 FAQ / 参数表 / 排障树
3. 仍然保留“这是当前主机事实，不是普遍规格”的边界说明

一句话：

> **缺文档时，优先把问题改写成“请给我这几个命令输出”，而不是把缺口继续留成抽象空白。**

---

---

## 7. 经典 community 问题要不要提前本地化

建议：**要。而且是训练/组织完本地文档成为知识库之后。**

原因：

- 高频问题反复搜索很浪费时间
- 本地知识库已经足够Agent抽取相关问题或关键词进行community/MSD等外部知识补充
- 很多工程经验其实是准 FAQ
- 提前整理成 `community_digest.md`，能显著降低后续检索成本

推荐做法：

- 先整理前 10~20 个最常见问题
- 每条写清：问题、结论、适用前提、来源、风险
- 不要把 forum 单帖写成官方规格

### 7.1 digest 与 FAQ / playbook 的边界

容易出问题的地方不是“有没有 digest”，而是 digest 和 FAQ/playbook 写成了两份重复答案。

推荐边界：

- `digest`：保留来源、案例差异、边界、经验摘要
- `faq`：保留可直接回答用户的标准答案
- `troubleshooting_playbook`：保留决策树和排查顺序

正确流向通常是：

> **新 external evidence -> digest -> 去重 -> 回灌 FAQ / playbook / params**

而不是：

> 每次发现新帖子，就再写一份新的完整答案。并且每次主动沉淀知识入库时，需要主动询问用户，或者用户主动说明“沉淀该知识入库”。

### 7.2 需要一份知识治理文档

当知识库开始包含：

- 官方 PDF
- 官方 README / 脚本
- Community
- Case
- `【Inference】`

就应该有一份单独的 `knowledge_governance.md`，至少定义：

- 条目模板
- 证据等级
- 冲突处理
- 去重策略
- 回灌规则

没有这份文档时，助手很容易在多轮训练后出现：

- 同一问题多份答案
- 弱证据覆盖强证据
- 外部经验无法正确回灌

### 7.3 先记录后修复，比边测边修更稳

验收或 smoke test 轮次里，不要默认“发现问题就立刻修”。

更稳的流程是：

1. 把问题先写进 `issues_log`
2. 把未立即修复的问题挂到一个统一 backlog 项
3. 只有当问题阻断验收 / 回归 / 关键闭环时才立即修

原因：

- 避免 Agent 在一个细节上无限深挖
- 保留完整审计线索
- 让“当前轮的目标”不被局部 bug 带偏

这是对带 external search、浏览器自动化、RAG、知识回灌项目尤其重要的一条工程纪律。

---

## 8. 推荐回答格式

```md
【Conclusion】
直接回答用户问题。

【Evidence】
- path:line
- document#page
- 【Inference】如果是推断，必须显式标注

【Explanation / Steps】
补充分析、排查路径或操作步骤。

【Risk / Boundary】
说明适用范围、版本差异、容易混淆点。

【Missing Information】
如果信息不足，明确还需要什么。
```

---

## 9. 一套通用防幻觉规则

训练任何专属助手都建议写进去：

1. 原始资料优先于二级整理
2. 关键结论必须可追溯
3. 推断必须显式标注
4. 超范围必须承认不知道
5. 先判断版本 / 模式 / 产品边界
6. 相似产品不能混答
7. 没有证据时不输出精确参数
8. 经验只能补充，不能覆盖规格

---

## 10. 推荐最小可用版本（MVP）

### 阶段 1：先做到能用

至少准备：

- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `prompts/main.md`
- `knowledge/overview.md`
- `knowledge/source_inventory.md`
- `knowledge/code_map.md`
- `knowledge/faq.md`
- `knowledge/troubleshooting_playbook.md`
- `knowledge/parameters_catalog.md`

### 阶段 2：再做到更稳

增加：

- `indexes/`
- `init/update/verify` 脚本
- 轻量 RAG：本地 chunk index + search 脚本（可选，知识库太小时不需要）
- 更细的专题知识文档
- 浏览器驱动的 community / case 搜索原型
- 搜索关键词扩展层
- 外部结果摘要层

### 阶段 3：再做到更强

增加：

- `community_digest.md`
- 向量检索
- 手动触发的外部搜索模式
- 私有系统接入能力
- 增量吸收与去重策略
- 高频问题经验回灌机制

说明：

- 如果阶段 2 的在线搜索已经足够稳定，阶段 3 **不一定等于继续喂大量离线资料**。
- 更合理的阶段 3 可以只是“轻量治理层”，例如：高价值经验确认后再沉淀、query 模式优化、少量 FAQ 回灌。
- 也就是说：**轻量 RAG 常常属于阶段 2；重量 RAG 才更接近阶段 3。**

---

## 11. 一个可以直接复用的初始化骨架

```md
# [领域名] 专属助手

## 角色
你是 [领域名] 专属问答助手。

## 知识优先级
1. 本地原始资料
2. 本地知识文档
3. 【Inference】工程推断

## 回答规则
- 关键结论必须引用
- 推断必须标注【Inference】
- 没证据时必须说未找到依据
- 不自动切换到外部搜索
- 外部搜索默认由工程师手动触发
- 若外部站点抓取受限，优先复用已登录浏览器，而不是盲目写爬虫

## 知识地图
- knowledge/overview.md
- knowledge/faq.md
- knowledge/troubleshooting_playbook.md
- knowledge/parameters_catalog.md
- knowledge/code_map.md

## 边界
- 支持：[问题类型]
- 谨慎：[需要更多证据的问题]
- 不支持：[超范围内容]
```

---

## 12. 最后一句话

你真正要训练出来的，不是一个看过很多资料的 AI，而是一个：

> **有边界、会查证、会引用、能积累经验、可长期维护的专属助手。**

---

## 13. 训练下一个专属助手时，哪些文件应该直接复用

如果你已经为一个专属助手打通了 `Community / Case / 轻量 RAG` 这套底座，那么训练下一个助手时，**不要从零重写**。

优先直接带过去：

### 13.1 方法类文档

- `GENERIC_SPECIALIZED_QA_ASSISTANT_TEMPLATE.md`
- `CLAUDE.md`（作为上一个项目的参考，不是原样照抄）
- `prompts/main.md`（作为手动初始化骨架）
- `knowledge/retrieval_strategy.md`

### 13.2 MCP / 外部搜索底座

- `mcp_servers/infineon_browser_server.py`
- `scripts/community_search_playwright.py`
- `scripts/community_read_playwright.py`
- `scripts/case_search_playwright.py`
- `scripts/case_read_playwright.py`
- `scripts/case_summary.py`
- `scripts/search_utils.py`
- `scripts/launch_infineon_mcp_browser.py`
- `.vscode/mcp.json`

### 13.3 轻量 RAG 底座

- `scripts/lightweight_rag.py`
- `scripts/build_lightweight_index.py`
- `scripts/search_lightweight_index.py`
- `indexes/chunk_schema.md`
- `governance/rag_regression.md`

### 13.3.1 证据仲裁底座

- `knowledge/evidence_scoring.md`
- `scripts/evidence_arbitrator.py`

### 13.3.2 外部检索稳定性底座

- `governance/mcp_observability.md`
- `governance/mcp_regression_suite.md`
- `governance/mcp_regression_suite.json`
- `run_mcp_regression.py`

### 13.4 可以选择性带过去的操作文档

- `knowledge/vscode_mcp_usage_guide_zh.md`

原则：

- **带“方法”和“工具底座”**
- **重做“领域知识内容”**

也就是说：

- Community/Case 的访问方式通常可复用
- 轻量 RAG 的脚本通常可复用
- 真正要重新训练的，是新芯片/新协议/新代码库对应的知识地图、FAQ、参数、排障链路

训练新助手时，要特别提醒新 Agent：

1. 先读模板，再读当前项目资料
2. 先做边界判断，不要继承旧项目的芯片/协议假设
3. 先复用 MCP / RAG 脚本，再决定哪些关键词词表需要改写
4. 索引和摘要可复用，**证据内容不能照搬**

---
