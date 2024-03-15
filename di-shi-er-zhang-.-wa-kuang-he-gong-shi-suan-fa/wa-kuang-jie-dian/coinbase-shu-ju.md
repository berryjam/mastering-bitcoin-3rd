# Coinbase数据

\
Coinbase 交易没有输入脚本字段。相反，这个字段被 coinbase 数据替换，其长度必须在 2 到 100 字节之间。除了前几个字节外，coinbase 数据的其余部分可以由矿工任意使用；它是任意的数据。

例如，在创世区块中，中本聪在 coinbase 数据中添加了文本“The Times 03/Jan/2009 Chancellor on brink of second bailout for banks”，将其作为这个区块可能创建的最早日期的证明，并传递了一条信息。目前，矿工经常使用 coinbase 数据来包含额外的 nonce 值和标识矿池的字符串。

coinbase 的前几个字节曾经是任意的，但现在不再是这样了。根据 BIP34，版本 2 的区块（版本字段设置为 2 或更高）必须在 coinbase 字段的开头作为脚本“push”操作包含区块高度。
