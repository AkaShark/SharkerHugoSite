---
title: "第一个Flutter应用 四"
date: 2022-10-09T10:35:30+08:00 
lastmod: 2022-10-09T10:35:30+08:00
author: ["Sharker"] 
categories: 
- Flutter
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

[第二章](https://book.flutterchina.club/chapter2/first_flutter_app.html#_2-1-1-%E5%88%9B%E5%BB%BAflutter%E5%BA%94%E7%94%A8%E6%A8%A1%E6%9D%BF)

## 调试Flutter应用
### 日志与断点
#### debugger() 声明
```dart
void someFunction(double offset) {
  debugger(when: offset > 30.0);
  // ...
}
```

#### print、debugPrint、flutter logs
Dart print()功能将输出到系统控制台，我们可以使用flutter logs来查看它（基本上是一个包装adb logcat）。

如果你一次输出太多，那么Android有时会丢弃一些日志行。为了避免这种情况，我们可以使用Flutter的foundation库中的debugPrint() (opens new window)。 这是一个封装print，它将输出限制在一个级别，避免被Android内核丢弃。

Flutter框架中的许多类都有toString实现。按照惯例，这些输出通常包括对象的runtimeType单行输出，通常在表单中ClassName(more information about this instance…)。 树中使用的一些类也具有toStringDeep，从该点返回整个子树的多行描述。已一些具有详细信息toString的类会实现一个toStringShort，它只返回对象的类型或其他非常简短的（一个或两个单词）描述。

#### 调试模式断言
在Flutter应用调试过程中，Dart assert语句被启用，并且 Flutter 框架使用它来执行许多运行时检查来验证是否违反一些不可变的规则。当一个某个规则被违反时，就会在控制台打印错误日志，并带上一些上下文信息来帮助追踪问题的根源。

要关闭调试模式并使用发布模式，请使用flutter run --release运行我们的应用程序。 这也关闭了Observatory调试器。一个中间模式可以关闭除Observatory之外所有调试辅助工具的，称为“profile mode”，用--profile替代--release即可。

#### 断点
Vscode 或者 AS上自带的

### 调试应用程序层
widget树 渲染树 Layer树
文档写的太少了而且没有实操，这个地方再找找资料补充下
官网上有对于DevTools的相关教程
[教程](https://docs.flutter.dev/development/tools/devtools/overview)

## 异常捕获
### Dart单线程模型
![](http://media.wjbbf.cn/mweb/16652812113231.jpg)
Dart线程运行过程，如上图中所示，入口函数 main() 执行完后，消息循环机制便启动了。首先会按照先进先出的顺序逐个执行微任务队列中的任务，事件任务执行完毕后程序便会退出，但是，在事件任务执行的过程中也可以插入新的微任务和事件任务，在这种情况下，整个线程的执行过程便是一直在循环，不会退出，而Flutter中，主线程的执行过程正是如此，永不终止。
在Dart中，所有的外部事件任务都在事件队列中，如IO、计时器、点击、以及绘制事件等，而微任务通常来源于Dart内部，并且微任务非常少，之所以如此，是因为微任务队列优先级高，如果微任务太多，执行时间总和就越久，事件队列任务的延迟也就越久，对于GUI应用来说最直观的表现就是比较卡，所以必须得保证微任务队列不会太长。值得注意的是，我们可以通过Future.microtask(…)方法向微任务队列插入一个任务。
在事件循环中，当某个任务发生异常并没有被捕获时，程序并不会退出，而直接导致的结果是当前任务的后续代码就不会被执行了，也就是说一个任务中的异常是不会影响其他任务执行的。

### Flutter框架异常捕获
onError是FlutterError的一个静态属性，它有一个默认的处理方法 dumpErrorToConsole，到这里就清晰了，如果我们想自己上报异常，只需要提供一个自定义的错误处理回调即可，如：
```dart
void main() {
  FlutterError.onError = (FlutterErrorDetails details) {
    reportError(details);
  };
 ...
}
```
这样我们就可以处理那些Flutter为我们捕获的异常了

### 其他异常捕获与日志收集
在Flutter中，还有一些Flutter没有为我们捕获的异常，如调用空对象方法异常、Future中的异常。在Dart中，异常分两类：同步异常和异步异常，同步异常可以通过try/catch捕获，而异步异常则比较麻烦，如下面的代码是捕获不了Future的异常的：
```dart
try{
    Future.delayed(Duration(seconds: 1)).then((e) => Future.error("xxx"));
}catch (e){
    print(e)
}
```

Dart中有一个runZoned(...) 方法，可以给执行对象指定一个Zone。Zone表示一个代码执行的环境范围，为了方便理解，读者可以将Zone类比为一个代码执行沙箱，不同沙箱的之间是隔离的，沙箱可以捕获、拦截或修改一些代码行为，如Zone中可以捕获日志输出、Timer创建、微任务调度的行为，同时Zone也可以捕获所有未处理的异常。下面我们看看runZoned(...)方法定义：
```dart
R runZoned<R>(R body(), {
    Map zoneValues, 
    ZoneSpecification zoneSpecification,
}) 
```
* zoneValues: Zone 的私有数据，可以通过实例zone[key]获取，可以理解为每个“沙箱”的私有数据。
* zoneSpecification：Zone的一些配置，可以自定义一些代码行为，比如拦截日志输出和错误等，举个例子：
```dart
runZoned(
  () => runApp(MyApp()),
  zoneSpecification: ZoneSpecification(
    // 拦截print 蜀西湖
    print: (Zone self, ZoneDelegate parent, Zone zone, String line) {
      parent.print(zone, "Interceptor: $line");
    },
    // 拦截未处理的异步错误
    handleUncaughtError: (Zone self, ZoneDelegate parent, Zone zone,
                          Object error, StackTrace stackTrace) {
      parent.print(zone, '${error.toString()} $stackTrace');
    },
  ),
);
```
这样一来，我们 APP 中所有调用print方法输出日志的行为都会被拦截，通过这种方式，我们也可以在应用中记录日志，等到应用触发未捕获的异常时，将异常信息和日志统一上报。
另外我们还拦截了未被捕获的异步错误，这样一来，结合上面的 FlutterError.onError 我们就可以捕获我们Flutter应用错误了并进行上报了！如下

```dart
void collectLog(String line){
    ... //收集日志
}
void reportErrorAndLog(FlutterErrorDetails details){
    ... //上报错误和日志逻辑
}

FlutterErrorDetails makeDetails(Object obj, StackTrace stack){
    ...// 构建错误信息
}

void main() {
// 已经捕获的异常
  var onError = FlutterError.onError; //先将 onerror 保存起来
  FlutterError.onError = (FlutterErrorDetails details) {
    onError?.call(details); //调用默认的onError
    reportErrorAndLog(details); //上报
  };
  runZoned(
  () => runApp(MyApp()),
  zoneSpecification: ZoneSpecification(
    // 拦截print
    print: (Zone self, ZoneDelegate parent, Zone zone, String line) {
      collectLog(line);
      parent.print(zone, "Interceptor: $line");
    },
    // 拦截未处理的异步错误
    handleUncaughtError: (Zone self, ZoneDelegate parent, Zone zone,
                          Object error, StackTrace stackTrace) {
      reportErrorAndLog(details);
      parent.print(zone, '${error.toString()} $stackTrace');
    },
  ),
 );
}
```