---
---
# 在 WSL2 Ubuntu 中安装 Docker

推荐直接安装 Docker Engine（不必用 Docker Desktop），适用于 WSL2 里的 Ubuntu。

## 一、安装 Docker Engine

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 二、启动服务

- 未启用 systemd：

```bash
sudo service docker start
```

- 已启用 systemd：

```bash
sudo systemctl enable --now docker
```

## 三、免 sudo 使用 docker

```bash
sudo usermod -aG docker $USER
```

需要重新登录（或 `wsl --shutdown` 后重开）才生效。

## 四、开机自启（可选）

在 `/etc/wsl.conf` 中加入：

```ini
[boot]
systemd=true
```

然后在 Windows 中执行 `wsl --shutdown` 重启 WSL，重开 Ubuntu 后服务会自动启动。

## 五、验证

```bash
docker run hello-world
```

输出 `Hello from Docker!` 即安装成功。
