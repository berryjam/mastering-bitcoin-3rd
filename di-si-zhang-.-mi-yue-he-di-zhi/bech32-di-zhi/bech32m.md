# Bech32m

尽管Bech32对于隔离见证v0表现良好，但开发人员不希望在隔离见证的后续版本中不必要地限制输出大小。在没有限制的情况下，在Bech32地址中添加或删除一个“q”可能导致用户意外将资金发送到一个不可花费的输出，或者是可以由任何人花费的输出（允许任何人夺取比特币）。开发人员对Bech32问题进行了彻底的分析，并发现改变算法中的一个常数将消除这个问题，确保对最多五个字符的任何插入或删除的检测失败的频率低于十亿分之一。

具有单个不同常数的Bech32版本被称为修改过的Bech32（Bech32m）。对于相同底层数据，Bech32和Bech32m地址中的所有字符都将相同，除了最后六个字符（校验和）。这意味着钱包需要知道正在使用哪个版本才能验证校验和，但是两种地址类型都包含一个内部版本字节，使得确定这一点变得容易。

为了同时处理Bech32和Bech32m，我们将查看Bech32m比特币地址的编码和解析规则，因为它们包括了解析Bech32地址的能力，并且是比特币钱包的当前推荐地址格式。

Bech32m地址以人类可读部分（HRP）开头。BIP173中有关于创建自己的HRP的规则，但是对于比特币，您只需要了解已选择的HRP，如表4-2所示。

表 4-2. 比特币中Bech32 人类可读部分前缀

| 人类可读部分前缀 | 网络类型   |
| -------- | ------ |
| bc       | 比特币主网  |
| tb       | 比特币测试网 |

HRP 之后是一个分隔符，即数字 "1"。早期的协议分隔符使用了冒号，但某些操作系统和应用程序允许用户双击单词以突出显示以进行复制和粘贴，这样的功能将不会延伸到并且会经过冒号。数字确保双击高亮功能可以与支持 bech32m 字符串的任何程序一起工作（其中包括其他数字）。选择数字 "1" 是因为 bech32 字符串在其他情况下不使用它，以防止数字 "1" 与小写字母 "l" 之间的意外音译。

&#x20;Bech32m 地址的另一部分称为 "数据部分"。这部分包括三个元素：

\
**见证版本**

一个单字节，在bech32m比特币地址中作为分隔符之后的单个字符编码。该字母表示SegWit版本。字母“q”是SegWit v0的编码，其中引入了bech32地址的初始版本。字母“p”是SegWit v1的编码（也称为Taproot），在那里开始使用bech32m。SegWit有17个可能的版本，对于比特币来说，bech32m数据部分的第一个字节必须解码为数字0到16（包括0和16）。

**见证程序**

长度为2到40个字节。对于SegWit v0，见证程序必须是20或32个字节；其他长度都无效。截至目前，对于SegWit v1，唯一定义的长度是32个字节，但以后可能会定义其他长度。

**校验和**

为6个字符。这是使用 BCH 码创建的，一种错误纠正码（尽管对于比特币地址，稍后我们将看到它仅用于错误检测，而不是纠正）。

\
让我们通过一个示例来说明这些规则，创建bech32和bech32m地址。在以下所有示例中，我们将使用Python的bech32m参考代码。&#x20;

我们将首先生成四个输出脚本，每个脚本对应于出版时使用的不同segwit输出类型，以及一个对应于尚未定义含义的未来segwit版本。这些脚本列在表4-3中。

表4-3 不同类型segwit输出的脚本

<table><thead><tr><th width="119">输出类型</th><th>示例脚本</th></tr></thead><tbody><tr><td>P2WPKH</td><td>OP_0 2b626ed108ad00a944bb2922a309844611d25468</td></tr><tr><td>P2WSH</td><td>OP_0 648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f</td></tr><tr><td>P2TR</td><td>OP_1 2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311</td></tr><tr><td>Future Example</td><td>OP_16 0000</td></tr></tbody></table>

