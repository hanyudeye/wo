---
---
# Docsify 一键发布 Markdown 到 GitHub Pages

## 思路

- Docsify 是纯静态文件，**不需要 gh-pages 分支**，也**不需要 GitHub Actions**
- 把 `index.html` 放仓库根目录，GitHub Pages 发布源选 `main` 分支 + `/` 根目录即可
- 所有 `.md` 文件自动成页面，改完 push 即生效

## 文件结构

```
仓库根/
├── index.html      # Docsify 入口
├── README.md       # 首页内容
└── _sidebar.md     # 侧边栏导航
```

## index.html 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>文档</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: '我的知识库',
      repo: '用户名/仓库名',      // 可选，显示 github 角标
      search: 'auto',            // 全文搜索
      maxLevel: 3,               // 侧边栏显示到几级标题
      loadSidebar: true          // 启用 _sidebar.md
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/docsify.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
</body>
</html>
```

## 配套文件

`_sidebar.md`：

```markdown
- [首页](/)
- [Emacs](computer/emacs.md)
```

## 初始化与本地预览

```sh
mkdir docs                # 新建空目录（init 会在已有目录时交互询问覆盖）
cd docs
npx docsify-cli init .    # 生成 index.html + README.md + .nojekyll
npx docsify-cli serve .   # 本地预览 http://localhost:3000
```

注意：`npx docsify serve` 会报 `could not determine executable`，必须用 **`docsify-cli`** 这个包名。

## GitHub 发布

1. 仓库 Settings → Pages
2. **Deploy from a branch** → 选 `main` + `/ (root)` → Save
3. 推送即上线：`git add -A && git commit -m "docsify" && git push`
