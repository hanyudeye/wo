# amix/vimrc 使用手册

> 仓库 `~/.vim_runtime`(amix/vimrc fork),vim 入口 `~/.vimrc`。
> 你的个人配置**只写在 `~/.vim_runtime/my_configs.vim`**(70 行,目前只设了剪贴板和 `kj` 退插入)。
> 改主配置会被 `git pull` 覆盖。
> **leader 键 = `,`**(`basic.vim:46`),下面所有 `,xx` 都先按 `,`。

---

## 零、先记住三个键

| 键        | 作用                                             |
|-----------|--------------------------------------------------|
| `,`       | leader,所有自定义快捷键的起点                    |
| `kj`      | 插入模式下退出插入(你在 `my_configs.vim` 里加的) |
| `,` + `,` | 取消搜索高亮                                     |

---

## 一、打开文件

| 按键 | 作用 | 说明 |
|---|---|---|
| `,j` | **CtrlP 模糊查找当前目录** | ⭐ 最常用。输入几个字母模糊匹配,回车打开 |
| `,nn` | NERDTree 开关 | 右侧文件树 |
| `,nf` | 在文件树中查找当前文件 | 定位当前文件 |
| `,nb` | 打开书签目录 | NERDTree 的 bookmark |
| `,f` | MRU 最近使用文件 | 按使用频率排 |
| `,e` | 打开 `my_configs.vim` | **你的个人配置,改设置就这里** |
| `,q` | 打开 `~/buffer` | 随手记的临时 buffer |
| `,x` | 打开 `~/buffer.md` | 同上,Markdown |
| `:e 路径` | 原生命令打开 | 不带 leader 的兜底 |
| `,te` | **在当前文件所在目录开新标签** | 编辑同目录文件最快的方式 |

### CtrlP 的忽略规则(已配好)

```vim
node_modules | ^\.DS_Store | ^\.git | ^\.coffee
```

所以搜不到 `.git`、`node_modules` 里的文件——这是故意的。

窗口高度上限 20 行(`ctrlp_max_height`)。

### NERDTree 已配

- 位置**右侧**,宽度 35
- 忽略 `*.pyc`、`__pycache__`
- 不显示隐藏文件

---

## 二、Buffer:查看 / 切换

Vim 的 buffer = 已打开的文件列表(不限于窗口)。

| 按键 | 作用 |
|---|---|
| `,b` | **CtrlPBuffer 模糊选 buffer** ⭐ 首选 |
| `,o` | BufExplorer 树形列表(相对路径,按名排序,自动定位当前) |
| `,l` | 下一个 buffer(`:bnext`) |
| `,h` | 上一个 buffer(`:bprevious`) |
| `:ls` | 列出所有 buffer(原生命令,看编号和状态) |
| `,bd` | 关闭当前 buffer 并回到上次窗口 |
| `,ba` | 关闭**所有**其他 buffer(`:bufdo bd`) |

### `,bd` 的实际行为

```vim
map <leader>bd :Bclose<cr>:tabclose<cr>gT
```

**它同时做了三件事**:`:Bclose`(清当前标签页)、`:tabclose`(关标签页)、`gT`(跳回上次标签)。

副作用要知道:如果当前标签页只有这一个 buffer,`:tabclose` 会**把标签页也关掉**。这是设计如此,不是 bug。

---

## 三、关闭与保存

| 按键 | 作用 |
|---|---|
| `,w` | **保存并强制写入**(`:w!`)⭐ 改权限文件也能存 |
| `:w` | 原生保存 |
| `:q` | 关闭当前窗口 |
| `:q!` | 放弃修改强制退出 |
| `,pp` | 切换 paste 模式(粘贴大段文本前先开) |
| `<leader>m` | 去 `^M`(Windows 换行符) |

保存时自动去尾空格:`autocmd BufWritePre` 作用于 `txt/js/py/wiki/sh/coffee`。

---

## 四、标签页(Tab)

| 按键 | 作用 |
|---|---|
| `,tn` | 新建标签页 |
| `,t,` | 切到上一个标签页 |
| `,tc` | 关闭当前标签页 |
| `,to` | 只留当前标签页 |
| `,tm` | 移动当前标签页到后面 |
| `,tl` | 回到上次所在标签页(记忆位置) |
| `Ctrl-w` + `w` | Vim 原生:跳到下一个窗口 |

---

## 五、窗口分屏

`Ctrl-w` + 方向键(已重映射成 vim 风格,免得按 `hjkl` 和移动混淆):

| 按键 | 作用 |
|---|---|
| <kbd>Ctrl-w</kbd> + `h` | 左边窗口 |
| <kbd>Ctrl-w</kbd> + `j` | 下面窗口 |
| <kbd>Ctrl-w</kbd> + `k` | 上面窗口 |
| <kbd>Ctrl-w</kbd> + `l` | 右边窗口 |
| <kbd>Ctrl-w</kbd> + `c` | 关闭窗口 |
| <kbd>Ctrl-w</kbd> + `o` | 只剩当前窗口(全屏) |

