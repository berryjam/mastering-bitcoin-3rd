# 简单的应用开发(二)：使用rust与BRC-20交互

在上一节已经介绍过如何使用bitcoinj与bitcoin交互，遗憾的是bitcoinj本身不支持构建P2TR的脚本，也缺少了BRC-20的indexer，所以不支持BRC-20。可能是因为BRC-20本身不像btc一样是链上的原生资产，但这不妨碍BRC-20的持续火热。

关于BRC-20的综合介绍，可以参见第十四章的翻译《BRC-20交易指南》。下面介绍如何基于两个rust的项目实现部署一个BRC-20合约及如何扫描区块解析这笔部署交易。

[ord-rs](https://github.com/bitfinity-network/ord-rs)：这个项目支持构建BRC-20交易，包括部署、铸造和发送BRC-20。但是这个项目缺少了indexer，不支持BRC-20交易的解析。另外这个项目缺少完整钱包功能，在构建BRC-20交易的时候，需要显式指定可用的UTXO，而账户可用的UTXO列表可以通过上一节的WalletTool导出，然后选择能够覆盖交易手续费的一笔或者多笔交易即可。

[ordhook](https://github.com/berryjam/ordhook)：由于上面ord-rs缺少indexer，所以需要这个项目来解析链上的BRC-20交易，但是项目本身还有一些配置，直接运行起来会有些问题，在原来的基础修改了这些：[https://github.com/berryjam/ordhook](https://github.com/berryjam/ordhook)。

## 1.发起一笔BRC-20交易





## 2.扫描解析BRC-20交易

