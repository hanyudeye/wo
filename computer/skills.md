# last30days 技能简介

> 版本: v3.18.3 | 安装路径: `~/.agents/skills/last30days-skill/`

## 是什么

`/last30days` 是一个社区研究技能，能跨 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket 等平台，抓取某个话题最近 30 天内人们**实际在讨论什么**。它不只是搜索引擎 - 它会把找到的内容按故事/主题聚类，提炼社区观点，引用真实评论。

## 基本用法

```
/last30days <话题>
```

**示例：**
- `/last30days Kanye West` - 人物/事件
- `/last30days Claude Code vs Cursor` - 产品对比
- `/last30days trending` - 发现当前热门话题
- `/last30days AI agents` - 概念/技术

## 查询类型（自动识别）

| 类型                | 触发方式                        | 输出特点                         |
|---------------------|---------------------------------|----------------------------------|
| **GENERAL**         | 默认                            | 叙述式总结 + 关键发现            |
| **COMPARISON**      | 含 `vs` 或 `versus`             | 对比表格 + 各方优劣              |
| **RECOMMENDATIONS** | 含 `best`、`top`、`recommended` | 排名列表（按信号质量排序）       |
| **NEWS**            | 含 `news`、`what's happening`   | 近期动态                         |
| **DISCOVERY**       | `trending` 或 `--trending`      | 三阶段协议：提名→研究→输出角度 |

## 关键特性

**多源聚合** - 同时搜索 Reddit（带评论）、X、YouTube（带字幕）、TikTok、HN、Polymarket 等，找到跨平台出现的故事。

**社区声音优先** - 引用真实用户评论（带投票数），不只是新闻标题。一条 1338 票的 Reddit 评论比一篇新闻稿信息量更大。

**自动保存** - 每次研究的原始数据保存到 `~/Documents/Last30Days/`，可随时回顾。

**对比模式** - 对两个或多个实体做深度对比，自动为每个实体独立搜索。

**发现模式** - 三阶段主机判断协议：引擎提名 → 你判断价值 → 引擎研究 → 你写内容角度 → 引擎渲染。

## 首次使用

首次运行会触发设置向导（约 30 秒）：
1. 扫描浏览器 cookie 解锁 X/Twitter 搜索（可选）
2. 安装 yt-dlp（YouTube）、Digg CLI、arXiv、Techmeme
3. 可选：注册 ScrapeCreators 获取 TikTok、Instagram 覆盖（10000 免费调用）

**免费即可用的源：** Reddit（含评论）、HN、Polymarket、GitHub、Web

## 常用后缀

| 参数 | 作用 |
|------|------|
| `--days=N` | 只看最近 N 天 |
| `--quick` | 快速模式，源数量较少 |
| `--deep` | 深度模式，50-70 条 Reddit |
| `--emit=html` | 输出 HTML 格式 |
| `--agent` | 代理模式，自动运行不等待 |

## 数据保存

研究结果自动保存为 Markdown 文件到 `~/Documents/Last30Days/`，文件名格式 `{slug}-raw.md`。可用 `library` 命令管理已保存的研究：

```
/last30days search my library for AI agents
/last30days what's in my topic queue
/last30days mark AI agents as covered
```

## 环境变量（可选）

写入 `~/.config/last30days/.env`：

| 变量                           | 作用                                |
|--------------------------------|-------------------------------------|
| `FROM_BROWSER=auto`            | 用浏览器 cookie 访问 X              |
| `XAI_API_KEY=xxx`              | xAI API 密钥（替代浏览器）          |
| `SCRAPECREATORS_API_KEY=xxx`   | TikTok/Instagram + Reddit 备份      |
| `BRAVE_API_KEY=xxx`            | Brave 搜索后端                      |
| `LAST30DAYS_REGISTER=dev`      | 默认寄存器（dev/exec/creator/eli5） |
| `FUN_LEVEL=high`               | 更多趣味内容                        |
| `LAST30DAYS_MEMORY_DIR=~/path` | 自定义保存路径                      |
