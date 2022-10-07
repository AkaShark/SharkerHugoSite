---
title: "第一个Flutter应用 三"
date: 2022-10-07T23:36:30+08:00 
lastmod: 2022-10-07T23:36:30+08:00
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


## 路由管理

### MaterialPageRoute
```dart
// 路由跳转
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context){
        return const NewRoute();
      })
    );
```
MaterialPageRoute继承自PageRoute类，PageRoute类是一个抽象类，表示占有整个屏幕空间的一个模态路由页面，它还定义了路由构建及切换时过渡动画的相关接口及属性。MaterialPageRoute 是 Material组件库提供的组件，它可以针对不同平台，实现与平台页面切换动画风格一致的路由切换动画

```dart
  MaterialPageRoute({
    WidgetBuilder builder,
    RouteSettings settings,
    bool maintainState = true,
    bool fullscreenDialog = false,
  })
```
MaterialPageRoute构造函数 (可以点进去看注释，注释写的也很清楚)
* builder 是一个WidgetBuilder类型的回调函数，它的作用是构建路由页面的具体内容，返回值是一个widget。我们通常要实现此回调，返回新路由的实例。
* settings 包含路由的配置信息，如路由名称、是否初始路由（首页）。
* maintainState：默认情况下，当入栈一个新路由时，原来的路由仍然会被保存在内存中，如果想在路由没用的时候释放其所占用的所有资源，可以设置maintainState为 false。
* fullscreenDialog表示新的路由页面是否是一个全屏的模态对话框，在 iOS 中，如果fullscreenDialog为true，新页面将会从屏幕底部滑入（而不是水平方向）。

### Navigator
Navigator是一个路由管理的组件，它提供了打开和退出路由页方法。Navigator通过一个栈来管理活动路由集合。通常当前屏幕显示的页面就是栈顶的路由。
常用方法
* Future push(BuildContext context, Route route)
将给定的路由入栈（即打开新的页面），返回值是一个Future对象，用以接收新路由出栈（即关闭）时的
返回数据。
* bool pop(BuildContext context, [ result ])
将栈顶路由出栈，result 为页面关闭时返回给上一个页面的数据。
* 实例方法
Navigator类第一个参数为context的静态方法都对应一个Navigator的实例方法，比如
Navigator.push(BuildContext context, Route route)等价于
Navigator.of(context).push(Route route) ，下面命名路由相关的方法也是一样的。

Navigator 还有很多其他方法，如Navigator.replace、Navigator.popUntil等，详情请参考
API文档或SDK 源码注释，在此不再赘述。

### 路由传值(非命名路由)
```dart
class TipRoute extends StatelessWidget {
  TipRoute({
    Key key,
    required this.text,  // 接收一个text参数
  }) : super(key: key);
  final String text;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("提示"),
      ),
      body: Padding(
        padding: EdgeInsets.all(18),
        child: Center(
          child: Column(
            children: <Widget>[
              Text(text),
              ElevatedButton(
                onPressed: () => Navigator.pop(context, "我是返回值"),
                child: Text("返回"),
              )
            ],
          ),
        ),
      ),
    );
  }
}

class RouterTestRoute extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: ElevatedButton(
        onPressed: () async {
          // 打开`TipRoute`，并等待返回结果
          var result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) {
                return TipRoute(
                  // 路由参数
                  text: "我是提示xxxx",
                );
              },
            ),
          );
          //输出`TipRoute`路由返回结果
          print("路由返回值: $result");
        },
        child: Text("打开提示页"),
      ),
    );
  }
}
```

### 命名路由
所谓命名路由，即有名字的路由，我们可以先给路由起一个名字，然后就可以通过路由名字直接打开新路由了，这为路由管理带来了一种直观、简单的方式。

#### 路由表
`Map<String, WidgetBuilder> routes;`他是一个Map，key为路由的名字，是一个字符串，value是个builder回调函数，用于生成相应的路由widget。

注册路由表
```dart
MaterialApp(
  title: 'Flutter Demo',
  initialRoute:"/", //名为"/"的路由作为应用的home(首页)
  theme: ThemeData(
    primarySwatch: Colors.blue,
  ),
  //注册路由表
  routes:{
   "new_page":(context) => NewRoute(),
   "/":(context) => MyHomePage(title: 'Flutter Demo Home Page'), //注册首页路由
  } 
);
```
跳转要通过路由名称来打开新路由，可以使用Navigator 的pushNamed方法：
`Future pushNamed(BuildContext context, String routeName,{Object arguments})`

