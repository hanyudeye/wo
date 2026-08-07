---
---
# Git 学习笔记

> 任务驱动式学习，逐步掌握 Git 核心技能。

---

## 第一阶段：Git 入门基础

**目标** 理解版本控制概念，掌握本地操作流程，能独立完成文件追踪、提交与历史查看。

### 核心任务

| # | 任务 | 命令 |
|---|------|------|
| 1 | 安装 Git 并配置用户信息 | `git config --global user.name` / `user.email` |
| 2 | 初始化仓库 | `git init` |
| 3 | 查看工作区状态 | `git status` |
| 4 | 添加文件到暂存区 | `git add` |
| 5 | 提交到本地仓库 | `git commit -m "消息"` |
| 6 | 查看提交历史 | `git log --oneline` |
| 7 | 查看文件差异 | `git diff` |
| 8 | 配置 `.gitignore` | — |
| 9 | 查看所有配置 | `git config --list` |
| 10 | 测试远程连接 | `ssh -T git@github.com`（私钥需 600 权限） |

### 关键概念

- **工作区 → 暂存区 → 仓库**：三个区域的关系
- `.gitignore` 语法
- 提交信息规范：简洁、有描述性

### 实践

创建 `my-project` 目录 → 初始化 → 添加 `README.md` → 配置 `.gitignore` 忽略 `temp.log` → 至少 3 次提交 → `git log --oneline` 查看历史

### 验收标准

- [ ] 能解释工作区、暂存区、仓库的作用
- [ ] 熟练使用 `add`、`commit`、`status`、`log`、`diff`
- [ ] 正确配置 `.gitignore`

---

## 第二阶段：分支与合并

**目标** 掌握分支操作，理解分支在实际开发中的作用，能安全处理合并冲突。

### 核心任务

| # | 任务 | 命令 |
|---|------|------|
| 1 | 创建并切换分支 | `git branch` / `git switch` |
| 2 | 在不同分支提交 | — |
| 3 | 合并分支 | `git merge` |
| 4 | 解决合并冲突 | 手动编辑 → 提交 |
| 5 | 查看分支图谱 | `git log --graph --oneline --all` |
| 6 | 删除已合并分支 | `git branch -d` |

### 关键概念

- 分支本质：指向提交的指针
- **快进合并** vs **三方合并**
- 冲突标记：`<<<<<<<` / `=======` / `>>>>>>>`

### 实践

基于 `main` 创建 `feature-login` → 添加 `login.py` 并提交两次 → 回 `main` 修改 `README.md`（制造冲突）→ 合并并解决 → `git log --graph` 查看 → 删除分支

### 验收标准

- [ ] 能解释分支的作用
- [ ] 区分快进合并与非快进合并
- [ ] 能独立处理合并冲突
- [ ] 会用 `git log --graph --oneline --all`

---

## 第三阶段：远程仓库协作

**目标** 掌握远程交互核心操作，理解常见协作流程。

### 核心任务

| # | 任务 | 命令 |
|---|------|------|
| 1 | 创建远程仓库 | GitHub/GitLab/Gitee |
| 2 | 关联远程仓库 | `git remote add origin <url>` |
| 3 | 推送到远程 | `git push -u origin main` |
| 4 | 克隆远程仓库 | `git clone <url>` |
| 5 | 拉取最新代码 | `git pull` / `git fetch` |
| 6 | 处理远程冲突 | — |
| 7 | 查看远程信息 | `git remote -v` / `git branch -r` |

### 关键概念

- `origin` / `upstream`（上游分支）
- `git fetch` vs `git pull`
- 远程跟踪分支（如 `origin/main`）

### 实践

推送 `my-project` → 另一目录 `git clone` → 修改并推送 → 原仓库 `git pull` → 制造并解决冲突

### 验收标准

- [ ] 理解 `fetch` 和 `pull` 的区别
- [ ] 能完成推送、拉取、解决远程冲突
- [ ] 理解远程跟踪分支含义
- [ ] 会用 `git clone`

---

## 附：查看文件历史变化

### GitHub 网页端

1. 打开仓库 → 找到文件 → 点击 **History**
2. 点任意 commit 查看该次改动（绿增红删）
3. 勾选两条记录可对比任意两版本差异

快捷链接：
```
https://github.com/用户名/仓库名/commits/分支名/文件路径
```

### 本地命令行

```bash
# 查看文件所有提交
git log --oneline 文件名

# 查看每次提交的详细改动
git log -p 文件名

# 查看改动统计
git log --stat 文件名

# 对比当前与历史版本
git diff a1b2c3 HEAD 文件名

# 对比两个历史版本
git diff 旧commitID 新commitID 文件名
```

### 技巧

- 只看最近 N 条：`git log -p -10 文件名`
- 按作者筛选：`git log --author="用户名" 文件名`
