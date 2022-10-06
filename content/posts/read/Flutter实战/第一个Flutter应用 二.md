---
title: "第一个Flutter应用 二"
date: 2022-10-05T21:21:33+08:00 
lastmod: 2022-10-05T21:21:33+08:00
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

## 状态管理
StatefulWidget的状态管理视情况被管理，通常有一下几种方式
* Widget 管理自己的状态
* Widget 管理子widget状态
* 混合管理 (父Widget和子Widget都管理状态)
如何决定使用哪种管理方式
* 如果状态是用户数据，如复选框的选中状态、滑块的位置，则该状态最好由父 Widget 管理。
* 如果状态是有关界面外观效果的，例如颜色、动画，那么状态最好由 Widget 本身来管理。
* 如果某一个状态是不同 Widget 共享的则最好由它们共同的父 Widget 管理。
在 Widget 内部管理状态封装性会好一些，而在父 Widget 中管理会比较灵活。有些时
候，如果不确定到底该怎么管理状态，那么推荐的首选是在父 Widget 中管理（灵活会显
得更重要一些）。

### Widget管理自身状态
_TapboxAState 类:
* 管理TapboxA的状态。
* 定义_active：确定盒子的当前颜色的布尔值。
* 定义_handleTap()函数，该函数在点击该盒子时更新_active，并调用setState()更新UI。
* 实现widget的所有交互式行为

```dart
// TapboxA 管理自身状态.

//------------------------- TapboxA ----------------------------------

class TapboxA extends StatefulWidget {
  TapboxA({Key? key}) : super(key: key);

  @override
  _TapboxAState createState() => _TapboxAState();
}

class _TapboxAState extends State<TapboxA> {
  bool _active = false;

  void _handleTap() {
    setState(() {
      _active = !_active;
    });
  }

  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _handleTap,
      child: Container(
        child: Center(
          child: Text(
            _active ? 'Active' : 'Inactive',
            style: TextStyle(fontSize: 32.0, color: Colors.white),
          ),
        ),
        width: 200.0,
        height: 200.0,
        decoration: BoxDecoration(
          color: _active ? Colors.lightGreen[700] : Colors.grey[600],
        ),
      ),
    );
  }
}
```

### 父Widget管理子Widget的状态
在以下示例中，TapboxB通过回调将其状态导出到其父组件，状态由父组件管理，因此它的父组件为StatefulWidget。但是由于TapboxB不管理任何状态，所以TapboxB为StatelessWidget。
ParentWidgetState 类:
* 为TapboxB 管理_active状态。
* 实现_handleTapboxChanged()，当盒子被点击时调用的方法。
* 当状态改变时，调用setState()更新UI。
TapboxB 类:
* 继承StatelessWidget类，因为所有状态都由其父组件处理。
* 当检测到点击时，它会通知父组件。

```dart
// ParentWidget 为 TapboxB 管理状态.

//------------------------ ParentWidget --------------------------------

class ParentWidget extends StatefulWidget {
  @override
  _ParentWidgetState createState() => _ParentWidgetState();
}

class _ParentWidgetState extends State<ParentWidget> {
  bool _active = false;

  void _handleTapboxChanged(bool newValue) {
    setState(() {
      _active = newValue;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: TapboxB(
        active: _active,
        onChanged: _handleTapboxChanged,
      ),
    );
  }
}

//------------------------- TapboxB ----------------------------------

class TapboxB extends StatelessWidget {
  TapboxB({Key? key, this.active: false, required this.onChanged})
      : super(key: key);

  final bool active;
  final ValueChanged<bool> onChanged;

  void _handleTap() {
    onChanged(!active);
  }

  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _handleTap,
      child: Container(
        child: Center(
          child: Text(
            active ? 'Active' : 'Inactive',
            style: TextStyle(fontSize: 32.0, color: Colors.white),
          ),
        ),
        width: 200.0,
        height: 200.0,
        decoration: BoxDecoration(
          color: active ? Colors.lightGreen[700] : Colors.grey[600],
        ),
      ),
    );
  }
}
```

