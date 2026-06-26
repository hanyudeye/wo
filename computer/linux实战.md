##  ssh-add 有什么用，什么时候用

`ssh-add` 的作用是：

> **把 SSH 私钥加载到 SSH Agent（`ssh-agent`）中，让后续 SSH、Git 等操作无需反复输入私钥密码（passphrase），也无需每次指定私钥文件。**

它**不会修改私钥**，也**不会写入 `~/.ssh/config`**。它只是把密钥交给一个后台代理进程管理。

---

# SSH 认证流程

假设你的私钥：

```text
~/.ssh/id_ed25519
```

连接 GitHub：

```bash
git push
```

默认流程：

```
git
 │
 ▼
ssh
 │
 ▼
读取 ~/.ssh/id_ed25519
 │
 ▼
需要输入 passphrase
 │
 ▼
登录成功
```

如果用了 `ssh-agent`：

```
git
 │
 ▼
ssh
 │
 ▼
询问 ssh-agent
 │
 ▼
ssh-agent 已保存私钥
 │
 ▼
直接认证成功
```

因此，一次登录后，后续所有 SSH 操作都可以复用已加载的密钥。

---

# 什么时候需要 `ssh-add`

## 场景 1：私钥设置了 passphrase（最常见）

例如：

```bash
ssh-keygen -t ed25519
```

会提示：

```text
Enter passphrase:
```

之后每次：

```bash
git pull
```

都会要求输入 passphrase。

执行：

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

输入一次 passphrase 后，直到 agent 退出都不用再输入。

---

## 场景 2：有多个 SSH 密钥

例如：

```text
~/.ssh/id_ed25519_github
~/.ssh/id_ed25519_gitlab
~/.ssh/id_ed25519_work
```

加载：

```bash
ssh-add ~/.ssh/id_ed25519_github
ssh-add ~/.ssh/id_ed25519_work
```

查看：

```bash
ssh-add -l
```

输出：

```text
256 SHA256:...
256 SHA256:...
```

---

## 场景 3：Git、VS Code、Emacs、终端共享认证

例如：

```
Emacs Magit
VS Code
git
scp
rsync
ssh
```

都使用同一个 `ssh-agent`。

---

# 常用命令

启动 agent：

```bash
eval "$(ssh-agent -s)"
```

添加密钥：

```bash
ssh-add ~/.ssh/id_ed25519
```

查看已加载：

```bash
ssh-add -l
```

查看详细：

```bash
ssh-add -L
```

删除一个：

```bash
ssh-add -d ~/.ssh/id_ed25519
```

删除全部：

```bash
ssh-add -D
```

---

# Linux 配置在哪里？

## 1. 私钥

默认目录：

```text
~/.ssh/
```

例如：

```text
~/.ssh/id_rsa
~/.ssh/id_ed25519
```

---

## 2. SSH 配置

文件：

```text
~/.ssh/config
```

例如：

```sshconfig
Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

注意：

> `ssh-add` **不会修改这个文件**。

---

## 3. ssh-agent

不是配置文件，而是一个后台进程。

查看：

```bash
ps -ef | grep ssh-agent
```

例如：

```text
ssh-agent
```

环境变量：

```bash
echo $SSH_AUTH_SOCK
```

例如：

```text
/run/user/1000/keyring/ssh
```

或：

```text
/tmp/ssh-XXXXXX/agent.12345
```

这是 SSH 与 agent 通信使用的 Unix Socket。

---

# Ubuntu 24.04 一般不需要手动运行 `ssh-add`

如果你使用 **GNOME** 登录，通常会自动启动 GNOME Keyring，它会充当 SSH Agent。

可以检查：

```bash
echo $SSH_AUTH_SOCK
```

如果有输出，再查看：

```bash
ssh-add -l
```

如果已经显示你的密钥，说明系统已经帮你管理了。

---

# 如何开机自动加载 SSH 密钥？

如果不是使用 GNOME Keyring，而是标准 `ssh-agent`，可以在 `~/.bashrc` 或 `~/.zshrc` 中启动 agent，并加载密钥：

```bash
if ! pgrep -u "$USER" ssh-agent >/dev/null; then
    eval "$(ssh-agent -s)"
