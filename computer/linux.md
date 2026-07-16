# Linux 学习路径与实战

---

## Phase 1：基础概念与命令行入门

**目标：** 理解 Linux 工作原理和文件系统结构，掌握终端基本操作。

### 知识点

- Shell (Bash)、CLI（命令行界面）
- 文件系统层次标准 (FHS)
- 绝对路径 vs 相对路径
- 输入/输出重定向 (`>`, `>>`, `<`)
- 基本文件权限概念（用户、组）

### 核心命令

```bash
pwd          # 当前工作目录
ls           # 列出文件
cd           # 切换目录
mkdir/rmdir  # 创建/删除目录
touch        # 创建空文件
cp/mv        # 复制/移动
cat/less     # 查看文件内容
```

### 实践任务

1. 创建主目录 `学习项目`，内含 `文档` 和 `代码` 两个子目录
2. 在 `文档` 下用命令行创建 `readme.txt`（内容："你好"）
3. 回到主目录，将 `readme.txt` 移动到新建的 `备用资料` 目录中

### 验收标准

- 能用绝对/相对路径描述从任意起点到达目标的命令组合
- 操作后用 `tree` 或 `ls -R` 验证目录结构正确

---

## Phase 2：进阶数据处理与权限管理

**目标：** 掌握管道、文本搜索/筛选、权限模型和进程管理。

### 知识点

- 管道符 (`|`) 与标准流 (stdin/stdout/stderr)
- 正则表达式 (Regex)
- 八进制/符号权限 (chmod)
- 进程 ID (PID)
- `find` 命令选项

### 核心命令

```bash
grep             # 文本搜索
find             # 文件定位
chmod/chown      # 修改权限/所有者
ps/top           # 查看进程
wc/sort/uniq     # 统计/排序/去重
awk              # 字段处理
```

### 实践任务

1. 创建包含多个模拟日志文件的目录结构
2. 用 `grep` + 管道搜索包含 "Error 404" 的文件名列表
3. 用 `awk` 提取错误记录的时间戳和 IP 地址
4. 修改某个日志文件权限，仅 root 可读写

### 验收标准

- 能解释 `cat file | grep pattern | sort | uniq -c` 每一步的作用
- 能根据场景选择 `find` 或通配符，并正确使用权限管理命令

---

## Phase 3：Shell 脚本自动化与系统服务

**目标：** 编写可重复的自动化脚本，理解 systemd 服务管理。

### 知识点

- Shebang (`#!`)
- 位置参数 (`$1`, `$2`, `$@`)
- 循环结构 (for, while)
- 条件判断 (if/elif/else)
- Systemd / Init 系统

### 脚本示例

```bash
#!/bin/bash
# 接受起始/结束年份，创建月份日志文件
START=$1
END=$2
for year in $(seq $START $END); do
    for month in $(seq -w 1 12); do
        touch "log_${year}_${month}.txt"
    done
done
```

### 实践任务

1. 编写脚本：接受起止年份参数，用循环创建月份日志文件
2. 执行网络诊断：ping、检查端口监听，报告进程 PID

### 验收标准

- 脚本能运行，包含 if 判断和循环两种流程控制
- 能解释网络诊断命令链，指出 PID 和端口状态

---

## Phase 4：高级数据处理与网络排查

**目标：** 掌握 sed/awk 高级用法，理解网络协议基础。

### 知识点

- GNU Awk (FS, RS 字段/记录分隔符)
- Sed 替换语法 (`s/pattern/replacement/flags`)
- 正则表达式分组捕获
- IP 子网掩码
- DNS 解析过程 / TTL

### 核心命令

```bash
sed 's/foo/bar/g'        # 全局替换
awk -F: '{print $1}'    # 指定分隔符提取字段
dig/nslookup             # DNS 查询
ping                     # 连通性测试
```

### 实践任务

1. 从模拟 Web 日志中筛选 HTTP 404 记录，提取 IP 和 URL，格式化为 "IP: URL"
2. 用命令行验证外部服务的 DNS 解析和数据传输，说明测试了哪两个层面

### 验收标准

- 能描述复杂管道链的执行流程和各部分功能
- 能区分"网络连接问题"和"服务本身问题"并初步定性判断

---

## Phase 5：容器化、版本控制与系统优化

**目标：** 跨环境部署和团队协作能力，工业级日志与故障排除。

### 知识点

- Docker (镜像、容器、Dockerfile)
- Git 工作流（分支策略、合并冲突）
- 日志管理 / 集中日志
- 资源监控 (CPU/Memory/I/O)
- 任务调度 (cron, systemd timers)

