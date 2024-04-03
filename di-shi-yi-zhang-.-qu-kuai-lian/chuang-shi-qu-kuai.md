# 创世区块

\
区块链中的第一个区块称为创世区块，创建于2009年。它是区块链中所有区块的共同祖先，这意味着如果你从任何一个区块开始，沿着时间的倒序链向后跟踪，最终会到达创世区块。

每个节点始终以至少一个区块的区块链开始，因为创世区块被静态编码在比特币核心中，因此无法更改。每个节点始终“知道”创世区块的哈希和结构，以及创建的固定时间，甚至包括其中的单个交易。因此，每个节点都有一个区块链的起点，一个安全的“根”，用于构建一个可信的区块链。

在Bitcoin Core客户端的[chainparams.cpp](https://github.com/bitcoin/bitcoin/blob/3955c3940eff83518c186facfec6f50545b5aab5/src/chainparams.cpp#L123)中，可以看到静态编码的创世区块。

以下标识哈希属于创世区块：

000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f

您可以在几乎任何区块浏览器网站上搜索该区块哈希，比如blockstream.info，您会找到一个页面描述该区块的内容，其中包含该哈希的URL链接。

[https://blockstream.info/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f](https://blockstream.info/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f)

或者，您可以在命令行上使用Bitcoin Core获取该区块：

```
$ bitcoin-cli getblock \
 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
{
"hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
"confirmations": 790496,
"height": 0,
"version": 1,
"versionHex": "00000001",
"merkleroot": "4a5e1e4baab89f3a32518a88c3[...]76673e2cc77ab2127b7afdeda33b",
"time": 1231006505,
"mediantime": 1231006505,
"nonce": 2083236893,
"bits": "1d00ffff",
"difficulty": 1,
"chainwork": "[...]000000000000000000000000000000000000000000000100010001",
"nTx": 1,
"nextblockhash": "00000000839a8e6886ab5951d7[...]fc90947ee320161bbf18eb6048",
"strippedsize": 285,
"size": 285,
"weight": 1140,
"tx": [
"4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
] }
```

创世区块中包含一条信息。Coinbase 交易输入包含文本：“The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.” 这条信息旨在通过引用英国报纸《泰晤士报》的头条，提供该区块可能被创建的最早日期的证明。它还作为一种戏谑的提醒，强调了独立货币系统的重要性，因为比特币的推出恰逢前所未有的全球金融危机。这条信息是比特币的创始人中本聪嵌入到第一个区块中的。