---

## 六、编辑常用

| 按键 | 作用 |
|---|---|
| <kbd>Ctrl-p</kbd> | 粘贴 YankStack 里**更早**的内容 |
| <kbd>Ctrl-n</kbd> | 粘贴 YankStack 里**更新**的内容 |
| <kbd>Ctrl-s</kbd> | 多光标:开始选择同词(多条光标) |
| <kbd>Alt-s</kbd> | 多光标:全选所有同词 |
| <kbd>Ctrl-x</kbd> | 多光标:跳过当前 |
| <kbd>Ctrl-j</kbd> | 触发 snipMate 补全 |
| `,ss` | 切换拼写检查 |
| `,sn` / `,sp` | 下一个 / 上一个拼写错误 |
| `,sa` / `,s?` | 加入临时词表 / 拼写建议 |
| `0` | 行首第一个非空字符(重映射自 `^`) |
| <kbd>Alt-j</kbd> / <kbd>Alt-k</kbd> | 上下移动整行 |

### 自动补括号(插入模式)

| 输入 | 得到 |
|---|---|
| `$1` | `()` 且光标在中间 |
| `$2` | `[]` |
| `$3` | `{}` |
| `$4` | 上下各插入 `{}` |
| `$q` | `''` |
| `$e` | `""` |

### 分屏粘贴的正确做法

大段文本粘贴前先 `,pp` 开 paste 模式,粘完再 `,pp` 关掉。否则缩进和自动补全会把文本搞乱。

---

## 七、Git 与检查

| 按键 | 作用 |
|---|---|
| `,d` | 切换 GitGutter(状态栏显示 diff 行) |
| `,g` | 生成 git commit message |
| `,v` | **复制当前行到 GitHub 的 permalink** |
| `,a` | ALE 跳下一个 lint 错误 |
| `,cc` | 打开 `cope` 搜索结果窗口 |
| `,co` | 复制全部内容到新标签并跑 `ggVG` |

ALE 已配 linter:`javascript→eslint`、`python→flake8`、`go→go/golint/errcheck`。

**ALE 只在保存时检查**(`ale_lint_on_text_changed='never'`),不会边打字边报。

GitGutter **默认关闭**(`gitgutter_enabled=0`),要看得按 `,d`。

---

## 八、其他

| 按键 | 作用 |
|---|---|
| `,z` | Goyo 全屏排版阅读模式(宽 100) |
| `,pp` | paste 模式 |
| <kbd>F5</kbd> | 调用 `CompileRun()` 编译并运行(按 `$VIMRUNTIME` 里的配置) |
| <kbd>Ctrl-space</kbd> | 反向搜索 `?` |
| <kbd>Space</kbd> | 向前搜索 `/` |
| `:noh` | 清除搜索高亮(= `,,`) |

---

## 九、搜索

Vim 原生,没被改:

| 按键 | 作用 |
|---|---|
| `/` | 向下搜 |
| `?` | 向上搜 |
| `n` / `N` | 下一个 / 上一个匹配 |
| `*` / `#` | 搜光标下的词(向下 / 向上) |
| `:vimgrep /pat/ **/*.py` | 递归搜索,结果进 quickfix |
| `:copen` | 打开 quickfix 窗口 |

grepprg 已设为 `/bin/grep -nH`,`Grep_Skip_Dirs` 跳过版本控制目录。

---

## 十、状态栏读法

你配置了两套状态栏:

- **lightline**:顶部彩色行。左侧显示模式 / paste 标志 / 文件名(`+` 已改,`-` 只读,`🔒` 只读文件);右侧行号 + 百分比。有 git 仓库时显示当前 commit。
- **statusline**(`laststatus=2`):底部行,显示文件名、修改标记、`CWD`、行号、列号。

`%F%m%r%h` 这几个标记:文件名、修改标志、只读标志、bufhidden。

---

## 十一、怎么改配置

**只改这一个文件:**

```
~/.vim_runtime/my_configs.vim
```

写好后 `:so %` 或重开 vim 生效。按 `,e` 直接打开。

现在里面是:
```vim
set clipboard=unnamedplus        " 剪贴板与系统互通(你已开)
inoremap kj <Esc>                " 插入模式退出的另一选择
```

想加映射就在这加,例如:
```vim
nnoremap <leader>w :write<cr>
```

---

## 待补

- `CompileRun()` 的具体编译/运行配置(在 `sources_forked/vim-compile-run/`?)
- NERDTree 内的常用操作(`a` 新建、`d` 删除、`r` 重命名、`c` 复制、`m` 移动)
- CtrlP 的模糊匹配语法(`%%` 当前词、`..` 父目录、`.` 只当前目录)
- fugitive 的状态栏 commit 显示行为
- 语言服务器(LSP)是否需要额外配置——这个 vimrc 版本里没看到 LSP 相关键位
