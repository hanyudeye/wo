# wo — 个人知识库 / second brain

## 结构

```
computer/    计算机技术（编程、Linux、Emacs、AI、工具等）
living/      生活知识（语言学习、健康、心理、烹饪等）
startup/     创业与赚钱（AI产品、投资、商业等）
books/       读书笔记
技术/
  编码术/       python脚本、n8n工作流
  计算机文档/   Chrome、MySQL、WSL、资源链接等
  其他术/       金融、旅行、外语
  生活术/       记账、常识
```

## 写作惯例

- 内容以**中文为主**，文件名可使用中文/英文混用
- Markdown 为主，偶有 `.org`、`.html`、`.pdf`
- 部分 `.md` 文件包含 AI 对话记录或 prompt 模板（如 emacs.md、linux.md 开头是学习教练 prompt）
- 用 `- ` 无序列表和中文标点，标题用 `##`/`###`

## 操作要点

- **没有**构建/测试/lint 系统 — 纯文档仓库，直接提交即可
- 添加新文件时，放入对应分类目录；拿不准就放在最相关的目录下
- Git: `main` 分支，origin 是 `git@github.com:hanyudeye/wo.git`
- Python 脚本在 `技术/编码术/python/` 和 `技术/编码术/script/` 下，有独立的 `.gitignore`

## 通用原则

- 优先用中文回答
- 文件是知识卡片，不是教程。保持简短、实用
- 如果某个话题没有对应目录，可以先创建，但保持顶层目录简洁