#### 传递参数
```dart
class EchoRoute extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    //获取路由参数  
    var args=ModalRoute.of(context).settings.arguments;
    //...省略无关代码
  }
}

Navigator.of(context).pushNamed("new_page", arguments: "hi");
```

对于有构造函数，并且构造函数需要传递参数的Widget我们可以使用下面的方式进行适配
```dart
MaterialApp(
  ... //省略无关代码
  routes: {
   "tip2": (context){
     return TipRoute(text: ModalRoute.of(context)!.settings.arguments);
   },
 }, 
);
```

### 路由生成钩子
MaterialApp有一个onGenerateRoute属性，它在打开命名路由时可能会被调用，之所以说可能，是因为当调用Navigator.pushNamed(...)打开命名路由时，如果指定的路由名在路由表中已注册，则会调用路由表中的builder函数来生成路由组件；如果路由表中没有注册，才会调用onGenerateRoute来生成路由。onGenerateRoute回调签名如下：
`Route<dynamic> Function(RouteSettings settings)`

有了onGenerateRoute回调，要实现上面控制页面权限的功能就非常容易：我们放弃使用路由表，取而代之的是提供一个onGenerateRoute回调，然后在该回调中进行统一的权限控制，如：
```dart
 onGenerateRoute: (settings) {
          return MaterialPageRoute(builder: (context) {
            String? routeName = settings.name;
            switch (routeName) {
              case "/": {
                return MyHomePage(title: "title");
              }
              case "new": {
                return NewRoute(titleStr: "titleStr");
              }
            }
            return Scaffold();
          });
```
其中MaterialPageRoute
```dart
  MaterialPageRoute({
    required this.builder,
    super.settings,
    this.maintainState = true,
    super.fullscreenDialog,
  }) : assert(builder != null),
       assert(maintainState != null),
       assert(fullscreenDialog != null) {
    assert(opaque);
  }
```
传入widgetBuild返回一个Route的子类

## 总结
建议使用命名路由的形式，这将会带来如下好处：
* 语义化更明确。
* 代码更好维护；如果使用匿名路由，则必须在调用Navigator.push的地方创建新路由页，这样不仅需要import新路由页的dart文件，而且这样的代码将会非常分散。
* 可以通过onGenerateRoute做一些全局的路由跳转前置处理逻辑。


## 包管理
```yaml
name: flutter_in_action
description: First Flutter Application.

version: 1.0.0+1

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^0.1.2

dev_dependencies:
  flutter_test:
    sdk: flutter
    
flutter:
  uses-material-design: true
```
* name: 应用或者包名
* description: 应用或包的描述、简介。
* version：应用或包的版本号。
* dependencies：应用或包依赖的其他包或插件。
* dev_dependencies：开发环境依赖的工具包（而不是flutter应用本身依赖的包）。
* flutter：flutter相关的配置选项。

如果我们的Flutter应用本身依赖某个包，我们需要将所依赖的包添加到dependencies下就可以了

### Pub仓库
Pub（https://pub.dev/ ）是 Google 官方的 Dart Packages 仓库，类似于 node 中的 npm仓库、Android中的 jcenter。我们可以在 Pub 上面查找我们需要的包和插件，也可以向 Pub 发布我们的包和插件。我们将在后面的章节中介绍如何向 Pub 发布我们的包和插件。

我们可以使用IDE的功能或者手动运行flutter packages get 命令来下载依赖包。另外，需要注意dependencies和dev_dependencies的区别，前者的依赖包将作为App的源码的一部分参与编译，生成最终的安装包。而后者的依赖包只是作为开发阶段的一些工具包，主要是用于帮助我们提高开发、测试效率，比如 flutter 的自动化测试包等。


#### 本地依赖
如果我们正在本地开发一个包，包名为pkg1，我们可以通过下面方式依赖：
```yaml
dependencies:
	pkg1:
        path: ../../code/pkg1
```

#### git依赖
```yaml
dependencies:
  pkg1:
    git:
      url: git://github.com/xxx/pkg1.git
```

```yaml
dependencies:
  package1:
    git:
      url: git://github.com/flutter/packages.git
      path: packages/package1        
```

问题他们这个不应该也有一个对于包的描述文件么，比如podspec之类的
