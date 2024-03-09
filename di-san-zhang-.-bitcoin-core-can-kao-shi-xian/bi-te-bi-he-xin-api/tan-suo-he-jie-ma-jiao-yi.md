# 探索和解码交易

在“从在线商店购买”中，Alice从Bob的商店购买了商品。她的交易已记录在区块链上。让我们使用 API 通过传递交易ID（txid）作为参数来检索和检查该交易：

\
$ bitcoin-cli getrawtransaction 466200308696215bbc949d5141a49a41\\\
38ecdfdfaa2a8029c1f9bcecd1f96177

01000000000101eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da13569 8679268041c54a0100000000ffffffff02204e0000000000002251203b41daba 4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f8240100 000000001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe 2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51b e739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e817130100000000

{% hint style="info" %}
交易ID（txid）并不具有权威性。在区块链中找不到txid并不意味着该交易未被处理。这被称为“交易可塑性”，因为在交易确认之前，交易可以被修改，从而改变其txid。一旦交易被包含在一个区块中，其txid就不能更改，除非发生了区块链重组，其中该区块从最佳区块链中被移除。在交易获得几个确认之后，区块链重组变得十分罕见。
{% endhint %}

命令getrawtransaction以十六进制表示返回一个序列化的交易。为了解码它，我们使用decoderawtransaction命令，并将十六进制数据作为参数传递。您可以复制getrawtransaction返回的十六进制数据，并将其粘贴为decoderawtransaction的参数：

$ bitcoin-cli decoderawtransaction 01000000000101eb3ae38f27191aa5f3850dc9cad0\
0492b88b72404f9da135698679268041c54a0100000000ffffffff02204e00000000000022512\
03b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f82401000000\
00001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe2d8ef13ed0af21d4f\
4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6\
dab0d2fa2b42a45182fc83e817130100000000

```json
{
	"txid": "466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177",
	"hash": "f7cdbc7cf8b910d35cc69962e791138624e4eae7901010a6da4c02e7d238cdac",
	"version": 1,
	"size": 194,
	"vsize": 143,
	"weight": 569,
	"locktime": 0,
	"vin": [{
		"txid": "4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19...aeb",
		"vout": 1,
		"scriptSig": {
			"asm": "",
			"hex": ""
		},
		"txinwitness": [
			"cf5efe2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e5...301"
		],
		"sequence": 4294967295
	}],
	"vout": [{
			"value": 0.00020000,
			"n": 0,
			"scriptPubKey": {
				"asm": "1 3b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca...068",
				"desc": "rawtr(3b41daba4c9ace578369740f15e5ec880c28279ee7f51b...6ev",
				"hex": "51203b41daba4c9ace578369740f15e5ec880c28279ee7f51b07d...068",
				"address": "bc1p8dqa4wjvnt890qmfws83te0v3qxzsfu7ul63kp7u56w8q...5qn",
				"type": "witness_v1_taproot"
			}
		},
		{
			"value": 0.00075000,
			"n": 1,
			"scriptPubKey": {
				"asm": "0 7752c165ea7be772b2c0acb7f4d6047ae6f4768e",
				"desc": "addr(bc1qwafvze0200nh9vkq4jmlf4sy0tn0ga5w0zpkpg)#qq404gts",
				"hex": "00147752c165ea7be772b2c0acb7f4d6047ae6f4768e",
				"address": "bc1qwafvze0200nh9vkq4jmlf4sy0tn0ga5w0zpkpg",
				"type": "witness_v0_keyhash"
			}
		}
	]
}
```

\
交易解码显示了此交易的所有组件，包括交易输入和输出。在这种情况下，我们看到该交易使用了一个输入，并生成了两个输出。这笔交易的输入是来自先前确认的交易的输出（显示为输入txid）。这两个输出对应于付款给Bob和找零返回给Alice。

我们可以通过使用相同的命令（例如getrawtransaction）检查在此交易中引用其txid的先前交易来进一步探索区块链。从一笔交易跳转到另一笔交易，我们可以跟踪一系列交易，从而了解硬币是如何从一个所有者传递到下一个所有者的。

\
