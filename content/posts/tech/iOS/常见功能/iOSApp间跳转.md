---
title: "iOS App间跳转"
date: 2024-03-27T20:41:10+08:00 
lastmod: 2024-03-27T20:41:10+08:00
author: ["Sharker"] 
categories: 
- iOS
tags: 
- iOS Scheme 应用间跳转
description: ""
weight: 
slug: ""
draft: false 
comments: true 
showToc: true 
TocOpen: true 
hidemeta: false 
showbreadcrumbs: true 
---

## 背景
在App的开发过程中经常会遇到与其他App联动相互拉起的需求(也就是拉起其他App或者被其他App拉起)，那么在iOS中这种拉起操作应该如何实现呢，本文将主要介绍以下几个方面
- 如何实现App拉起
- 如何实现App之间的相互拉起

## 背景知识
这里提前补充需要了解的知识点，下面是url的基本格式
`protocol://hostname[:port]/path/[;parameters][?query]#fragment`
- protocol, 协议名称也叫做scheme，例如http、https当然这个地方也可以自定义
- hostname：域名或ip地址，例如 www.baidu.com 就是域名；110.242.68.3就是IP地址。
- port：端口号，例如 www.baidu.com:80后面的80就是端口号，80是默认端口号，一般不显示。
- path：路径，表示主机上的目录或文件路径。例如：fanyi.baidu.com/translate。
- query：可选项，用于传递参数，由?符号开始，&符号隔开，参数名和值用=符号相连。例如：www.baidu.com/s?ie=utf-8&…
在使用App拉起的过程中需要使用到url的基本格式定义，在拉起的过程中定义的url格式如下
`customAppScheme://xxxxx/path?params=xxx`

## App拉起
在iOS的系统中从A App打开B App，需要A App去找到B App，这就和我们邮寄信件一样我们需要写一个我们信件的目标地址，在系统中我们可以通过`UIApplication`中的API来完成这件事

``` Objective-c
/**
 通过应用程序打开一个资源路径
@param url 资源路径的地址
@return 返回成功失败的信息
 */
- (BOOL)openURL:(NSURL*)url;
```
`openURL:`通过url来标识我们要跳转的App的位置，一个简单的例子

``` Objective-c
// 跳转到打电话
NSURL *url = [NSURL URLWithString:@"tel://10086"];
[[UIApplication sharedApplication] openURL:url];

//发送系统短信
NSURL *url = [NSURL URLWithString:@"sms://1383838438"];
[[UIApplication sharedApplication] openURL:url];
```
从上面的例子可以产出来拉起其他App核心关键点在url，以上面的打电话为例url的定义为`tel://10086`结合上面的url格式定义，Scheme为tel，host为10086，可以才到10086就是要打的电话，那`tel`自然就是标识这打电话App，`tel`这个Scheme在系统的认知中就是标识着电话App，同样的如果我想要打开其他App只需要知道他的Scheme自然就可以打开该App。

## App之间相互拉起
### 注册URL Scheme
根据上面的App拉起可以得出只要知道了App的scheme就可以拉起这个App，那么如果我们有两个App A和B，现在要求我用A App打开B App，自然解决方法就是在A中open B的scheme就可以了，可是B的scheme是什么呢，这就需要我们自己来定义啦。

