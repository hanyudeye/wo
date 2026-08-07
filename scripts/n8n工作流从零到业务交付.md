---
---
# n8n 工作流从零到业务交付

## 一、不懂业务？先背熟这 8 个通用业务模板（覆盖 80% 中小企业需求）

| 业务模板 | 触发器 | 核心处理 | 典型输出 | n8n 关键节点 |
|---------|--------|----------|----------|-------------|
| **线索处理** | 表单/邮件/广告回传 | 清洗→去重→打分→分派→首联 | CRM 新建记录 + 钉钉通知销售 | HTTP Request, IF, Set, CRM API |
| **客服分流** | 企微/钉钉/网页聊天 | 意图识别→知识库检索→生成回复→人工兜底 | 自动回复/工单创建 | Webhook, AI Agent, Vector DB, Send Message |
| **内容生产** | 选题库/关键词/竞品 | 大纲→正文→配图→审核→多平台发布 | 成品推文/视频脚本/SEO 文章 | AI Agent, HTTP Request, Social APIs |
| **数据同步** | 定时/数据变更 | 抽取→转换(ETL)→加载→校验 | 多系统数据一致 | Schedule, Postgres/MySQL, Spreadsheet, Merge |
| **监控预警** | 定时/日志/页面变化 | 阈值判断/内容 Diff→分级告警 | 飞书/短信/邮件告警 | Cron, HTTP Request, IF, Slack/Lark |
| **会议/音频落地** | 录音上传/会议结束 | ASR→结构化摘要→待办提取→归档 | 纪要文档 + 任务系统 | HTTP Request(funASR), AI Agent, Notion/GitHub |
| **报表自动化** | 定时/手动触发 | 多数据源聚合→计算指标→渲染图表→分发 | PDF/Excel/看板链接 | Schedule, Databases, Code(Python), Send Mail |
| **电商/订单闭环** | 下单/发货/退款/评价 | 状态流转→库存扣减→发票/物流→售后触发 | ERP/店铺后台同步 | Webhook, ERP API, IF, Function |

先死记这张表。看到任何业务场景，先往这 8 个桶里套。

---

## 二、n8n 硬技能速成路线（2 周）

### Week 1：跑通节点语法 + 表达式 + 错误处理

| 天 | 任务 | 产出 |
|---|------|------|
| 1 | 官方 Quickstart + Core Concepts 文档读完 | 能解释：Workflow, Node, Connection, Expression `{{ $json.field }}` |
| 2 | 手搓 3 个微工作流：定时取天气发飞书、Webhook 接 JSON 存 SQLite、表单 IF 判断两条路径 | 3 个可运行 .json |
| 3 | 精通 Set / IF / Switch / Merge / Code 这 5 个逻辑节点 | 能不查文档写数据清洗、分支、合并 |
| 4 | 表达式进阶：`$json`、`$parameter`、`$workflow`、`$execution`、日期运算、数组/对象方法 | 能在节点里写复杂数据变换 |
| 5 | 错误处理：Error Trigger, Continue On Fail, Retry, 自定义告警 | 工作流能「不挂、可排查」 |
| 6-7 | 复刻 2 个官方模板（搜 n8n templates CRM/Lead/Content） | 看懂别人怎么组装业务流 |

### Week 2：接入 AI + 实战 2 个完整 Demo

| 天 | 任务 |
|---|------|
| 8 | 搞定 AI Agent 节点 + Vector Store(Qdrant/PGVector) + Embeddings(DeepSeek/BGE) |
| 9 | 做知识库问答：上传 PDF → 切片 → 入库 → 聊天测试 |
| 10 | 做内容生产线：关键词 → 大纲 → 正文 → 审核 → 发飞书/公众号草稿箱 |
| 11 | 加人工审批节点（Wait for Webhook/Email）理解 HITL |
| 12 | 学子工作流/复用、环境变量、Credentials 管理 |
| 13 | 部署生产：Docker + Postgres + Nginx SSL + 基础监控 |
| 14 | 整理成个人作品集：README + 架构图 + 运行录屏 + 部署文档 |

---

## 三、不懂业务时的「作弊获取需求」3 招

| 方法 | 怎么做 | 产出 |
|------|--------|------|
| **招聘 JD 挖掘** | Boss直聘/LinkedIn 搜「运营专员/客服主管/销售运营」，把 JD 里的「职责」抄下来，每条问：这步能不能自动化？ | 50+ 真实痛点清单 |
| **竞品模板反向** | 进 n8n 官方模板库、Make/Zapier 模板库、GitHub Awesome-n8n，按行业筛选，直接抄成品改参数 | 现成可交付方案 |
| **找熟人小老板免费诊断** | 发微信：「哥们帮你自动化个流程，免费，只要你给我讲讲最烦人的重复操作」录音整理 | 真实场景 + 种子用户 + 案例 |

---

## 四、今晚就能跑的最小闭环练习

目标：跑通 `Webhook → AI 摘要 → 飞书群`（15 分钟）

### 起 n8n（本地最快）

```bash
docker run -d --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

进 `http://localhost:5678` 新建工作流。

节点链：**Webhook → HTTP Request (DeepSeek) → HTTP Request (飞书 Webhook) → Respond to Webhook**

### 关键配置

**Webhook**
- URL：`/test/summary`
- Method：POST
- Body 示例：`{ "text": "长文本..." }`

**DeepSeek 节点**
- Method：POST
- URL：`https://api.deepseek.com/v1/chat/completions`
- Header：`Authorization: Bearer YOUR_KEY`
- Body：

```json
{
  "model": "deepseek-chat",
  "messages": [
    {"role": "system", "content": "你是摘要助手，输出 3 句核心要点"},
    {"role": "user", "content": "={{ $json.text }}"}
  ],
  "temperature": 0.3
}
```

**飞书节点**
- Method：POST 到群机器人 Webhook
- Body：`{"msg_type":"text","content":{"text":"摘要：{{ $json.choices[0].message.content }}"}}`

### 测试

```bash
curl -X POST http://localhost:5678/webhook/test/summary \
  -H "Content-Type: application/json" \
  -d '{"text": "你的长文本..."}'
```

跑通后，把这套流程复刻 3 遍（换 Prompt、换输出端），你就懂 n8n 核心骨架了。

---

## 五、第一周作业单

| # | 动作 | 完成标准 |
|---|------|----------|
| 1 | 本地跑通 n8n + 摘要转发流程 | 能在飞书群看到 AI 摘要 |
| 2 | 读完官方 Core Concepts + Expressions + Error Handling 三篇文档 | 能写出 `{{ $json.data.map(x => x.id) }}` |
| 3 | 从模板库导入 1 个 Lead Management 工作流，改成对接你的测试表单/飞书 | 跑通全链路 |
| 4 | 去 Boss 直聘搜 20 个运营/客服/销售运营 JD，把「重复操作」抄进 Notion | 得到 20 个可自动化切入点 |
| 5 | 找 1 个熟人小老板，微信发那段话，约 15 分钟语音 | 录到至少 1 个真实痛点 |

---

## 六、关键心态转变

| 错误心态 | 正确心态 |
|---------|---------|
| 我没客户，不敢做 | 我先做出作品，再找人试用 |
| 要包装成大公司 | 用真实的独立开发者身份，卖的是速度、灵活、懂技术 |
| 要一次搞定大单 | 先跑通 ¥500-2000 的微服务，积累案例和信心 |

不懂业务是常态，技术人员通过「模板化常见业务模式」来补齐，不是靠当顾问。
