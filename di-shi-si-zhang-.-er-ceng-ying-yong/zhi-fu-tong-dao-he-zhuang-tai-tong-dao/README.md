# 支付通道和状态通道

支付通道是一种在比特币区块链之外交换比特币交易的无信任机制。这些交易，如果在比特币区块链上结算，是有效的，但实际上它们被保留在链外，等待最终的批量结算。由于这些交易没有被结算，它们可以进行交换而不受通常的结算延迟的影响，从而实现了极高的交易吞吐量、低延迟和细粒度的交易。

实际上，“通道”这个术语是一个隐喻。状态通道是在两个参与者之间交换状态的虚拟构造，位于区块链之外。实际上并没有“通道”，底层的数据传输机制也不是通道。我们使用“通道”这个术语来表示两个参与者之间的关系和共享状态，而这些状态是位于区块链之外的。

为了进一步解释这个概念，可以将其类比为 TCP 流。从更高层次的协议角度来看，它是连接互联网上两个应用程序的“套接字”。但是如果观察网络流量，TCP 流实际上只是 IP 数据包上的一条虚拟通道。每个 TCP 流的端点对 IP 数据包进行序列化和组装，以创建字节流的幻象。在底层，它实际上是由断开的数据包组成的。

类似地，支付通道只是一系列交易。如果这些交易被正确地排序和连接，它们将创建可信的可赎回义务，尽管你不信任通道的另一侧。

在本节中，我们将研究各种形式的支付通道。首先，我们将研究用于构建单向（单向）支付通道的机制，用于按流量计费的微支付服务，例如视频流。然后，我们将扩展这个机制，介绍双向支付通道。最后，我们将探讨如何将双向通道端对端连接，形成多跳通道在一个路由网络中，最初是在闪电网络的名称下提出的。

支付通道是状态通道概念的一部分，它表示在区块链之外通过最终结算在区块链上保证的状态的更改。支付通道是一个状态通道，其中被更改的状态是虚拟货币的余额。
