# SharkerBlog

Hugo + PaperMod 博客，发布到 <https://akashark.github.io/>。
已验证环境：macOS Apple Silicon、Hugo 0.167.0（Homebrew）。
主题包含在源码中，不需要 Node.js 或 npm。

## 环境准备

```bash
git clone --recurse-submodules git@github.com:AkaShark/SharkerHugoSite.git
cd SharkerHugoSite
./setup.sh
```

已有这个目录时直接运行 `./setup.sh`。脚本会在缺少 Hugo 时通过 Homebrew
安装，并初始化发布仓库。需要已安装 Git、Homebrew，以及有权推送两个仓库的
GitHub SSH 登录。主题兼容性修改已随源码保存；升级 Hugo 后先运行 `make build`。

## 写文章与预览

```bash
./newDoc.sh "tech/我的新文章.md"
make preview
```

打开 <http://localhost:1313/en/>。新文章在 `content/posts/` 中，默认为
`draft: true`，预览会显示草稿。确认内容后改成 `draft: false`；未来日期的文章
不会进入正式构建。日期含时区，请按实际发布时间设置。按 Ctrl+C 停止预览。

`make build` 只生成正式内容到 `.build/site/`，不发布。预览在内存中构建，
不会修改仓库里历史遗留的 `public/` 文件。

## 发布

```bash
./deploy.sh "Publish my new article"
```

脚本检查 `docs/` 工作区和分支，从远端快进更新，在独立目录构建成功后同步到
`docs/`，提交并推送 `AkaShark/AkaShark.github.io` 的 `master` 分支。
GitHub Pages 使用该分支根目录发布，通常需要等待几分钟。
构建失败会立即停止，草稿不会发布；无内容变化时也可重复运行。

为保留旧文章地址，同步不会自动删除历史发布文件。如果需要撤下文章，除了
修改源文件，还要单独检查并删除 `docs/` 中对应的历史 HTML；不能仅靠草稿标记
撤下之前已公开的内容。

发布只推送静态站点。保存文章源码和新的子模块版本时，在主仓库另行提交推送：

```bash
git add content docs
git commit -m "Update blog content"
git push origin master
```

如果还修改了配置或模板，把相应文件一起加入提交。

## 目录

- `content/`：文章与页面。
- `themes/hugo-PaperMod/`：随仓库保存的主题。
- `layouts/`：自定义模板（包含首页全文 RSS）。
- `config.yaml`：站点设置。
- `docs/`：GitHub Pages 发布仓库子模块。
- `.build/`：忽略提交的本地构建产物。
- `public/`：历史构建产物，当前脚本不使用它。
