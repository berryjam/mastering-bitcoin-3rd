# 获取比特币核心状态信息

比特币核心通过 JSON-RPC 接口提供不同模块的状态报告。最重要的命令包括 getblockchaininfo、getmempoolinfo、getnetworkinfo 和 getwalletinfo。&#x20;

比特币的 getblockchaininfo RPC 命令早已介绍过。getnetworkinfo 命令显示有关比特币网络节点状态的基本信息。使用 bitcoin-cli 运行它：

$ bitcoin-cli getnetworkinfo

```json
{
	"version": 240001,
	"subversion": "/Satoshi:24.0.1/",
	"protocolversion": 70016,
	"localservices": "0000000000000409",
	"localservicesnames": [
		"NETWORK",
		"WITNESS",
		"NETWORK_LIMITED"
	],
	"localrelay": true,
	"timeoffset": -1,
	"networkactive": true,
	"connections": 10,
	"connections_in": 0,
	"connections_out": 10,
	"networks": [
		"...detailed information about all networks..."
	],
	"relayfee": 0.00001000,
	"incrementalfee": 0.00001000,
	"localaddresses": [],
	"warnings": ""
}
```

返回的数据采用 JavaScript 对象表示法（JSON）格式，这种格式可以轻松地被所有编程语言“消费”，但也非常易读。在这些数据中，我们看到比特币核心软件和比特币协议的版本号。我们还可以看到当前连接数以及有关比特币网络和与此节点相关的各种信息设置。

{% hint style="info" %}
bitcoind 需要一些时间，也许超过一天的时间，来赶上当前的区块链高度，因为它要从其他比特币节点下载区块并验证这些区块中的每一笔交易 —— 在撰写本文时，这些交易已经接近 10 亿笔。您可以使用 getblockchaininfo 来检查其进度，以查看已知区块的数量。本章后续示例假定您至少已经到达了区块 775,072。因为比特币交易的安全性取决于区块，所以以下示例中的一些信息将根据您的节点有多少区块而略有变化
{% endhint %}
