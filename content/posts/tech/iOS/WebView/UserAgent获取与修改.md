---
title: "UserAgent获取与修改"
date: 2024-02-26T22:40:08+08:00 
lastmod: 2024-02-26T22:40:08+08:00
author: ["Sharker"] 
categories: 
- iOS WebView UA
tags: 
- UA 
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
早从19年 iOS 13上Apple就建议我们将App中使用UIWebView的地方切换为WKWebView了。
>ITMS-90809: Deprecated API Usage - Apple will stop accepting submissions of apps that use UIWebView APIs . See https://developer.apple.com/documentation/uikit/uiwebview for more information.

按照Apple2019年12月13日的[文档](https://developer.apple.com/news/?id=12232019b),20年4月，新应用必须使用WKWebView替代UIWebView，20年12月，应用更新必须使用WKWebView替换UIWebView。具体的时间点可以看下面这张图(有点像是找历史的感觉..)
![CleanShot 2024-03-25 at 22.37.36@2x-2024-03-25-22-41-19](https://sharkerhub.oss-cn-beijing.aliyuncs.com/Obsidian/Blog/CleanShot 2024-03-25 at 22.37.36@2x-2024-03-25-22-41-19.png)


不过好像Apple觉得可能这样太苛责了，或者商店改动的App比较少的原因，后面将这个时间放的宽松了些[文档](https://developer.apple.com/news/?id=edwud51q)，会留给开发者更多的时间，后续具体的截止时间再通知，但是为了更多的时间兼容WKWebView，建议还是更早的替换，我们的App已经将内容展示的部分替换为了WKWebView，但是对于获取UserAgent的部分还使用的UIWebView的API，本篇文章就来讨论下UIWebView的API获取UserAgent切换为WKWebView获取UserAgent的实践。

查找项目是否包含UIWebView的代码
1. 搜索项目代码，找到所有用到UIWebView的地方，替换为WKWebView。
2. 检查SDK是否使用UIWebView，在终端命令行下cd到项目目录，输入下面命令：
`grep -r UIWebView .`
找到所有包含UIWebView的SDK，替换为最新的不包含UIWebView的版本。


## UIWebView获取UA
``` Objective-c
UIWebView *webView = [[UIWebView alloc] initWithFrame:CGRectZero];
NSString *userAgent = [webView stringByEvaluatingJavaScriptFromString:@"navigator.userAgent"];
NSLog(@"userAgent :%@", userAgent);
```

## WKWebView获取UA
``` Objective-C
WKWebView *webView = [[WKWebView alloc] initWithFrame:CGRectZero];
[wkWebView evaluateJavaScript:@"navigator.userAgent" completionHandler:^(id result, NSError *error) {
    NSLog(@"userAgent :%@", result);
}];
```

## 如何修改UA
这种需求太常见了，App内嵌的H5页面有时候需要判断App的版本，App的类型等等信息，这些信息在H5页面初始化的时候作为参数，通过UA来进行获取，于是就有了App修改UA的操作，当然这样的修改大部分是在默认的UA上添加所需要的元素。

> 网上常见的一种最佳实践方式是通过UIWebView获取UA并修改，然后通过WKWebView来进行页面的真实加载，这种的不符合我们说的将UIWebView全部替换的思路，所以这里不展开研究，这是提一下这一种方式确实不错，UIWebView获取UA是同步的，这样获取修改比较方便，同时也不影响WKWebView加载主题内容，但是使用UIWebView的API不知道啥时候就可能被Apple封杀...


### 通过UserDefaults修改
由于WKWebView有一个特性，在初始化时会获取UserDefaults中“UserAgent”这个key的值，这需要我们在真正使用的WKWebView之前要创建一个WKWebView获取他默认的UA
``` Swift
webView = WKWebView();
webView?.evaluateJavaScript("navigator.userAgent", completionHandler: { (obj: Any?, error: Error?) in
   guard let ua = obj as? String else {
        return
    }
    let customUA = "\(ua) Custom User Agent"
    UserDefaults.standard.register(defaults: ["UserAgent": customUA])
    UserDefaults.standard.synchronize()
})
```
> 这种方式在特定版本会有问题 后面会具体说下这个问题

### 通过WKWebView.customUserAgent设置
这种方式其实和第一种方式并没有什么差别，而且还比较复杂，因为只对这一个WebView有效
```Swift 
let fakeWebView = WKWebView();
fakeWebView.evaluateJavaScript("navigator.userAgent", completionHandler: { (obj: Any?, error: Error?) in
    guard let ua = obj as? String else {
        return
    }
    let customUA = "\(ua) Custom User Agent"
    let realWebView = WKWebView()
    realWebView.customUserAgent = customUA
})
```
> 这里获取UA的webView和最终加载内容的WebView并不是同一个后面会说明原因

### 通过applicationNameForUserAgent设置
- config的此属性与上一个属性(webview.customUserAgent)不同，不是将设置的字符串完全变成你所设置的值
- 它将字符串集添加到WebView的默认UserAgent并执行它。
- 这正好就是我们想要的，您所要做的就是设置要添加的字符串。
- 修改后的UserAgent，如：Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Custom UserAgent

``` Swift
let config = WKWebViewConfiguration()
config.applicationNameForUserAgent = "Custom User Agent"
let webview = WKWebView(frame: .zero, configuration: config)
```

以上三种方式系统采用的优先级
```
customUserAgent > UserDefault > applicationNameForUserAgent
```
- 左侧优先级高于右侧
- 如果设置了customUserAgent或UserDefaults方法，则applicationNameForUserAgent将被忽略。
- applicationNameForUserAgent仅添加到了webview具有的默认UserAgent中。(applicationNameForUserAgent被赋得值就是UA自定义的部分)


## Xcode15 iOS 17 遇到的问题

## 注意事项
- 修改UA的步骤一定要在`loadRequest`之前，不然的话可能会导致修改了但是第一次不生效的情况(使用WKWebView是异步的操作，一定要把这部分考虑进去)
- 获取并修改userAgent的webView对象跟加载网页的webView不是同一个对象 不然的话也会出现第一次设置不生效的情况，可以参考这片[文章](https://cloud.tencent.com/developer/article/1158832)
- WKWebView的创建以及执行JS的方法evaluateJavaScript都必须在主线程操作


## Ref
[iOS修改WebView的UserAgent](https://juejin.cn/post/6844904030980800519)

[NSUserDefaults中的registerDefaults](https://www.jianshu.com/p/c630b2b64a10)

[记使用WKWebView修改user-agent在iOS 12踩的一个坑](https://cloud.tencent.com/developer/article/1158832)