\
对于P2WPKH输出，见证程序包含一个承诺，其构造方式与“P2PKH的传统地址”（见第63页）中的P2PKH输出的承诺完全相同。将公钥传递到SHA256哈希函数中。然后，将结果的32字节摘要传递到RIPEMD-160哈希函数中。该函数的摘要（承诺）放置在见证程序中。

对于付款给见证脚本哈希（P2WSH）输出，我们不使用P2SH算法。而是将脚本传递到SHA256哈希函数中，并使用该函数的32字节摘要作为见证程序。对于P2SH，SHA256摘要再次与RIPEMD-160哈希，但在某些情况下可能不安全；有关详细信息，请参见“P2SH碰撞攻击”（第73页）。使用SHA256而不是RIPEMD-160的结果是P2WSH承诺为32字节（256位），而不是20字节（160位）。

对于付款到taproot（P2TR）输出，见证程序是secp256k1曲线上的一个点。它可以是一个简单的公钥，但在大多数情况下，它应该是一个公钥，该公钥承诺了一些附加数据。我们将在“Taproot”（第178页）中详细了解这个承诺。

对于未来segwit版本的示例，我们简单地使用最高可能的segwit版本号（16）和允许的最小见证程序（2字节）以及空值。

现在我们知道了版本号和见证程序，我们可以将它们转换为bech32地址。让我们使用Python的bech32m参考库快速生成这些地址，然后深入了解发生了什么：

$ github="https://raw.githubusercontent.com"&#x20;

$ wget $github/sipa/bech32/master/ref/python/segwit\_addr.py&#x20;

$ python

```python
>>> from segwit_addr import *
>>> from binascii import unhexlify
>>> help(encode)
encode(hrp, witver, witprog)
 Encode a segwit address.
>>> encode('bc', 0, unhexlify('2b626ed108ad00a944bb2922a309844611d25468'))
'bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'
>>> encode('bc', 0,unhexlify('648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f'))
'bc1qvj9r9egtd7mu2gemy28kpf4zefq4ssqzdzzycj7zjhk4arpavfhsct5a3p'
>>> encode('bc', 1,
unhexlify('2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311'))
'bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7'
>>> encode('bc', 16, unhexlify('0000'))
'bc1sqqqqkfw08p'
```

如果我们打开文件segwit\_addr.py并查看代码的操作，我们会注意到bech32（用于segwit v0）和bech32m（用于后续segwit版本）之间唯一的区别是常数：

BECH32\_CONSTANT = 1&#x20;

BECH32M\_CONSTANT = 0x2bc830a3

接下来我们注意到生成校验和的代码。在校验和的最后一步中，适当的常数通过异或运算合并到值中。这个单一的值是bech32和bech32m之间唯一的区别。

&#x20;校验和创建完成后，数据部分（包括见证版本、见证程序和校验和）中的每个5位字符都转换为字母数字字符。&#x20;

要解码回输出脚本，我们反向工作。首先让我们使用参考库来解码我们的两个地址：

```python
>>> help(decode)
decode(hrp, addr)
 Decode a segwit address.
>>> _ = decode("bc", "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee")
>>> _[0], bytes(_[1]).hex()
(0, '2b626ed108ad00a944bb2922a309844611d25468')
>>> _ = decode("bc",
 "bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7")
>>> _[0], bytes(_[1]).hex()
(1, '2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311')
```

我们获得了见证版本和见证程序。 这些可以插入到我们输出脚本的模板中：

\<version> \<program>

例如：

OP\_0 2b626ed108ad00a944bb2922a309844611d25468&#x20;

OP\_1 2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311

{% hint style="danger" %}
这里需要注意的一个可能错误是，见证版本0对应的是OP\_0，使用的是字节0x00，但见证版本1对应的是OP\_1，使用的是字节0x51。而见证版本2到16分别对应0x52到0x60。
{% endhint %}

当实现bech32m编码或解码时，我们强烈建议您使用BIP350提供的测试向量。我们也要求您确保您的代码通过与支付尚未定义的未来segwit版本相关的测试向量。即使您无法在新的比特币功能推出时立即添加支持，这也将帮助您的软件在未来多年保持可用。

