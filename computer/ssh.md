# SSH 教程

## 基本用法

```bash
ssh user@host           # 默认端口22
ssh -p 2222 user@host   # 指定端口
ssh -i ~/.ssh/mykey user@host  # 指定密钥
```

## 密钥生成

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# 生成 ~/.ssh/id_ed25519（私钥）和 ~/.ssh/id_ed25519.pub（公钥）
```

## 公钥部署到服务器

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host
```

手动方式：
```bash
cat ~/.ssh/id_ed25519.pub | ssh user@host 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
```

## 多台电脑登录同一服务器

每台电脑生成自己的密钥，公钥都追加到服务器的 `~/.ssh/authorized_keys`，一行一条。

```bash
# 在每台电脑上
ssh-keygen -t ed25519
ssh-copy-id user@server
```

## 权限问题（常见故障）

SSH 对权限很敏感，公钥认证失败 99% 是权限问题：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

Home 目录也不能太开放：
```bash
chmod 755 ~
```

CentOS/RHEL 还需：
```bash
restorecon -Rv ~/.ssh
```

## SSH Config 配置

编辑 `~/.ssh/config`，简化连接：

```
Host myserver
    HostName 192.168.1.100
    User root
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host work
    HostName work.example.com
    User deploy
    IdentityFile ~/.ssh/work_key
```

之后直接：
```bash
ssh myserver
ssh work
```

## 端口转发

```bash
# 本地转发：访问本地8080 -> 远程的localhost:80
ssh -L 8080:localhost:80 user@host

# 远程转发：访问远程8080 -> 本地的localhost:80
ssh -R 8080:localhost:80 user@host

# 动态转发（ SOCKS 代理）
ssh -D 1080 user@host
```

## 文件传输

```bash
scp file.txt user@host:/path/         # 上传
scp user@host:/path/file.txt ./       # 下载
scp -r ./dir user@host:/path/         # 递归复制目录
rsync -avz ./dir user@host:/path/     # 增量同步
```

## 跳板机 / ProxyJump

```bash
ssh -J jump_host user@target_host
```

Config 写法：
```
Host target
    HostName 10.0.0.5
    User root
    ProxyJump jump_host
```

## 免密登录（Agent Forwarding）

```bash
ssh -A user@host    # 转发本地密钥到跳板机
```

Config 中：
```
Host jump
    HostName jump.example.com
    User admin
    ForwardAgent yes
```

## 调试

```bash
ssh -vvv user@host   # 详细输出，排查问题
```

## 常见问题

**Q: 还是要输入密码？**
- 检查权限（见上方）
- 服务器日志：`tail -f /var/log/auth.log` 或 `journalctl -u sshd -f`
- 用 `-vvv` 看具体哪一步失败
 
**Q: 连接慢？**
- 禁用 DNS 反向解析：`UseDNS no` 在 `/etc/ssh/sshd_config`

**Q: 密钥被拒绝？**
- 确认公钥内容完整，没有换行
- 检查 `~/.ssh/authorized_keys` 文件权限
- 检查 `sshd_config` 中 `PubkeyAuthentication yes`
