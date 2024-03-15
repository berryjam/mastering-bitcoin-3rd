# Regtest：本地区块链

\
Regtest，全称“回归测试”，是比特币核心功能之一，允许你创建一个用于测试目的的本地区块链。与signet和testnet3不同，它们是公共的、共享的测试区块链，regtest区块链旨在作为本地测试的封闭系统运行。你可以从头开始启动一个regtest区块链。你可以向网络添加其他节点，也可以只运行一个节点，用于测试比特币核心软件。&#x20;

要启动比特币核心进入regtest模式，你可以使用regtest标志：

```
$ bitcoind -regtest
```

与testnet一样，比特币核心将在bitcoind默认目录的regtest子目录下初始化一个新的区块链：

```
bitcoind: Using data directory /home/username/.bitcoin/regtest
```

要使用命令行工具，您也需要指定regtest标志。让我们尝试使用getblockchaininfo命令来检查regtest区块链：

```
$ bitcoin-cli -regtest getblockchaininfo
{
 "chain": "regtest",
 "blocks": 0,
 "headers": 0,
 "bestblockhash": "0f9188f13cb7b2c71f2a335e3[...]b436012afca590b1a11466e2206",
 "difficulty": 4.656542373906925e-10,
 "mediantime": 1296688602,
 "verificationprogress": 1,
 "chainwork": "[...]000000000000000000000000000000000000000000000000000002",
 "pruned": false,
 [...]
```

您可以看到，目前还没有区块。让我们创建一个默认钱包，获取一个地址，然后挖一些（500个区块）以获取奖励：

```
$ bitcoin-cli -regtest createwallet ""
$ bitcoin-cli -regtest getnewaddress
bcrt1qwvfhw8pf79kw6tvpmtxyxwcfnd2t4e8v6qfv4a
$ bitcoin-cli -regtest generatetoaddress 500 \
 bcrt1qwvfhw8pf79kw6tvpmtxyxwcfnd2t4e8v6qfv4a
[
 "3153518205e4630d2800a4cb65b9d2691ac68eea99afa7fd36289cb266b9c2c0",
 "621330dd5bdabcc03582b0e49993702a8d4c41df60f729cc81d94b6e3a5b1556",
 "32d3d83538ba128be3ba7f9dbb8d1ef03e1b536f65e8701893f70dcc1fe2dbf2",
 ...,
 "32d55180d010ffebabf1c3231e1666e9eeed02c905195f2568c987c2751623c7"
]
```

挖掘这些区块只需要几秒钟时间，这确实很容易进行测试。如果您检查钱包余额，您会看到您获得了前400个区块的奖励（coinbase 奖励必须在您能够支配之前有100个区块的深度）：

```
$ bitcoin-cli -regtest getbalance
12462.50000000
```

