# 简单的应用开发(二)：使用rust与BRC-20交互

在上一节已经介绍过如何使用bitcoinj与bitcoin交互，遗憾的是bitcoinj本身不支持构建P2TR的脚本，也缺少了BRC-20的indexer，所以不支持BRC-20。可能是因为BRC-20本身不像btc一样是链上的原生资产，但这不妨碍BRC-20的持续火热。

关于BRC-20的综合介绍，可以参见第十四章的翻译《BRC-20交易指南》。下面介绍如何基于两个rust的项目实现部署一个BRC-20合约及如何扫描区块解析这笔部署交易。

[ord-rs](https://github.com/bitfinity-network/ord-rs)：这个项目支持构建BRC-20交易，包括部署、铸造和发送BRC-20。但是这个项目缺少了indexer，不支持BRC-20交易的解析。另外这个项目缺少完整钱包功能（缺少UTXO历史和coin selector），在构建BRC-20交易的时候，需要显式指定可用的UTXO，而账户可用的UTXO列表可以通过上一节的WalletTool导出，然后手动选择能够覆盖交易手续费的一笔或者多笔交易即可。由于这个项目手续费的计算是固定的，至少为0.000102 （2500+4700+3000=10200聪，1BTC=10^8 聪）BTC，所以测试时候需要多准备些测试BTC。

<figure><img src="../.gitbook/assets/image (1) (1) (1).png" alt=""><figcaption><p>固定手续费</p></figcaption></figure>

[ordhook](https://github.com/berryjam/ordhook)：由于上面ord-rs缺少indexer，所以需要这个项目来解析链上的BRC-20交易，但是项目本身还有一些配置，直接运行还会下载一些预处理数据，缺少reveal交易的打印信息，在原来的基础修改了这些：[https://github.com/berryjam/ordhook](https://github.com/berryjam/ordhook)。

本节使用bitcoinj钱包创建的密钥，及通过钱包工具导出所有UTXO。然后通过ord-rs发起交易，再使用ordhook解析这笔交易，希望能给到大家一些启发。

{% hint style="info" %}
请先安装rust，只需要一条命令即可：

$curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

安装完成后， 便可以使用cargo编译运行rust程序。
{% endhint %}

## 0.准备工作

上一节使用WalletTool可以导出钱包的相关信息，通过添加参数--dump-privkeys即可显示私钥信息。

```
gradle -PmainClass=org.bitcoinj.wallettool.WalletTool run --args='dump --chain /Users/bj89200ml/Documents/java_workspace/src/github.com/bitcoinj/bitcoinj/walletappkit-example.spvchain --wallet /Documents/java_workspace/src/github.com/bitcoinj/bitcoinj/walletappkit-example.wallet --net testnet --dump-privkeys'
```

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption><p>图 3.8 私钥信息</p></figcaption></figure>

这里会显示多个账户，是因为我们使用的HD派生钱包，对于钱包来说，这些账户的UTXO都可以使用。以账户tb1q2uhd28nklz63xj2u6j78l6902ehsmjl3d75q5e为例，下面为对应的私钥，而WIF(Wallet Import Format)格式是Base58编码后的格式，可读性更好。这里由于ord-rs限制了只能使用WIF格式的私钥，这里我们选择后面那个priv WIF。

<figure><img src="../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>图 3.9 账户UTXO列表</p></figcaption></figure>

可以看到这里有几笔交易信息，其中第1笔可用资金相对比较多，为0.0002 BTC，output有两个，其中out为0的接受地址为我们的账户：tb1q2uhd28nklz63xj2u6j78l6902ehsmjl3d75q5e，这里可以用作部署BRC-20交易。另外一笔由于是一笔找零output，账户是其他用户的，所以不能使用。

至此，我们已经准备好发起一笔BRC-20交易。

## 1.发起一笔BRC-20交易

```
$git clone https://github.com/bitfinity-network/ord-rs.git
$cd ord-rs
```

ord-rs可以使用以下命令部署一个BRC-20 Token。

```
cargo run --example deploy --
  -T <tick>
  -a <total-supply>
  -l <mint-limit>
  -p <WIF private key>
  -n <network>
  <tx_input_id:tx_input_index> <tx_input_id:tx_input_index> <tx_input_id:tx_input_index>
```

tick：BRC-20代币符号，长度为4个字母，如"ordi"，如果存在则无效。

total-supply：为BRC-20的最大供应量。

mint-limit：每次 BRC-20 代币铸造量的限制。

WIF private key：账户的私钥，WIF格式。

network：所选择部署的网络，我们使用测试网，填test即可。

tx\_input\_id:tx\_input\_index：最后是所选择的可用input，是一个列表，因为有可能单笔交易不能覆盖交易总费用。如图3.9所示，选择0.0002 BTC那笔交易，则填21649a082d765b3c1cdc6c3c2878cc59c77e9d6faed6690db9e4fe21be3b30a6:0。

因此整体运行如下：

```
$cargo run --example deploy -- -T sAts -a 21000000 -l 100  -p <WIF prive key> -n test 21649a082d765b3c1cdc6c3c2878cc59c77e9d6faed6690db9e4fe21be3b30a6:0
```

运行输出如下：

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption><p>图 3.10 运行输出</p></figcaption></figure>

上面会打印相关的交易信息，这里我们只要关心两笔交易，一笔是commit交易，另外一笔是reveal交易。交易hash分别为：2aa8c13d0a1348feb245ea45fd1912fb7c62d81fa71b6566e313a2d8fcf0c343、75f8c989a042f51849ae63a711d7ed4628afdb6edc55d53e7b22ace898d23927。

由于Taproot和MAST的特性，第一笔commit交易与普通的P2SH转账交易没区别，要在链上显示具体的Token信息，还必须提供一笔reveal交易，来显示具体的脚本信息。所以后面扫描解析BRC-20交易，也只需要关心reveal交易：75f8c989a042f51849ae63a711d7ed4628afdb6edc55d53e7b22ace898d23927。

## 2.扫描解析BRC-20交易

```
$git clone https://github.com/berryjam/ordhook.git
$cd ordhook
$cargo run --bin ordhook config new --testnet
```

上面会在目录ordhook下创建Ordhook.toml，我们需要修改配置，连接到上一节我们运行的bitcoin节点，配置大致如下，按照本地实际环境修改即可。

```
[storage]
working_dir = "ordhook"

# The Http Api allows you to register / deregister
# dynamically predicates.
# Disable by default.
#
# [http_api]
# http_port = 20456

[network]
mode = "testnet"
bitcoind_rpc_url = "http://127.0.0.1:18332"
bitcoind_rpc_username = "berry"
bitcoind_rpc_password = "123456"
# Bitcoin block events can be received by Chainhook
# either through a Bitcoin node's ZeroMQ interface,
# or through the Stacks node. Zmq is being
# used by default:
bitcoind_zmq_url = "tcp://0.0.0.0:18543"
# but stacks can also be used:
# stacks_node_rpc_url = "http://0.0.0.0:20443"

[resources]
ulimit = 2048
cpu_core_available = 16
memory_available = 32
bitcoind_rpc_threads = 4
bitcoind_rpc_timeout = 15
expected_observers_count = 1

# Disable the following section if the state
# must be built locally
[snapshot]
download_url = "https://archive.hiro.so/mainnet/ordhook/mainnet-ordhook-sqlite-latest"

[logs]
ordinals_internals = true
chainhook_internals = true

```

执行扫描解析命令

```
cargo run  --release -- scan blocks --interval 2754428:2754428 --config-path=./Ordhook.toml --post-to=http://localhost:3000/api/events
```

运行结果如下：

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption><p>图 3.11 区块BRC-20交易扫描结果</p></figcaption></figure>

可以看到其中一笔交易hash为：75f8c989a042f51849ae63a711d7ed4628afdb6edc55d53e7b22ace898d23927，正是刚才我们发起部署BRC-20 Token的交易，其铭文内容十六进制内容为7b226f70223a226465706c6f79222c2270223a226272632d3230222c227469636b223a2273417473222c226d6178223a223231303030303030222c226c696d223a22313030227d，使用utf8编码。我们可以通过[在线将十六进制转utf8](https://onlinetools.com/utf8/convert-hexadecimal-to-utf8)后查看到原文：

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption><p>图 3.12 铭文内容</p></figcaption></figure>

{"op":"deploy","p":"brc-20","tick":"sAts","max":"21000000","lim":"100"}

其中op：表示操作类型，有deploy、mint、transfer三种类型。

p：固定为brc-20。

tick：Token符号，上面我们部署使用的sAts，这里一致。

max：Token最大发行量，上面使用21000000，这里一致。

lim：每次最大最大铸造数量，上面使用100，这里一致。
