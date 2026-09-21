给我在zshrc配置一个可以任意切换代理的函数，默认使用代理


```zsh
# ===================== 代理管理 =====================
# 默认代理地址（改成你自己的）
PROXY_DEFAULT="http://127.0.0.1:10808"

# 预设代理，键名可任意，用法：proxy clash
typeset -gA PROXY_PRESETS=(
  clash   "http://127.0.0.1:7890"
  v2ray   "http://127.0.0.1:10809"
  socks   "socks5://127.0.0.1:1080"
)

# 不走代理的地址
PROXY_NO="localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,*.local"

proxy() {
  local addr

  case "$1" in
    off|none|0)
      unset http_proxy https_proxy all_proxy ftp_proxy
      unset HTTP_PROXY HTTPS_PROXY ALL_PROXY FTP_PROXY
      unset no_proxy NO_PROXY
      echo "🚫 代理已关闭"
      return
      ;;
    list|ls)
      echo "预设代理："
      local k
      for k in ${(k)PROXY_PRESETS}; do
        printf "  %-8s %s\n" "$k" "${PROXY_PRESETS[$k]}"
      done
      [[ -n $http_proxy ]] && echo "\n当前代理：$http_proxy"
      return
      ;;
    ""|on)
      addr="${2:-$PROXY_DEFAULT}"      # proxy on / proxy 用默认
      ;;
    *)
      if (( ${+PROXY_PRESETS[$1]} )); then
        addr="${PROXY_PRESETS[$1]}"     # 预设名
      elif [[ "$1" == *:* ]]; then
        addr="$1"                       # 直接给地址/端口
      else
        echo "未知代理：$1"; proxy list; return 1
      fi
      ;;
  esac

  [[ "$addr" != *://* ]] && addr="http://$addr"   # 自动补协议

  export http_proxy="$addr"  https_proxy="$addr"  all_proxy="$addr"  ftp_proxy="$addr"
  export HTTP_PROXY="$addr"  HTTPS_PROXY="$addr"  ALL_PROXY="$addr"  FTP_PROXY="$addr"
  export no_proxy="$PROXY_NO" NO_PROXY="$PROXY_NO"

  echo "✅ 代理已开启：$addr"
}

# 默认开机启用代理（不想默认开启就注释掉这行）
proxy on >/dev/null 2>&1
```

用法：

- `proxy` / `proxy on` → 开启默认代理
- `proxy off` → 关闭代理（`none`、`0` 同义）
- `proxy clash` → 切换到预设
- `proxy 127.0.0.1:8888` → 临时指定任意地址（自动补 `http://`）
- `proxy socks5://127.0.0.1:1080` → 直接给完整地址
- `proxy list` → 查看所有预设和当前状态

注意：zshrc 里改完执行 `source ~/.zshrc` 生效；如果也想让 git 走代理，可在 `proxy` 函数里追加：

```zsh
git config --global http.proxy "$addr" 2>/dev/null
```

关闭分支里对应加上 `git config --global --unset http.proxy`。