### Dockerfile 示例

```dockerfile
FROM ubuntu:24.04
COPY backup.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/backup.sh
CMD ["/usr/local/bin/backup.sh"]
```

### 实践任务

1. 将备份脚本封装为 Docker 镜像，在任意环境运行
2. 用 `crontab` 设置每分钟清理临时文件的任务，模拟排查失败原因

### 验收标准

- 能解释容器化相比直接在宿主机运行的优势
- 能按"发现→定位→记录→修复→验证"流程处理故障

---

## SSH 实战

### ssh-add 的作用

把 SSH 私钥加载到 SSH Agent，让后续 SSH/Git 操作无需反复输入 passphrase，也无需每次指定私钥文件。

**认证流程对比：**

```
无 agent：  git → ssh → 读取私钥 → 输入 passphrase → 成功
有 agent：  git → ssh → 询问 agent → agent 已有私钥 → 直接成功
```

### 什么时候需要 ssh-add

**场景 1：私钥设置了 passphrase（最常见）**

```bash
ssh-keygen -t ed25519          # 会提示设置 passphrase
eval "$(ssh-agent -s)"        # 启动 agent
ssh-add ~/.ssh/id_ed25519     # 输入一次 passphrase，后续免输
```

**场景 2：多个 SSH 密钥**

```bash
ssh-add ~/.ssh/id_ed25519_github
ssh-add ~/.ssh/id_ed25519_work
ssh-add -l                     # 查看已加载的密钥
```

**场景 3：多工具共享认证**

Git、VS Code、Emacs (Magit)、scp、rsync、ssh 都使用同一个 ssh-agent。

### 常用命令

```bash
eval "$(ssh-agent -s)"   # 启动 agent
ssh-add ~/.ssh/xxx       # 添加密钥
ssh-add -l               # 列出已加载
ssh-add -L               # 列出公钥
ssh-add -d ~/.ssh/xxx    # 删除一个
ssh-add -D               # 删除全部
```

### 配置文件位置

| 文件 | 说明 |
|------|------|
| `~/.ssh/id_ed25519` | 私钥（默认目录 `~/.ssh/`） |
| `~/.ssh/config` | SSH 配置（`IdentityFile` 指定私钥） |
| `ssh-agent` 进程 | 后台进程，通过 `$SSH_AUTH_SOCK` 通信 |

### 指定私钥的几种方式

| 方式 | 示例 | 优点 | 缺点 |
|------|------|------|------|
| `~/.ssh/config` 的 `IdentityFile` | `IdentityFile ~/.ssh/id_ed25519` | 一劳永逸，按 Host 匹配 | 需手动编辑 |
| `ssh -i` 参数 | `ssh -i ~/.ssh/id_ed25519 user@host` | 临时指定 | 每次手动输入 |
| `ssh-add` 加到 agent | `ssh-add ~/.ssh/id_ed25519` | 会话内所有操作复用 | agent 重启后失效 |
| `AddKeysToAgent yes` | 加到 `~/.ssh/config` | 首次使用自动加入 agent | 需配合 ssh-agent |
| GNOME Keyring | Ubuntu 24.04 默认 | 登录时自动解锁，无感 | 仅 GNOME 桌面 |

> `IdentityFile` 是告诉 SSH 该试哪个私钥，`ssh-add` 是把私钥加载到 agent 内存。推荐配置：`IdentityFile` + `AddKeysToAgent yes`。

### User git 是什么

GitHub/GitLab/Bitbucket/Gitee 的 SSH 用户名都固定为 `git`。认证靠密钥反查身份，`User git` 只是连接用户名。

### 推荐配置（Ubuntu 24.04）

```sshconfig
Host github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    AddKeysToAgent yes
```

### 开机自动加载

```bash
# ~/.bashrc 或 ~/.zshrc
if ! pgrep -u "$USER" ssh-agent >/dev/null; then
    eval "$(ssh-agent -s)"
fi
ssh-add ~/.ssh/id_ed25519 2>/dev/null
```

更推荐在 `~/.ssh/config` 中使用 `AddKeysToAgent yes`，首次使用时自动加入。

### SSH 基本用法

1. 本地生成密钥对：`ssh-keygen -t ed25519 -f ~/.ssh/xxx`
2. 把公钥 (`xxx.pub`) 追加到远程机器的 `~/.ssh/authorized_keys`
3. 本地用私钥连接
