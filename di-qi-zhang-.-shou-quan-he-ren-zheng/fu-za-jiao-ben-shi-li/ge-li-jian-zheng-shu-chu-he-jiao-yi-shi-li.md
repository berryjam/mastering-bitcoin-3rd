# 隔离见证输出和交易示例

让我们来看一些示例交易，并了解它们在隔离见证下的变化。首先，我们将看看如何将P2PKH支付作为隔离见证程序完成。然后，我们将研究P2SH脚本的隔离见证等效物。最后，我们将看看如何将前述隔离见证程序嵌入P2SH脚本中。

## 支付给见证公钥哈希（P2WPKH）

让我们首先看一下一个P2PKH输出脚本的示例：

OP\_DUP OP\_HASH160 ab68025513c3dbd2f7b92a94e0581f5d50f654e7&#x20;

OP\_EQUALVERIFY OP\_CHECKSIG

有了隔离见证，Alice会创建一个P2WPKH脚本。如果该脚本与相同的公钥进行了绑定，它将如下所示：

0 ab68025513c3dbd2f7b92a94e0581f5d50f654e7

如您所见，P2WPKH输出脚本比P2PKH等价脚本简单得多。它由两个值组成，推送到脚本评估堆栈上。对于旧的（不支持隔离见证的）比特币客户端，这两次推送看起来像是任何人都可以使用的输出。对于较新的、支持隔离见证的客户端，第一个数字（0）被解释为版本号（见证版本），而第二部分（20字节）是一个见证程序。这20字节的见证程序简单地是公钥的哈希值，就像P2PKH脚本中一样。&#x20;

现在，让我们看一下Bob用来花费这个输出的相应交易。对于原始脚本，花费交易必须在交易输入中包含一个签名：

```
[...]
"vin" : [
 "txid": "abcdef12345...",
 "vout": 0,
 "scriptSig": “<Bob’s scriptSig>”,
]
[...]
```

然而，要花费P2WPKH输出，交易在该输入上没有签名。相反，Bob的交易有一个空的输入脚本，并包含一个见证结构：

```
[...]
"vin" : [
 "txid": "abcdef12345...",
 "vout": 0,
 "scriptSig": “”,
]
[...]
“witness”: “<Bob’s witness structure>”
[...]
```

## P2WPKH类型钱包构建

P2WPKH见证程序应该只由接收方创建，而不应由支出方从已知的公钥、P2PKH脚本或地址进行转换。支出方无法知道接收方的钱包是否具有构建隔离见证交易和花费P2WPKH输出的能力。

此外，P2WPKH输出必须由压缩公钥的哈希构建。未压缩的公钥在隔离见证中是非标准的，并且可能会在未来的软分叉中被明确禁用。如果P2WPKH中使用的哈希来自未压缩的公钥，则可能无法花费，并且您可能会丢失资金。P2WPKH输出应由收款方的钱包通过从其私钥派生压缩公钥来创建。&#x20;

{% hint style="danger" %}
P2WPKH应该由接收方通过将压缩的公钥转换为P2WPKH哈希来构建。支出方或其他任何人都不应该将P2PKH脚本、比特币地址或未压缩的公钥转换为P2WPKH见证脚本。一般来说，支出方应该按照接收方指示的方式发送。
{% endhint %}

## 支付给见证脚本哈希 (P2WSH)

segwit v0见证程序的第二种类型对应于P2SH脚本。我们在“支付到脚本哈希”中看到了这种类型的脚本。在该示例中，P2SH被Mohammed的公司用来表示多签名脚本。向Mohammed的公司的付款被编码为以下脚本：

OP\_HASH160 54c557e07dde5bb6cb791c7a540e0a4796f5e97e OP\_EQUAL

这个P2SH脚本引用了一个赎回脚本的哈希，该赎回脚本定义了一个2-of-3多重签名的要求来花费资金。要花费这个输出，Mohammed的公司将呈现赎回脚本（其哈希与P2SH输出中的脚本哈希匹配）以及满足该赎回脚本所需的签名，全部都在交易输入中：

```
[...]
"vin" : [
 "txid": "abcdef12345...",
 "vout": 0,
 "scriptSig": “<SigA> <SigB> <2 PubA PubB PubC PubD PubE 5 OP_CHECKMULTISIG>”,
]
```

现在，让我们看看如何将整个示例升级为segwit v0。如果Mohammed的客户正在使用兼容segwit的钱包进行付款，他们将创建一个P2WSH输出，看起来像这样：

0 a9b7b38d972cabc7961dbfbcb841ad4508d133c47ba87457b4a0e8aae86dbb89

与P2WPKH示例一样，你可以看到隔离见证等效脚本要简单得多，减少了P2SH脚本中的模板开销。相反，隔离见证输出脚本由两个值推送到堆栈中：一个见证版本（0）和见证脚本的32字节SHA256哈希（见证程序）。

{% hint style="info" %}
虽然P2SH使用了20字节的RIPEMD160(SHA256(script))哈希，但P2WSH见证程序使用了32字节的SHA256(script)哈希。这种哈希算法选择上的差异是有意为之的，以在某些用例中提供更强的安全性（P2WSH提供128位的安全性，而P2SH提供80位的安全性）。详情请参阅“P2SH碰撞攻击”（第73页）。
{% endhint %}

\
穆罕默德的公司可以通过呈现正确的见证脚本和足够的签名来消费P2WSH输出。见证脚本和签名将作为见证结构的一部分包含在其中。不会将任何数据放入输入脚本，因为这是一个原生见证程序，不使用遗留的输入脚本字段：

```
[...]
"vin" : [
 "txid": "abcdef12345...",
 "vout": 0,
 "scriptSig": “”,
]
[...]
“witness”: “<SigA> <SigB> <2 PubA PubB PubC PubD PubE 5 OP_CHECKMULTISIG>”
[...]
```

## P2WPH和P2WSH之间的差异

\
在前两节中，我们展示了两种类型的见证程序：“支付给见证公钥哈希（P2WPKH）”和“支付给见证脚本哈希（P2WSH）”。这两种类型的见证程序都由相同的版本号后跟数据推送组成。它们看起来非常相似，但解释方式有很大不同：其中一种被解释为公钥哈希，需要用签名来满足，而另一种被解释为脚本哈希，需要用见证脚本来满足。它们之间的关键区别在于见证程序的长度：

* P2WPKH中的见证程序为20字节。
* P2WSH中的见证程序为32字节。&#x20;

这是区分两种见证程序类型的唯一差异。通过查看哈希的长度，节点可以确定它是P2WPKH还是P2WSH类型的见证程序。