---
title: "第一个Flutter应用 一"
date: 2022-10-05T21:21:51+08:00 
lastmod: 2022-10-05T21:21:51+08:00
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

## 有状态与无状态组件
* Stateful widget 可以拥有状态，这些状态在 widget 生命周期中是可以变的，而 Stateless widget 是不可变的。
* Stateful widget 至少由两个类组成：
    * 一个StatefulWidget类。
    * 一个 State类； StatefulWidget类本身是不变的，但是State类中持有的状态在 widget 生命周期中可能会发生变化。

## Widget 接口
Widget定义
```dart
@immutable // 不可变的
abstract class Widget extends DiagnosticableTree {
  const Widget({ this.key });

  final Key? key;

  @protected
  @factory
  Element createElement();

  @override
  String toStringShort() {
    final String type = objectRuntimeType(this, 'Widget');
    return key == null ? type : '$type-$key';
  }

  @override
  void debugFillProperties(DiagnosticPropertiesBuilder properties) {
    super.debugFillProperties(properties);
    properties.defaultDiagnosticsTreeStyle = DiagnosticsTreeStyle.dense;
  }

  @override
  @nonVirtual
  bool operator ==(Object other) => super == other;

  @override
  @nonVirtual
  int get hashCode => super.hashCode;

  static bool canUpdate(Widget oldWidget, Widget newWidget) {
    return oldWidget.runtimeType == newWidget.runtimeType
        && oldWidget.key == newWidget.key;
  }
  ...
}
```
* @immutable 代表 Widget 是不可变的，这会限制 Widget 中定义的属性（即配置信息）必须是不可变的（final），为什么不允许 Widget 中定义的属性变化呢？这是因为，Flutter 中如果属性发生变化则会重新构建Widget树，即重新创建新的 Widget 实例来替换旧的 Widget 实例，所以允许 Widget 的属性变化是没有意义的，因为一旦 Widget 自己的属性变了自己就会被替换。这也是为什么 Widget 中定义的属性必须是 final 的原因。
* widget类继承自DiagnosticableTree，DiagnosticableTree即“诊断树”，主要作用是提供调试信息。
* Key: 这个key属性类似于 React/Vue 中的key，主要的作用是决定是否在下一次build时复用旧的 widget ，决定的条件在canUpdate()方法中。
* createElement()：正如前文所述“一个 widget 可以对应多个Element”；Flutter 框架在构建UI树时，会先调用此方法生成对应节点的Element对象。此方法是 Flutter 框架隐式调用的，在我们开发过程中基本不会调用到。
* debugFillProperties(...) 复写父类的方法，主要是设置诊断树的一些特性。
* canUpdate(...)是一个静态方法，它主要用于在 widget 树重新build时复用旧的 widget ，其实具体来说，应该是：是否用新的 widget 对象去更新旧UI树上所对应的Element对象的配置；通过其源码我们可以看到，只要newWidget与oldWidget的runtimeType和key同时相等时就会用new widget去更新Element对象的配置，否则就会创建新的Element。

## Flutter 中的四棵树
Flutter渲染流程
* 根据 Widget 树生成一个 Element 树，Element 树中的节点都继承自 Element 类。
* 根据 Element 树生成 Render 树（渲染树），渲染树中的节点都继承自RenderObject 类。
* 根据渲染树生成 Layer 树，然后上屏显示，Layer 树中的节点都继承自 Layer 类。

