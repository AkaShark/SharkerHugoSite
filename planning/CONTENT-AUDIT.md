# 文章整理记录

整理日期：2026-09-30。保留原始正文、发表日期与修改日期，补齐摘要，统一标题、栏目、标签和专题。删除了正文中一个无效的 `[TOC]` 占位标记。

正式文章 18 篇：技术 9 篇、阅读 7 篇、生活 2 篇。草稿 3 篇。

## 地址修复

三篇 Go 语法速通原本生成同一个地址，存在覆盖问题。本次改为 `go-basics-1`、`go-basics-2`、`go-basics-3`；旧地址跳转到第一篇，并通过专题导航串联。其他正式文章保留原地址。更早的不带 `/en/` 的旧地址也建立了跳转。

## 草稿与空白内容

- KVO / KVC：原正文仅为“测试”，改为草稿。
- 《图解 HTTP》读后感：原正文为空，改为草稿。
- `content/docs/NetWork/HTTP发展史浅析.md`：原正文为空，改为草稿；旧链接转向完整的 HTTP 发展史文章。

源码均保留，未用生成内容填充成假文章。旧公开空白页在本次发布中撤下，转向相应栏目或已有完整文章。

## 正式文章

| 栏目 | 标题 | 专题 | 源文件 |
| --- | --- | --- | --- |
| 阅读 | Flutter 实战笔记 06：文本与基础组件 | Flutter 实战笔记 | [第三章基础组件 一.md](../content/posts/read/Flutter实战/第三章基础组件%20一.md) |
| 阅读 | Flutter 实战笔记 05：调试应用 | Flutter 实战笔记 | [第一个Flutter应用 四.md](../content/posts/read/Flutter实战/第一个Flutter应用%20四.md) |
| 阅读 | Flutter 实战笔记 04：路由管理 | Flutter 实战笔记 | [第一个Flutter应用 三.md](../content/posts/read/Flutter实战/第一个Flutter应用%20三.md) |
| 阅读 | Flutter 实战笔记 02：有状态与无状态组件 | Flutter 实战笔记 | [第一个Flutter应用 一.md](../content/posts/read/Flutter实战/第一个Flutter应用%20一.md) |
| 阅读 | Flutter 实战笔记 03：状态管理 | Flutter 实战笔记 | [第一个Flutter应用 二.md](../content/posts/read/Flutter实战/第一个Flutter应用%20二.md) |
| 阅读 | Flutter 实战笔记 01：Dart 与开发起步 | Flutter 实战笔记 | [起步.md](../content/posts/read/Flutter实战/起步.md) |
| 阅读 | 为什么需要虚拟内存？ | — | [为什么要有虚拟内存.md](../content/posts/read/图解系统/为什么要有虚拟内存.md) |
| 生活 | 任务、目标与计划：把想法落实为行动 | — | [任务目标计划.md](../content/posts/life/自我成长/任务目标计划.md) |
| 生活 | 关于汇报与思考方式的感悟 | — | [20221001.md](../content/posts/life/思考/20221001.md) |
| 技术 | HTTP 演进：从 HTTP/0.9 到 HTTP/3（译） | 理解 HTTP | [EP194: Evolution of HTTP[翻译].md](../content/posts/tech/计算机网络/EP194:%20Evolution%20of%20HTTP[翻译].md) |
| 技术 | iOS App 间跳转：URL Scheme 实践 | iOS 开发实践 | [iOSApp间跳转.md](../content/posts/tech/iOS/常见功能/iOSApp间跳转.md) |
| 技术 | WKWebView 的 User-Agent 获取与修改 | iOS 开发实践 | [UserAgent获取与修改.md](../content/posts/tech/iOS/WebView/UserAgent获取与修改.md) |
| 技术 | Go 语法速通（三）：并发与反射 | Go 语法速通 | [基础语法速通③.md](../content/posts/tech/Go/语法/基础语法速通③.md) |
| 技术 | Go 语法速通（二）：函数、接口与结构体 | Go 语法速通 | [基础语法速通②.md](../content/posts/tech/Go/语法/基础语法速通②.md) |
| 技术 | Go 语法速通（一）：基础语法 | Go 语法速通 | [基础语法速通①.md](../content/posts/tech/Go/语法/基础语法速通①.md) |
| 技术 | Xcode 14 新功能笔记（译） | — | [Xcode14新功能.md](../content/posts/tech/翻译/Xcode14新功能.md) |
| 技术 | 设计模式：工厂模式 | — | [工厂模式.md](../content/posts/tech/设计模式/工厂模式.md) |
| 技术 | HTTP 发展史浅析 | 理解 HTTP | [HTTP发展史浅析.md](../content/posts/tech/计算机网络/HTTP发展史浅析.md) |

## 未自动改写的内容

旧技术文章保持当时的版本语境；翻译出处、历史图床图片与代码在新 SDK 下的有效性需要后续逐篇复核，不能把换主题视为技术内容已经重新验证。相关计划见 BACKLOG.md。
