---
title: "Xcode14新功能"
date: 2022-09-28T21:20:22+08:00 
lastmod: 2022-09-28T21:20:22+08:00
author: ["Sharker"] 
categories: 
- 翻译
tags: 
- Xcode
description: ""
weight: 
slug: ""
draft: false 
comments: true 
showToc: true 
TocOpen: true 
hidemeta: false 
disableShare: true 
showbreadcrumbs: true 
---

# What’s New in Xcode 14

[What’s New in Xcode 14](https://medium.com/better-programming/whats-new-in-xcode-14-f6b56c33a8b3)

## Single Size App Icon
在WWDC22, Apple发布了最新的Xcode14，Xcode14中带来了大量的功能和性能的提高，包括了在源码编辑器和其他方面上很多比较Cool的东西，我将和你一起分享下你要知道的。

让我们来一起过下这些主题
## Code Structure When Scrolling
单尺寸App icon对于开发者是一个非常好的功能，你再也不需要App Icon生成工具，你能使用单一的一个1024x1024px的App Icon 资源。
不但如此，这将减少你App的尺寸，你可以尝试下使用1024x1024px的App Icon资源，然后导入到Xcode的Assets中从右边的工具条上选择单尺寸，一旦你导出IPA，你将看出来不同
![](http://media.wjbbf.cn/mweb/16643692829307.jpg)

下面的图是一个app归档后的结果，他展示了选择App icon 单图片和多图片的不同
![](http://media.wjbbf.cn/mweb/16643695060013.jpg)
## Code Structure When Scrolling
我第一次看到这个功能很是吃惊，我想起来了成组的table View的样式，我确信这个是一个有价值的功能，为我们在编辑器滑动的时候展示我们在那个方法。
![](http://media.wjbbf.cn/mweb/16643697173427.jpg)
你当然可以禁止或者开启这个功能在Setting中如下展示
![](http://media.wjbbf.cn/mweb/16643697849218.jpg)
同样的对于标记导航也有修改，你能通过标记导航看到你在代码前写的标记标签。
![](http://media.wjbbf.cn/mweb/16643698812118.jpg)

## Memberwise Initializer Completion
完成成员变量的初始化，在之前版本的Xcode，你需要去右击成员变量初始化
在Xcode 14 提供了高效的方式, 创建成员变量初始化，你只需要写下init，然后你将看到最接近的成员变量初始化的方法
![](http://media.wjbbf.cn/mweb/16643705837020.jpg)
还有更多代码补全的提高，这些补全也更加精确
![](http://media.wjbbf.cn/mweb/16643706443539.jpg)

## Optiuonal Unwrapping
我看到的一大进步是你不需要通过 if let 设置来创建不可变变量来检查可选变量。
![](http://media.wjbbf.cn/mweb/16643709591771.jpg)

## Xcode Build TimeLine
在之前版本的 Xcode 中，我们将构建日志视为一个列表，就像您在左侧看到的以下列表一样。我们还知道正在构建哪个步骤以及需要多少时间。现在，使用 Xcode 14，我们可以将这些日志视为时间线。
![](http://media.wjbbf.cn/mweb/16643709994138.jpg)


## Highlighted Other Features and Improvements in the Release Notes
还有很多高光的其他能力和提高在release文档中被提到
* Simulator now supports remote notifications in iOS 16 when running in macOS 13 on Mac computers with Apple silicon or T2 processors.
* Xcode 14 can now compile targets in parallel with their Swift target dependencies.
* You can now enable sandboxing for shell script build phases using the ENABLE_USER_SCRIPT_SANDBOXING build setting.
* Xcode now provides RECOMMENDED_MACOSX_DEPLOYMENT_TARGET, RECOMMENDED_IPHONEOS_DEPLOYMENT_TARGET, RECOMMENDED_TVOS_DEPLOYMENT_TARGET, RECOMMENDED_WATCHOS_DEPLOYMENT_TARGET, and RECOMMENDED_DRIVERKIT_DEPLOYMENT_TARGET build settings that indicate the recommended minimum deployment versions for each supported Xcode platform.
* Because bitcode is now deprecated, builds for iOS, tvOS, and watchOS no longer include bitcode by default.
* The Thread Performance Checker shows runtime performance issues in the Issue Navigator and the source editor while debugging an app.
* Interface Builder now updates scenes asynchronously.
* Wrapping code with an if statement now automatically reindents the block.