### 混合状态管理
对于一些组件来说，混合管理的方式会非常有用。在这种情况下，组件自身管理一些内部状态，而父组件管理一些其他外部状态。
在下面 TapboxC 示例中，手指按下时，盒子的周围会出现一个深绿色的边框，抬起时，边框消失。点击完成后，盒子的颜色改变。 TapboxC 将其_active状态导出到其父组件中，但在内部管理其_highlight状态。这个例子有两个状态对象_ParentWidgetState和_TapboxCState。
_ParentWidgetStateC类:
* 管理_active 状态。
* 实现 _handleTapboxChanged() ，当盒子被点击时调用。
* 当点击盒子并且_active状态改变时调用setState()更新UI。

_TapboxCState 对象:
* 管理_highlight 状态。
* GestureDetector监听所有tap事件。当用户点下时，它添加高亮（深绿色边框）；当用户释放时，会移除高亮。
* 当按下、抬起、或者取消点击时更新_highlight状态，调用setState()更新UI。
* 当点击时，将状态的改变传递给父组件。


整体Demo代码如下
```dart
//---------------------------- ParentWidget ----------------------------

class ParentWidgetC extends StatefulWidget {
  @override
  _ParentWidgetCState createState() => _ParentWidgetCState();
}

class _ParentWidgetCState extends State<ParentWidgetC> {
  bool _active = false;

  void _handleTapboxChanged(bool newValue) {
    setState(() {
      _active = newValue;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: TapboxC(
        active: _active,
        onChanged: _handleTapboxChanged,
      ),
    );
  }
}

//----------------------------- TapboxC ------------------------------

class TapboxC extends StatefulWidget {
  TapboxC({Key? key, this.active: false, required this.onChanged})
      : super(key: key);

  final bool active;
  final ValueChanged<bool> onChanged;
  
  @override
  _TapboxCState createState() => _TapboxCState();
}

class _TapboxCState extends State<TapboxC> {
  bool _highlight = false;

  void _handleTapDown(TapDownDetails details) {
    setState(() {
      _highlight = true;
    });
  }

  void _handleTapUp(TapUpDetails details) {
    setState(() {
      _highlight = false;
    });
  }

  void _handleTapCancel() {
    setState(() {
      _highlight = false;
    });
  }

  void _handleTap() {
    widget.onChanged(!widget.active);
  }

  @override
  Widget build(BuildContext context) {
    // 在按下时添加绿色边框，当抬起时，取消高亮  
    return GestureDetector(
      onTapDown: _handleTapDown, // 处理按下事件
      onTapUp: _handleTapUp, // 处理抬起事件
      onTap: _handleTap,
      onTapCancel: _handleTapCancel,
      child: Container(
        child: Center(
          child: Text(
            widget.active ? 'Active' : 'Inactive',
            style: TextStyle(fontSize: 32.0, color: Colors.white),
          ),
        ),
        width: 200.0,
        height: 200.0,
        decoration: BoxDecoration(
          color: widget.active ? Colors.lightGreen[700] : Colors.grey[600],
          border: _highlight
              ? Border.all(
                  color: Colors.teal[700],
                  width: 10.0,
                )
              : null,
        ),
      ),
    );
  }
}
```

### 全局状态管理
* 实现一个全局的事件总线，将语言状态改变对应为一个事件，然后在APP中依赖应用语言的组件的initState 方法中订阅语言改变的事件。当用户在设置页切换语言后，我们发布语言改变事件，而订阅了此事件的组件就会收到通知，收到通知后调用setState(...)方法重新build一下自身即可。
* 使用一些专门用于状态管理的包，如 Provider、Redux，读者可以在 pub 上查看其详细信息。

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  // 对于StatefulWidget自动会执行creatState 但在生命周期的那个时刻呢
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Invoke "debug painting" (press "p" in the console, choose the
          // "Toggle Debug Paint" action from the Flutter Inspector in Android
          // Studio, or the "Toggle Debug Paint" command in Visual Studio Code)
          // to see the wireframe for each widget.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TaboxA(),
            ParentWidget(),
            ParentWidgetC(),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}

