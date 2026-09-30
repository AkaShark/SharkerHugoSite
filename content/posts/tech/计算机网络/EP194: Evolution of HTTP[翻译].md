---
title: "HTTP 演进：从 HTTP/0.9 到 HTTP/3（译）"
date: "2025-12-21T11:40:26+08:00"
lastmod: "2025-12-21T11:40:26+08:00"
url: "/en/posts/tech/计算机网络/ep194-evolution-of-http翻译/"
author: "Sharker"
categories: ["技术"]
tags: ["HTTP", "计算机网络", "翻译"]
description: "回顾 HTTP 各版本的发展，以及性能和传输方式的变化。"
draft: false
series: ["理解 HTTP"]
series_order: 2
---

这篇文章回顾了HTTP协议的发展历程，从HTTP/0.9到HTTP/3，强调了其在性能和实时性方面的改进，同时提到了服务器系统性能指标，如QPS、TPS、并发数和RT，讨论了Nginx的流行原因，还列出了一些重要的网络调试命令，以及集线器、交换机和路由器在网络中的作用。


超文本传输协议(HTTP)历经多年发展，已经从简单的文本传输演变成了为满足现代应用需求的高性能注重实时体验的协议。

## HTTP 演进历程

![Image](https://substackcdn.com/image/fetch/$s_!3GQA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82f1e76a-8fbf-4e8f-b030-e20037c66f70_3000x3900.png "Image")


HTTP 的发展历程如下
1. HTTP/0.9 设置用于通过单个 GET 获取简单的 HTML文档
2. HTTP/1.0 增加了头部信息和状态码以支持更丰富的交互，但每个请求任需要建立新的链接 (每次请求结束后关闭链接，再次请求时创建新链接)
3. HTTP/1.1 引入了持久链接和更多的方法支持，让日常网页浏览变得更快、更高效
4. HTTP/2 通过多路复用技术解决了性能瓶颈，允许对个请求共享一个链接
5. HTTP/3 转向了基于 UDP 的 QUIC 协议，以降低延迟并提高可靠性，尤其是适用于移动和实时应用(移动的网络环境更加复杂)

## 系统性能指标

你的 API 运行缓慢。但究竟慢到什么程度？你需要具体数据。真实的指标能告诉你哪里出了问题，以及该从何处着手修复。

![Image](https://substackcdn.com/image/fetch/$s_!Zyn0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F063ae714-8714-4695-8b0e-16a765c5c1a8_2360x2960.png "Image")

- QPS(Queries Per Second) 每秒请求数，指的是系统每秒处理的请求数量，你的服务器一秒收到 1000 个请求，那服务器的 QPS 就是 1000。
- TPS(Transactions Per Second) 每秒事务数，指的是系统每秒能够处理完成交易的数量，一次交易包含完整的往返流程，即请求发出、访问数据库并返回响应。TPS反应的是实际完成的工作量而不仅仅是接收到的请求数。
- Concurrency 并发数，指的是系统在任一给定时刻同时处理的活跃请求数量，即使每秒有 100 个请求，但是如果每个请求需要 5s 才能完成，那么实际上同时处理的并发请求数高达 500 个。高并发意味着需要更多的资源、更优的连接池管理以及更加智能的线程调度。
- RT 响应时间，指的是从请求开始到收到响应所需要经过的时间，在客户端层面和服务器层面均可测量。

一个简单的公式将他们联系在一起： QPS = 并发数 / 平均响应时间
更高的并发数或者更低的响应时间 = 更高的吞吐量

## Nginx 为什么如此流行

![Image](https://substackcdn.com/image/fetch/$s_!ta7a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe42382d5-9be5-443a-9f75-56ecfa22569c_2360x2960.png "Image")

Nginx受欢迎原因如下:

- 高性能服务器
- 反向代理与负载均衡器
- 缓存层
- SSL 终端卸载


## 应该掌握的网络调试命令

![Image](https://substackcdn.com/image/fetch/$s_!sXIK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa25e1401-cc6f-49f1-9ed1-6f093a01ac6c_2360x2664.png "Image")

> 帮助故障定位

- ping：检查目标是否响应，并报告往返时间以确认基本可达性。
- traceroute / tracert：显示路径上的每一跳，以便您查看数据包在何处变慢或停止。
- mtr / pathping：持续测量每一跳的延迟和丢包，以发现间歇性问题。
- ip addr, ip link / ipconfig /all：打印本地 IP 地址、MAC 地址和接口状态，以便您验证机器的网络身份。 
- ip route：显示路由表，以确认系统将使用哪个网关和下一跳。
- ip neigh：显示 IP 到 MAC 的条目，以检测局域网中的重复或过时 ARP 记录。
- ss -tulpn：列出监听套接字和进程 ID，以便确认服务是否确实绑定到预期端口。
- dig：解析 DNS 记录以验证客户端将连接的确切 IP 地址。
- curl -I：仅获取 HTTP(S)头信息，以检查状态码、重定向和缓存设置。
- tcpdump / tshark：捕获数据包，以便您能检查真实流量，并验证发送与接收的内容。
- iperf3：测量两台主机之间的端到端吞吐量，以区分带宽限制与应用问题。
- ssh：在远程机器上打开一个安全外壳，以便直接运行检查并应用修复。
- sftp：安全地传输文件，以便在事件期间拉取日志或推送工件。
- nmap：扫描开放端口并探测版本，以确认哪些服务已暴露并正在响应。


> 上述命令有些 Mac 需要单独安装 brew 包


## 集线器、交换机与路由

每个家庭或者办公网络都离不开这三种设备，集线器、交换机和路由器，但它们的角色常常被混淆。

![Image](https://substackcdn.com/image/fetch/$s_!BXWB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09a8b52f-2b80-4762-92cd-c5d18d5a7a3c_2360x2960.png "Image")

- 集线器工作在物理层（第一层）。它是三者中最简单的设备，无法识别地址或数据类型。当数据包到达时，它只是简单地将其广播给所有连接的设备，形成一个大的冲突域。这意味着所有设备会竞争相同的带宽，使得集线器在现代网络中效率低下。
- 交换机工作在第二层（数据链路层）。它能够知道MAC 地址，并将数据帧仅转发至正确的目标设备。交换机的每个端口都构成独立的冲突域，从而提升效率并加速局域网内的通信。
- 路由器工作在网络层（第三层）。它根据 IP 地址路由数据包，并将不同网络连接在一起，例如将家庭网络连接到互联网。每个路由器接口构成一个独立的广播域，从而隔离本地流量和外部流量。