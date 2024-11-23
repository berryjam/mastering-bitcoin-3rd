---
description: cpuminer
---

# 使用cpuminer进行挖矿

默认情况下，**Bitcoin 全节点**（`bitcoind`）不会自动挖矿。运行全节点的主要功能是维护和验证区块链，而不是参与挖矿。全节点的职责是接收、验证、转发交易和区块，以及存储整个区块链数据。挖矿需要大量的计算资源，而大多数运行全节点的用户只是为了支持网络或进行钱包管理，不是为了挖矿。

所以如果启动了全节点后，如果往全节点发送交易的时候，我们可以观察到交易能进入到mempool，但并没有出块。有两种方式，能够触发挖矿。

1. 使用 bitcoin-cli generatetoaddress \<nblocks> \<address>，通过rpc接口调用全节点的GenerateBlocks进行挖矿。这种方式只适合在测试环境或者自定义网络里进行挖矿，在主网几乎不太可能能挖到块。
2. 使用专门为比特币或其他基于 SHA256 算法的加密货币设计的挖矿软件，如软件cpuminer，可以通过 `getblocktemplate` 连接比特币节点，进行 Solo 挖矿，或者通过矿池的 Stratum 协议与矿池合作。

下面介绍从[cpuminer](https://github.com/pooler/cpuminer)源码编译，并连接到本地运行的全节点进行solo挖矿。

```
$mkdir -p /data/miner_workspace/src/github.com/pooler
$git clone git@github.com:pooler/cpuminer.git
$cd cpuminer
$./autogen.sh
$./nomacro.pl
$./configure CFLAGS="-O3"
$make
```

结束后，当前目录生成程序minerd。

但是cpuminer需要获取blocktemplate才能挖矿，如果运行自定义网络只运行一个节点是没办法获取到的，调用getblocktemplate会返回not connected错误。

```
$bitcoin-cli -rpcuser=user -rpcpassword=pass -rpcconnect=localhost -rpcport=8332 getblocktemplate '{"rules": ["segwit"]}'
error code: -10
error message:
Bitcoin Core is in initial sync and waiting for blocks...
```

所以还需要额外运行另外一个节点，并连接到当前节点。

```
$bitcoind --conf=/data/bitcoin/bitcoin.conf -daemon -reindex -addnode=<机器1的ip>:8333
```

此刻，因为网络区块高度为0，如果再调用getblocktemplate，会提示区块仍然同步中。

```
$bitcoin-cli -rpcuser=user -rpcpassword=pass -rpcconnect=localhost -rpcport=8332 getblocktemplate '{"rules": ["segwit"]}'
error code: -10
error message:
Bitcoin Core is in initial sync and waiting for blocks...
```

此刻需要通过generatetoaddress生成至少一个块，就可以查询到blocktemplate使用cpuminer进行挖矿。

```
$bitcoin-cli -rpcuser=user -rpcpassword=pass -rpcconnect=localhost -rpcport=8332 generatetoaddress 1 <address>
$bitcoin-cli -rpcuser=user -rpcpassword=pass -rpcconnect=localhost -rpcport=8332 getblocktemplate '{"rules": ["segwit"]}'
{
  "capabilities": [
    "proposal"
  ],
  "version": 536870912,
  ......
}
```

通过minerd连接到本地节点进行挖矿，在本地成功计算出nonce后，会调用submitblock，提交块到当前全节点。

```
$/data/miner_workspace/src/github.com/pooler/cpuminer/minerd --url=http://127.0.0.1:8332 --userpass=user:pass --coinbase-addr=<address> --protocol-dump
> POST / HTTP/1.1
Host: 127.0.0.1:8332
Authorization: Basic YmVycnk6MTIzNDU2
Accept-Encoding: deflate, gzip, br, zstd
Content-Type: application/json
User-Agent: cpuminer/2.5.1
X-Mining-Extensions: midstate
Content-Length: 230

[2024-11-23 17:57:14] thread 3: 24 hashes, 9.68 khash/s
[2024-11-23 17:57:14] thread 2: 24 hashes, 9.18 khash/s
[2024-11-23 17:57:14] thread 1: 24 hashes, 9.44 khash/s
[2024-11-23 17:57:14] thread 0: 24 hashes, 9.01 khash/s
[2024-11-23 17:57:14] JSON protocol request:
{"method": "submitblock", "params": ["00000020259b13a6f59da1bd307ecac4b4280fbb1217a4982cf23f869bd1f34af3608967ac4c87b4c999bad534076fae39980dd64c7bfc3f8845b5a365da32b011e055e7faa64167ffff7f20bfffffff0101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff025200ffffffff01002f6859000000001976a914a6cc6d3896e4181ff3608b15972e22f4d31523a088ac00000000"], "id":1}
```

如果创世难度设置很低的话，瞬间出完2015块后，网络难度会自动调整成非常高，返回high-hash结果，当前算力就挖不出来。这就需要使用特定的挖矿机器或者gpu，加入到矿池进行挖矿。

```
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Content-Type: application/json
< Date: Sat, 23 Nov 2024 09:53:07 GMT
< Content-Length: 43
<
* Connection #1 to host 127.0.0.1 left intact
[2024-11-23 09:53:07] JSON protocol response:
{
   "error": null,
   "result": "high-hash",
   "id": 1
}
```