负责渲染和布局的是Render Tree
```dart
Container( // 一个容器 widget
  color: Colors.blue, // 设置容器背景色
  child: Row( // 可以将子widget沿水平方向排列
    children: [
      Image.network('https://www.example.com/1.png'), // 显示图片的 widget
      const Text('A'),
    ],
  ),
);
```
对于上面的代码会变成如下三棵树，其中对于容器设置back会变成cloredBox
![](http://media.wjbbf.cn/mweb/16649627634852.jpg)
* 三棵树中，Widget 和 Element 是一一对应的，但并不和 RenderObject 一一对应。比如 StatelessWidget 和 StatefulWidget 都没有对应的 RenderObject。

## StatelessWidget
### Context
statelessWidget是不需要记录状态的Widget，主要是方法是在build中构建UI配置，build方法有一个context参数，它是BuildContext类的一个实例，表示当前 widget 在 widget 树中的上下文，每一个 widget 都会对应一个 context 对象（因为每一个 widget 都是 widget 树上的一个节点）。实际上，context是当前 widget 在 widget 树中位置中执行”相关操作“的一个**句柄(handle)**，比如它提供了从当前 widget 开始向上遍历 widget 树以及按照 widget 类型查找父级 widget 的方法。下面是在子树中获取父级 widget 的一个示例：
```dart
class ContextRoute extends StatelessWidget  {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Context测试"),
      ),
      body: Container(
        child: Builder(builder: (context) {
          // 在 widget 树中向上查找最近的父级`Scaffold`  widget 
          Scaffold scaffold = context.findAncestorWidgetOfExactType<Scaffold>();
          // 直接返回 AppBar的title， 此处实际上是Text("Context测试")
          return (scaffold.appBar as AppBar).title;
        }),
      ),
    );
  }
}
```

## StatefulWidget
createState() 用于创建和 StatefulWidget 相关的状态，它在StatefulWidget 的生命周期中可能会被**多次调用**。例如，当一个 StatefulWidget 同时插入到 widget 树的多个位置时，Flutter 框架就会调用该方法为每一个位置生成一个独立的State实例，其实，**本质上就是一个StatefulElement对应一个State实例**。

## State
一个StatefulWidget类会对应一个State类，State表示与其对应的StatefulWidget要维护的状态，State中的保存的状态信息可以:
* 在widget构建时被同步读取
* 在widget生命周期中可以被改变，当State被改变时，可以手动调用其setState()方法通知Flutter框架状态发生改变，Flutter框架收到状态改变的消息后，会重新调用其build方法构建widget树，从而更新UI

State 中有两个常用的属性:
* widget，它表示与该 State 实例关联的 widget 实例，由Flutter 框架动态设置。注意，这种关联并非永久的，因为在应用生命周期中，UI树上的某一个节点的 widget 实例在重新构建时可能会变化，但State实例只会在第一次插入到树中时被创建，当在重新构建时，如果 widget 被修改了，Flutter 框架会动态设置State. widget 为新的 widget 实例。
* context。StatefulWidget对应的 BuildContext，作用同StatelessWidget 的BuildContext。

### State 生命周期
* initState: 
当 widget 第一次插入到 widget 树时会被调用，对于每一个State对象，Flutter 框
架只会调用一次该回调，所以，通常在该回调中做一些一次性的操作，如状态初始化、订阅
子树的事件通知等。不能在该回调中调用
BuildContext.dependOnInheritedWidgetOfExactType（该方法用于在 widget 
树上获取离当前 widget 最近的一个父级InheritedWidget，关于InheritedWidget
我们将在后面章节介绍），原因是在初始化完成后， widget 树中的InheritFrom 
widget也可能会发生变化，所以正确的做法应该在在build（）方法或
didChangeDependencies()中调用它。
* didChangeDependencies:
当State对象的依赖发生变化时会被调用；例如：在之前build() 中包含了一个
InheritedWidget （第七章介绍），然后在之后的build() 中Inherited widget发
生了变化，那么此时InheritedWidget的子 widget 的didChangeDependencies()
回调都会被调用。典型的场景是当系统语言 Locale 或应用主题改变时，Flutter 框架
会通知 widget 调用此回调。需要注意，组件第一次被创建后挂载的时候（包括重创建）
对应的didChangeDependencies也会被调用。
* build:
此回调读者现在应该已经相当熟悉了，它主要是用于构建 widget 子树的，会在如下场景
被调用：
    * 在调用initState()之后
    * 在调用didUpdateWidget()之后
    * 在调用setState()之后
    * 在调用didChangeDependencies()之后
    * 在State对象从树中一个位置移除后(会调用deactivate)又重新插入到树的其他位置
* reassemble: 此回调是专门为了开发调试而提供的，在热重载(hot reload)时会被调用，此回调在Release模式下永远不会被调用。
* didUpdateWidget:
在 widget 重新构建时，Flutter 框架会调用widget.canUpdate来检测 widget 树
中同一位置的新旧节点，然后决定是否需要更新，如果widget.canUpdate返回true则会
调用此回调。正如之前所述，widget.canUpdate会在新旧 widget 的 key 和 
runtimeType 同时相等时会返回true，也就是说在在新旧 widget 的key和
runtimeType同时相等时didUpdateWidget()就会被调用。
* deactivate:
当 State 对象从树中被移除时，会调用此回调。在一些场景下，Flutter 框架会将 
State 对象重新插到树中，如包含此 State 对象的子树在树的一个位置移动到另一个位
置时（可以通过GlobalKey 来实现）。如果移除后没有重新插入到树中则紧接着会调用
dispose()方法。 
* dispose:
当 State 对象从树中被永久移除时调用；通常在此回调中释放资源。

![](http://media.wjbbf.cn/mweb/16649689076582.jpg)

ps:
在继承StatefulWidget重写其方法时，对于包含`@mustCallSuper`标注的父类方法，都要在子类方法中**调用父类方法**。

### 在Widget树中获取State对象
* context获取
context对象有一个findAncestorStateOfType()方法，该方法可以从当前节点沿着 
widget 树向上查找指定类型的 StatefulWidget 对应的 State 对象。下面是实现打
开 SnackBar 的示例：
```dart
class GetStateObjectRoute extends StatefulWidget {
  const GetStateObjectRoute({Key? key}) : super(key: key);

  @override
  State<GetStateObjectRoute> createState() => _GetStateObjectRouteState();
}

class _GetStateObjectRouteState extends State<GetStateObjectRoute> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("子树中获取State对象"),
      ),
      body: Center(
        child: Column(
          children: [
            Builder(builder: (context) {
              return ElevatedButton(
                onPressed: () {
                  // 查找父级最近的Scaffold对应的ScaffoldState对象
                  ScaffoldState _state = context.findAncestorStateOfType<ScaffoldState>()!;
                  // 打开抽屉菜单
                  _state.openDrawer();
                },
                child: Text('打开抽屉菜单1'),
              );
            }),
          ],
        ),
      ),
      drawer: Drawer(),
    );
  }
}
```
* 在 Flutter 开发中便有了一个默认的约定：如果 StatefulWidget 的状态是希望暴露出的，应当在 StatefulWidget 中提供一个of 静态方法来获取其 State 对象，开发者便可直接通过该方法来获取
```dart
Builder(builder: (context) {
  return ElevatedButton(
    onPressed: () {
      // 直接通过of静态方法来获取ScaffoldState
      ScaffoldState _state=Scaffold.of(context);
      // 打开抽屉菜单
      _state.openDrawer();
    },
    child: Text('打开抽屉菜单2'),
  );
}),
```
* 通过GolbalKey
GlobalKey 是 Flutter 提供的一种在整个 App 中引用 element 的机制。如果一个 
widget 设置了GlobalKey，那么我们便可以通过globalKey.currentWidget获得该 
widget 对象、globalKey.currentElement来获得 widget 对应的element对象，
如果当前 widget 是StatefulWidget，则可以通过globalKey.currentState来获得
该 widget 对应的state对象。
ps: 使用 GlobalKey 开销较大，如果有其他可选方案，应尽量避免使用它。另外，同一
个 GlobalKey 在整个 widget 树中必须是唯一的，不能重复。

## 使用RenderObject定义Widget
```dart
class CustomWidget extends LeafRenderObjectWidget{
  @override
  RenderObject createRenderObject(BuildContext context) {
    // 创建 RenderObject
    return RenderCustomObject();
  }
  @override
  void updateRenderObject(BuildContext context, RenderCustomObject  renderObject) {
    // 更新 RenderObject
    super.updateRenderObject(context, renderObject);
  }
}

class RenderCustomObject extends RenderBox{

  @override
  void performLayout() {
    // 实现布局逻辑
  }

  @override
  void paint(PaintingContext context, Offset offset) {
    // 实现绘制
  }
}
```
## 常见组件
* Text (opens new window)：该组件可让您创建一个带格式的文本。
* Row (opens new window)、 Column (opens new window)： 这些具有弹性空间的布局类 widget 可让您在水平（Row）和垂直（Column）方向上创建灵活的布局。其设计是基于 Web 开发中的 Flexbox 布局模型。
* Stack (opens new window)： 取代线性布局 (译者语：和 Android 中的FrameLayout相似)，[Stack](https://docs.flutter.dev/flutter/ widgets/Stack-class.html)允许子 widget 堆叠， 你可以使用 Positioned (opens new window)来定位他们相对于Stack的上下左右四条边的位置。Stacks是基于Web开发中的绝对定位（absolute positioning )布局模型设计的。
* Container (opens new window)： Container (opens new window)可让您创建矩形视觉元素。Container 可以装饰一个BoxDecoration (opens new window), 如 background、一个边框、或者一个阴影。 Container (opens new window)也可以具有边距（margins）、填充(padding)和应用于其大小的约束(constraints)。另外， Container (opens new window)可以使用矩阵在三维空间中对其进行变换。

### Material组件

### Cupertino组件

在Widget之上的两个库，是Flutter提供的两种风格的组件库