class TaboxA extends StatefulWidget {
  const TaboxA({Key? key}) : super(key: key);

  @override
  State<TaboxA> createState() => _TaboxAState();
}

class _TaboxAState extends State<TaboxA> {
  bool _active = false; // Widget自己管理状态
  _handleTap() {
    setState(() {
      _active = !_active;
    });
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _handleTap,
      child: Container(
        width: 200.0,
        height: 200.0,
        decoration: BoxDecoration(
          color: _active ? Colors.lightGreen[700] : Colors.grey[600],
        ),
        child: Center(
          child: Text(
            _active ? "Active" : "Inactive",
            style: const TextStyle(
              fontSize: 32.0,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }
}

// 交给父类管理状态
class ParentWidget extends StatefulWidget {
  const ParentWidget({Key? key}) : super(key: key);

  @override
  State<ParentWidget> createState() => _ParentWidgetState();
}

class _ParentWidgetState extends State<ParentWidget> {
  bool _active = false;
  _handleTapboxChanged(bool newValue) {
    if (newValue == _active) return;
    setState(() {
      _active = newValue;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: TapBoxB(
        active: _active,
        onChanged: _handleTapboxChanged,
      ),
    );
  }
}
class TapBoxB extends StatelessWidget {
  const TapBoxB({Key? key, required this.active, required this.onChanged}) : super(key: key);

  final bool active;
  final ValueChanged<bool> onChanged;

  _handleTap() {
    onChanged(!active);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _handleTap,
      child: Container(
        width: 200.0,
        height: 200.0,
        decoration: BoxDecoration(
          color: active ? Colors.lightGreen[700] : Colors.grey[600],
        ),
        child: Center(
          child: Text(
            active ? "Active" : "Inactive",
            style: const TextStyle(
              fontSize: 32.0,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }
}


// 混合管理模式
class ParentWidgetC extends StatefulWidget {
  @override
  State<ParentWidgetC> createState() => _ParentWidgetCState();
}
// 管理active状态
class _ParentWidgetCState extends State<ParentWidgetC> {
  bool _active = false;
  
  _handleTapboxChanged(bool newValue) {
    if (newValue == _active) return ;
    setState(() {
      _active = newValue;
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Container(
      child: TapBoxC(
        active: _active,
        activeOnChanged: _handleTapboxChanged,
      ),
    );
  }
}

class TapBoxC extends StatefulWidget {
  const TapBoxC({Key? key, required this.active, required this.activeOnChanged}) : super(key: key);
  // 父widget管理的状态
  final bool active;
  final ValueChanged<bool> activeOnChanged;

  @override
  State<TapBoxC> createState() => _TapBoxCState();
}

// 管理highlight状态
class _TapBoxCState extends State<TapBoxC> {
  bool _highlight = false;
  
  void _handleTapDown(TapDownDetails details) {
    setState(() {
      _highlight = true;
    });
  }

  void _handleTapUp(TapUpDetails details) {
    setState(() {
      _highlight = false;
    });
  }

  void _handleTapCancel() {
    setState(() {
      _highlight = false;
    });
  }

  void _handleTap() {
    // 回调active状态
    widget.activeOnChanged(!widget.active);
  }

  @override
  Widget build(BuildContext context) {
    return  GestureDetector(
      onTapDown: _handleTapDown, // 处理按下事件
      onTapUp: _handleTapUp, // 处理抬起事件
      onTap: _handleTap,
      onTapCancel: _handleTapCancel,
      child: Container(
        width: 200.0,
        height: 200.0,
        decoration: BoxDecoration(
          color: widget.active ? Colors.lightGreen[700] : Colors.grey[600],
          border: _highlight ? Border.all(
            color: Colors.teal,
            width: 10.0
          ): null,
        ),
        child: Center(
          child: Text(
            widget.active ? 'Active' : 'Inactive',
            style: const TextStyle(fontSize: 32.0, color: Colors.white),
          ),
        ),
      ),
    );
  }
}
```