![CleanShot 2024-04-14 at 18.36.05@2x-2024-04-14-18-36-19](https://sharkerhub.oss-cn-beijing.aliyuncs.com/Obsidian/Blog/CleanShot%202024-04-14%20at%2018.36.05%402x-2024-04-14-18-36-19.png)

在Xcode的工程配置中点击info条目，在info下找到URL Types点击添加

![CleanShot 2024-04-14 at 18.38.08@2x-2024-04-14-18-38-17](https://sharkerhub.oss-cn-beijing.aliyuncs.com/Obsidian/Blog/CleanShot%202024-04-14%20at%2018.38.08%402x-2024-04-14-18-38-17.png)

填写其中identifier和URL Schemes
- identifier: URL Identifier是自定义的 URL scheme 的名字，一般采用反转域名的方法保证该名字的唯一性
- URL Schemes: 为自己的app定义的schemes。使用另外的app调起自己的app时，使用这个参数
identifier是可选的，定义identifier后会变成url的host，scheme会变成url的protocol，
这么看来定义的时候identifier变成了打开url的host，scheme变成了协议，也就是说url的格式为
`URL Scheme://URL identifier`

> scheme 定义需要注意
> url scheme必须能唯一标识一个App，如果你设置的scheme和其他的scheme相同，那么默认的表现是未知的
> URL Scheme的命名应该是只能纯英文字符，而不能含有下划线或者数字
> 一个App可以同时拥有多个scheme

通过上面的方式就定义好了Scheme啦，假设我们定义A App的scheme为`customA` B App的scheme为`customB` 当然实际上scheme对应的url protocol为`customA://`和`customB://`

### 处理拉起请求
已经定义好了A和B的scheme，继续完成上面的需求，用A打开B，在A的任意位置我们调用
``` Objective-C
NSURL *url = [NSURL URLWithString:@"customB://idetifierB"];
[[UIApplication sharedApplication] openURL:url];
```
可以成功拉起B App那么如何将一些参数传递到B呢，如果使用的url为`customB://idetifierB?params1=xx&params2=yy`，B App如何获取到这参数。

上面其实有提到过处理应用之间的跳转是通过`UIApplication`来完成的，所以可以在B App中通过重写`- (BOOL)application:(UIApplication *)app openURL:(NSURL *)url options:(NSDictionary<UIApplicationOpenURLOptionsKey,id> *)options`来获取到对应的请求来完成相应逻辑的处理。

![CleanShot 2024-04-14 at 19.14.43@2x-2024-04-14-19-15-08](https://sharkerhub.oss-cn-beijing.aliyuncs.com/Obsidian/Blog/CleanShot%202024-04-14%20at%2019.14.43%402x-2024-04-14-19-15-08.png)

## 补充
### 注册URL Scheme 方式2
注册URL Scheme的方式还有一种，在Info.plist中间中右击添加`URL types`类型为`Array`,\
![CleanShot 2024-04-14 at 20.44.49@2x-2024-04-14-20-45-05](https://sharkerhub.oss-cn-beijing.aliyuncs.com/Obsidian/Blog/CleanShot%202024-04-14%20at%2020.44.49%402x-2024-04-14-20-45-05.png)
添加的每个item的内容，这和上面介绍的注册URL Scheme的方式类似。

### `[[UIApplication sharedApplication] canOpenURL:url` 使用
在调用`[[UIApplication sharedApplication] openURL:url]`前可以去判断下是否可以打开该应用`[[UIApplication sharedApplication] canOpenURL:url`，但是在iOS9后判断`canOpenURL`需要再info.plist文件中将目标Url定义进白名单，否则不能使用。
在Info.plist文件中添加`LSApplicationQueriesSchemes`字段，该字段对应的是数组类型，然后添加CustomA(要跳转的目标Scheme)

![CleanShot 2024-04-14 at 20.54.37@2x-2024-04-14-20-54-42](https://sharkerhub.oss-cn-beijing.aliyuncs.com/Obsidian/Blog/CleanShot%202024-04-14%20at%2020.54.37%402x-2024-04-14-20-54-42.png)

> `LSApplicationQueriesSchemes`对应的Array至多只能添加50个item，应该是Apple为了安全考虑不允许去扫描用户已经安装的App(可以跳转的前提是已经安装App且将scheme注册进系统)

#### 对于`LSApplicationQueriesSchemes`白名单的理解
Apple文档的介绍如下
![](https://img-blog.csdnimg.cn/img_convert/7c0a6918c6eaf5f008738681ab91373c.png)
说的是，在iOS9后，如果想要使用`canOpenURL`方法检查是否可以打这个URL或可以处理该URL的App，需要在info.plist里添加LSApplicationQueriesSchemes字段来预设url，否则是否安装都会返回NO。

“白名单”的意义是要检查当前设备上是否安装了其他App，而不是打开其他App必须添加“白名单”，所以如果想要打开其他App，直接使用openURL即可。

==`canOpenURL：`方法有限制，`openURL:`方法是没有限制的。==

![CleanShot 2024-04-14 at 21.22.21@2x-2024-04-14-21-23-36](https://sharkerhub.oss-cn-beijing.aliyuncs.com/Obsidian/Blog/CleanShot%202024-04-14%20at%2021.22.21%402x-2024-04-14-21-23-36.png)

#### 如何回跳
上面已经知道了如何跳转到另一个App中，完成了最开始说的从A App跳转到B App的需求，但是如果要求跳转到B App后完成调回App的操作呢，根据上面的介绍其实这个需求也很简单，B App条回A App重点是拿到A App的scheme即可，可以将A App的scheme在第一次跳转到B App的时候作为参数传递给B App这样在B App完成逻辑处理后就可以使用该Scheme完成回跳。

具体来说就是
A->B->A
- 首先要从B中的info.plist设置A注册的Scheme白名单
- 然后从A->B的时候通过参数将A的scheme带过去
- B处理完对应的业务后通过同样的方式返回A

其实在微信SDK中我们也是这样做的，在跳转到微信的url中添加一个backurl然后传递自己的App Scheme 微信执行完成后会拉起自己的App。

## Ref
- [iOS scheme跳转机制](https://jianshu.com/p/138b44833cda)
- [关于iOS“白名单”的理解](https://blog.csdn.net/u013712343/article/details/119244506)