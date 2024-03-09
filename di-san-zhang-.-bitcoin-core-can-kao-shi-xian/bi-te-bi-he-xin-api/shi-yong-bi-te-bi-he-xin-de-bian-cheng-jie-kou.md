# 使用比特币核心的编程接口

比特币命令行助手 bitcoin-cli 对于探索比特币核心API和测试功能非常有用。但是，API的整个目的在于以编程方式访问函数。在本节中，我们将演示如何从另一个程序访问比特币核心。

\
比特币核心的API是一个JSON-RPC接口。JSON是一种非常方便的数据呈现方式，可以让人类和程序都轻松读取。RPC代表远程过程调用，这意味着我们通过网络协议调用远程（位于比特币核心节点上的）过程（函数）。在这种情况下，网络协议是HTTP。

\
当我们使用bitcoin-cli命令获取命令的帮助时，它向我们展示了使用curl的示例，这是一种功能多样的命令行HTTP客户端，用于构建这些JSON-RPC调用之一：

\
$ curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest",&#x20;

"method": "getblockchaininfo",

&#x20;"params": \[] }' -H 'content-type: text/plain;' http://127.0.0.1:8332/

该命令显示了 curl 发送一个 HTTP 请求到本地主机 (127.0.0.1)，连接到默认的比特币 RPC 端口 (8332)，并使用纯文本编码提交一个 jsonrpc 请求，请求 getblockchaininfo 方法。

您可能会注意到 curl 会要求发送凭据以及请求一起发送。比特币核心在每次启动时会创建一个随机密码，并将其放置在数据目录下，命名为 .cookie。bitcoin-cli 辅助工具可以在给定数据目录的情况下读取此密码文件。类似地，您可以复制密码并将其传递给 curl (或任何更高级别的比特币核心 RPC 封装)，如示例 3-3 所示。

示例 3-3. 使用基于 cookie 的身份验证与比特币核心

$ cat .bitcoin/.cookie **cookie**:17c9b71cef21b893e1a019f4bc071950c7942f49796ed061b274031b17b19cd0

$ curl --user **cookie**:17c9b71cef21b893e1a019f4bc071950c7942f49796ed061b274031b17b19cd0 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockchaininfo", "params": \[] }' -H 'content-type: text/plain;' http://127.0.0.1:8332/

{"result":{"chain":"main","blocks":799278,"headers":799278, "bestblockhash":"000000000000000000018387c50988ec705a95d6f765b206b6629971e6978879", "difficulty":53911173001054.59,"time":1689703111,"mediantime":1689701260, "verificationprogress":0.9999979206082515,"initialblockdownload":false, "chainwork":"00000000000000000000000000000000000000004f3e111bf32bcb47f9dfad5b", "size\_on\_disk":563894577967,"pruned":false,"warnings":""},"error":null, "id":"curltest"}

或者，您可以使用 Bitcoin Core 源代码目录中提供的辅助脚本 `./share/rpcauth/rpcauth.py` 创建一个静态密码。

如果您正在自己的程序中实现 JSON-RPC 调用，您可以使用通用的 HTTP 库来构建该调用，类似于前面的 curl 示例所示。

然而，大多数流行的编程语言都有库可以以更简单的方式“包装” Bitcoin Core API。我们将使用 python-bitcoinlib 库来简化 API 访问。该库不是 Bitcoin Core 项目的一部分，需要按照通常的 Python 库安装方式进行安装。 请记住，这需要您运行一个 Bitcoin Core 实例，该实例将用于进行 JSON-RPC 调用。

示例 3-4 中的 Python 脚本执行了一个简单的 `getblockchaininfo` 调用，并打印了 Bitcoin Core 返回数据中的块参数。

示例 3-4. 通过 Bitcoin Core 的 JSON-RPC API 运行 getblockchaininfo

```python
from bitcoin.rpc import RawProxy
# Create a connection to local Bitcoin Core node
p = RawProxy()
# Run the getblockchaininfo command, store the resulting data in info
info = p.getblockchaininfo()
# Retrieve the 'blocks' element from the info
print(info['blocks'])
```

运行后，我们得到以下结果：

$ python rpc\_example.py&#x20;

773973

它告诉我们本地 Bitcoin Core 节点的区块链中有多少个区块。这并不是令人惊讶的结果，但它演示了使用该库作为简化接口访问 Bitcoin Core 的 JSON-RPC API 的基本用法。

接下来，让我们使用 getrawtransaction 和 decodetransaction 调用来检索 Alice 对 Bob 的付款的详细信息。在示例 3-5 中，我们检索 Alice 的交易并列出交易的输出。对于每个输出，我们显示接收者地址和价值。作为提醒，Alice 的交易有一个输出支付给 Bob，另一个输出是 Alice 的找零。

示例 3-5. 检索交易并迭代其输出

```python
from bitcoin.rpc import RawProxy
p = RawProxy()
# Alice's transaction ID
txid = "466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177"
# First, retrieve the raw transaction in hex
raw_tx = p.getrawtransaction(txid)
# Decode the transaction hex into a JSON object
decoded_tx = p.decoderawtransaction(raw_tx)
# Retrieve each of the outputs from the transaction
for output in decoded_tx['vout']:
    print(output['scriptPubKey']['address'], output['value'])
```

运行此代码，我们得到：

$ python rpc\_transaction.py bc1p8dqa4wjvnt890qmfws83te0v3qxzsfu7ul63kp7u56w8qc0qwp5qv995qn 0.00020000 bc1qwafvze0200nh9vkq4jmlf4sy0tn0ga5w0zpkpg 0.00075000

前面的两个例子都相当简单。你不真的需要一个程序来运行它们；你可以同样使用bitcoin-cli助手。然而，下一个例子需要几百个RPC调用，并更清晰地展示了编程接口的使用。&#x20;

在示例3-6中，我们首先检索一个块，然后通过引用每个交易ID检索其中的每个交易。接下来，我们遍历每个交易的输出，并累加其值。&#x20;

示例3-6。检索一个块并添加所有交易输出

<pre class="language-python"><code class="lang-python">from bitcoin.rpc import RawProxy

p = RawProxy()

# The block height where Alice's transaction was recorded
blockheight = 775072

# Get the block hash of the block at the given height
blockhash = p.getblockhash(blockheight)

# Retrieve the block by its hash
block = p.getblock(blockhash)

# Element tx contains the list of all transaction IDs in the block
transactions = block['tx']

block_value = 0
# Iterate through each transaction ID in the block
for txid in transactions:
    tx_value = 0
    # Retrieve the raw transaction by ID
    raw_tx = p.getrawtransaction(txid)
<strong>    # Decode the transaction
</strong>    decoded_tx = p.decoderawtransaction(raw_tx)
    # Iterate through each output in the transaction
    for output in decoded_tx['vout']:
        # Add up the value of each output
        tx_value = tx_value + output['value']
    # Add the value of this transaction to the total
    block_value = block_value + tx_value
print("Total value in block: ", block_value)
</code></pre>

运行这段代码，我们得到：

\
$ python rpc\_block.py&#x20;

Total value in block: 10322.07722534

我们的示例代码计算出这个区块中的总交易价值为10,322.07722534 BTC（包括25 BTC的奖励和0.0909 BTC的手续费）。与通过搜索区块哈希或高度在区块浏览器网站上报告的金额进行比较。一些区块浏览器报告的总值不包括奖励和手续费。看看你能否发现差异。

\