fi

ssh-add ~/.ssh/id_ed25519 2>/dev/null
```

不过，这种方式每次开启新终端都可能尝试加载密钥，不如使用专门的 agent 管理。

更推荐的是利用 OpenSSH 的配置自动添加：

```sshconfig
Host *
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519
```

这样首次使用该密钥时，OpenSSH 会自动把它加入当前的 agent（前提是已有可用的 `ssh-agent`）。

---

# 推荐配置（Ubuntu 24.04 + GNOME）

建议采用：

* 私钥：`~/.ssh/id_ed25519`
* `~/.ssh/config`：

```sshconfig
Host github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    AddKeysToAgent yes
```

* 使用 GNOME Keyring 或 `ssh-agent` 管理密钥
* 通过 `ssh-add -l` 检查密钥是否已加载

这种配置兼容 Git、SSH、Emacs（如 Magit）、VS Code 等绝大多数开发工具。

---

# 指定使用哪个私钥的几种方式

总的目的是让 SSH 知道用哪个私钥去认证，各方法对比：

| 方式 | 示例 | 优点 | 缺点 |
|------|------|------|------|
| **`~/.ssh/config` 中的 `IdentityFile`** | `IdentityFile ~/.ssh/id_ed25519` | 一劳永逸，按 Host 自动匹配 | 需要手动编辑配置文件 |
| **`ssh -i` 参数** | `ssh -i ~/.ssh/id_ed25519 user@host` | 临时指定，不写配置文件 | 每次都要手动输入，Git 等工具无法自动使用 |
| **`ssh-add` 加到 agent** | `ssh-add ~/.ssh/id_ed25519` | 一次添加，会话内所有 SSH 操作复用 | agent 重启后失效，需重新添加 |
| **`AddKeysToAgent yes`** | 加到 `~/.ssh/config` | 首次使用后自动加入 agent，后续免输入 | 需配合已有的 `ssh-agent` 使用 |
| **GNOME Keyring** | Ubuntu 24.04 默认 | 登录时自动解锁密钥，完全无感 | 仅适用于 GNOME 桌面环境 |
| **`~/.bashrc` / `~/.zshrc` 自动 `ssh-add`** | 启动 shell 时执行 `ssh-add` | 简单直接 | 每次开终端弹窗输密码，不推荐 |

> 注意：`~/.ssh/config` 的 `IdentityFile` 是**告诉 SSH 该试哪个私钥**，`ssh-add` 是**把私钥加载到 agent 内存**。两者解决的问题不同，可以配合使用。推荐 `~/.ssh/config` 写 `IdentityFile` + `AddKeysToAgent yes`，兼顾自动匹配和免密码。

---

# `User git` 中的 `git` 是什么？

配置中的 `User git` 不是 GitHub 账户名，而是 **GitHub 统一的 SSH 用户名**。

GitHub 规定所有 SSH 连接的用户名都固定为 `git`，实际认证靠 SSH 密钥来识别你是谁。类似的还有：

| 平台 | SSH 用户名 |
|------|-----------|
| GitHub | `git` |
| GitLab | `git` |
| Bitbucket | `git` |
| Gitee | `git` |

所以无论你在 GitHub 上叫什么用户名，SSH 配置里都写 `User git`。SSH 只会用这个用户名连接到服务器，服务器再根据你提供的 SSH 公钥反查你的身份。`IdentityFile` 指定的私钥才是真正决定"你是谁"的关键。


## ssh 的用法

1. 本地生成密钥对：ssh-keygen -t ed25519 -f ~/.ssh/xxx
2. 把公钥（xxx.pub）追加到远程机器的 ~/.ssh/authorized_keys 里
3. 本地用私钥连接
也就是你在本地生成 key，把公钥贴到 服务器 上。不需要从远程机器复制什么下来。


## linux 下有同 wgesture 类似的手势软件吗 

没有好用的类似软件

