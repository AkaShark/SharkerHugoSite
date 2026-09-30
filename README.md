# Sharker / Notes

Hugo + [Mana](https://github.com/Livour/hugo-mana-theme) 中文个人博客。
线上地址：<https://akashark.github.io/en/>。

## 快速开始

```bash
./setup.sh
./newDoc.sh tech my-first-note "我的第一篇笔记"
make preview
```

预览地址：<http://localhost:1313/en/>。新文章默认是草稿。
完成正文、摘要和标签，将 `draft: true` 改为 `false` 后：

```bash
make check
./deploy.sh "Publish my first note"
git add content docs
git commit -m "Update blog content"
git push origin master
```

完整说明见 [写作与发布手册](planning/WRITING.md)、[后续写作计划](planning/BACKLOG.md)、[文章整理记录](planning/CONTENT-AUDIT.md)。

## 环境

已验证：macOS Apple Silicon，Hugo Extended 0.167.0，Python 3，Git，rsync。
当前构建不需要 Node.js/npm。`setup.sh` 会安装缺少的 Hugo，并初始化固定版本的 Mana 和发布仓库子模块。
克隆时使用 `git clone --recurse-submodules git@github.com:AkaShark/SharkerHugoSite.git`。

## 常用命令

| 命令 | 用途 |
| --- | --- |
| `make preview` | 本地预览，包括草稿，内存构建 |
| `make drafts` | 列出草稿 |
| `make build` | 构建正式内容、旧链接跳转与 404 到 `.build/site/` |
| `make check` | 构建并检查地址冲突、正文/摘要/标签、站内链接、RSS、搜索、草稿隔离 |
| `make deploy` | 检查后推送 GitHub Pages 发布仓库 |

`docs/` 是独立发布仓库，`deploy.sh` 只提交推送该仓库，不自动提交文章源码。
主仓库的源码变更需另行提交。主题和配置变更也应一起提交。
GitHub Pages 构建状态可在发布仓库的 Actions 查看。

正式同步会删除不再生成的旧页面和旧资源；Git 元数据与 CNAME 会保留。
旧文章链接通过固定 `url` 和 `planning/redirects.json` 维护。
`public/` 和 PaperMod 是历史文件，本次未删除，当前构建不使用。
