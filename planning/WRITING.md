# 写作与发布手册

## 日常使用

在仓库根目录执行。环境准备一次即可：`./setup.sh`。

```bash
# 技术 / 阅读 / 生活分别使用 tech / read / life
./newDoc.sh tech wkwebview-navigation "WKWebView 导航问题排查"
./newDoc.sh read book-notes "一本书带来的三个问题"
./newDoc.sh life monthly-review "这个月的行动复盘"

# 专题文章
./newDoc.sh tech go-context "Go context 的取消与超时" --series "Go 语法速通" --order 4

# 本地预览（包括草稿）
make preview
# http://localhost:1313/en/，Ctrl+C 停止

# 列出草稿 / 检查正式构建
make drafts
make check

# 确认 draft: false 后发布
./deploy.sh "Publish WKWebView notes"

# 另存源码（静态站点发布不等于文章源码备份）
git add content docs
git commit -m "Publish WKWebView notes"
git push origin master
```

`newDoc.sh` 会创建 `content/posts/<栏目>/<年>/<slug>/index.md`。
例：`content/posts/tech/2026/wkwebview-navigation/index.md`。
短链接固定为 `/en/posts/tech/wkwebview-navigation/`，以后改标题、改文件夹不会改变地址。
`slug` 用小写英文和连字符，一经发布尽量不改。
旧用法 `./newDoc.sh "tech/文章名.md"` 仍可用，但新文章推荐使用上面的页面包方式。

## 分类、标签与专题

- **栏目 categories**：只选一个，`技术`、`阅读`、`生活`。目录中的 tech/read/life 与之对应。
- **标签 tags**：选 2–4 个具体主题，例如 `iOS`、`WKWebView`、`HTTP`。每个标签独立填写，不能把几个词挤在一个字符串里。
- **专题 series**：只有连续、有阅读顺序的内容才设置；专题名一致即可自动归集。`series_order` 控制阅读顺序，不影响首页按发表日期排序。
- **description**：用一句话说明读者能获得什么。它会出现在首页、列表和搜索摘要。
- **date**：真实首次发表时间。初稿默认创建时间，发布时按实际情况修改；未来时间的文章在当前构建中不会发布。
- **lastmod**：实质更新时修改，不用为了换主题刷新所有旧文章的时间。
- **draft**：`true` 只在本地草稿预览中可见，`false` 才进入正式构建。
- **url**：历史文章已经固定；新文章由工具生成。不要为了改标题而修改它。

```yaml
title: "WKWebView 导航问题排查"
date: "2026-09-30T12:00:00-04:00"
lastmod: "2026-09-30T12:00:00-04:00"
url: "/en/posts/tech/wkwebview-navigation/"
author: "Sharker"
categories: ["技术"]
tags: ["iOS", "WKWebView"]
description: "从回调顺序到复现案例，定位 WKWebView 导航异常。"
draft: true
# 可选
series: ["iOS 开发实践"]
series_order: 3
```

## 图片与引用

把图片放在同一文章目录，如 `navigation.png`，正文写 `![导航回调顺序](navigation.png)`。
这样正文和素材一起备份，避免依赖外部图床。不要把个人隐私、令牌或公司内部截图提交到这个公开仓库。
旧文章的远程图片地址本次保留，未把无法确认版权或可用性的图片批量替换。

正文从 `##` 开始，页面已经自动显示文章标题。使用标准 Markdown 代码围栏并标注语言。
引用和翻译在开头说明原文标题、作者和链接；区分原文观点与自己的理解。

## 从想法到文章

1. **收集选题**：写到 `planning/BACKLOG.md`，记录“要解决的问题”和一个具体例子。
2. **只开一篇主稿**：创建草稿，先写结论假设和大纲。
3. **补证据**：技术文加入环境版本、可复现步骤、代码和实际结果；阅读文加入自己的判断与实践。
4. **本地预览**：检查手机宽度、代码块、图片、目录、引用与搜索结果。
5. **发布检查**：填写摘要与标签，确认正文完成，修改 `draft: false`，运行 `make check`。
6. **发布与备份**：执行 `deploy.sh`，等待 GitHub Pages 完成，再提交推送文章源码和 `docs` 指针。
7. **回访更新**：发现错误就修正，实质修改更新 `lastmod`，不要改旧链接。

建议先采用每两周一篇完整文章、其间维护一篇旧文的节奏。不需要为凑频率发布占位稿。
未来日期只决定构建时是否包含文章；这个仓库没有定时任务，到时间仍需重新发布。

## 撤回与恢复

把文章改回 `draft: true` 后重新发布，即会从正式产物中移除。新脚本会清理旧生成文件；
重定向目标若已撤回，也不会继续生成指向它的跳转。GitHub/CDN 缓存可能稍后刷新。
草稿源码仍在公开 Git 仓库中，`draft` 不是保密机制。

恢复旧版本：从源码仓库选择需要恢复的文件或提交，确认后重新构建发布。
站点发布记录也保留在 `AkaShark/AkaShark.github.io` 的 Git 历史里。

## 站点维护

- `config.yaml`：网站标题、简介、菜单、社交链接。
- `layouts/`：本项目的 Mana 模板覆盖；不要直接改主题子模块。
- `assets/css/custom.css`：中文排版、首页栏目和移动端细节。
- `i18n/en.toml`：中文界面文案。保留 en 是为了兼容原有 `/en/` 地址。
- `planning/redirects.json`：旧地址到新地址的跳转表。
- `themes/mana`：固定版本的上游主题子模块。升级前先提交现有修改，升级后执行 `make check` 并预览。

本主题的搜索改为全文索引，避免只能搜到正文开头；文章列表按栏目递归收录，
避免多级目录只显示子目录；专题按 `series_order` 排序。主列表使用分页，筛选通过标签与专题入口完成。
