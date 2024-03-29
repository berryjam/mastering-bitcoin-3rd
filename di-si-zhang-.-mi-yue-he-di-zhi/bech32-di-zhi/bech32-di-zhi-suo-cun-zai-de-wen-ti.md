# Bech32地址所存在的问题

Bech32地址在每个方面都可能取得成功，除了一个问题。关于它们能够检测错误的数学保证只有在你输入到钱包中的地址长度与原始地址的长度相同时才适用。如果在转录过程中添加或删除任何字符，则该保证将不适用，你的钱包可能会将资金发送到错误的地址。然而，即使没有这个保证，人们仍然认为用户添加或删除字符几乎不可能产生带有有效校验和的字符串，从而确保用户的资金安全。

不幸的是，Bech32算法中一个常量的选择恰巧使得在以字母“p”结尾的地址的倒数第二个位置添加或删除字母“q”变得非常容易。在这种情况下，你还可以多次添加或删除字母“q”。这样做有时会被校验和检测到，但远不如Bech32对字符替换错误的预期频率那样少见。请参见示例4-4。

示例4-4. 扩展Bech32地址的长度而不使其校验和失效

预期的 Bech32 地址:

bc1pqqqsq9txsqp

具有有效校验和的不正确地址:

bc1pqqqsq9txsqqqqp&#x20;

bc1pqqqsq9txsqqqqqqp&#x20;

bc1pqqqsq9txsqqqqqqqqp&#x20;

bc1pqqqsq9txsqqqqqqqqqp&#x20;

bc1pqqqsq9txsqqqqqqqqqqqp

对于初始版本的隔离见证（版本0），这并不是一个实际的问题。对于v0隔离见证输出，只定义了两个有效的长度：22字节和34字节。这对应于bech32地址的长度为42个字符或62个字符，因此某人需要在bech32地址的倒数第二个位置添加或删除字母“q”20次，才能向无效地址发送资金，而钱包无法检测到。然而，如果未来实施了基于隔离见证的升级，这将成为用户的一个问题。

