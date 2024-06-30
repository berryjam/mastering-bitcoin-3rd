# BTC二层网络Stacks介绍及代码分析

随着2024年初BTC的大热，各种BTC二层网络如雨后春笋般出现。在个人博客里[《BTC Layer2的3种方案（转载+翻译）》](https://berryjam.github.io/2024/02/\(%E8%BD%AC%E8%BD%BD+%E7%BF%BB%E8%AF%91\)BTC-Layer2%E6%96%B9%E6%A1%88%E6%B1%87%E6%80%BB/)，对当前火热的三个项目：**B²、Merlin、BEVM**进行了初步介绍**。**其中B²、BEVM实现原理是类似ethereum的ZK-Rollup的扩容方案，但局限于比特币脚本并不是图灵完备，实现上挑战还是比较高的。而Merlin是基于质押BTC的方式，质押节点是由Merlin指定的，不够去中心化。

接下来要介绍的Stacks与Merlin类似，也是基于质押的方式，但是任何人都能成为Stacker，实现去中心化。并且通过“链锚定”的方式，利用BTC主链的**PoW**来保护Stacks子链的安全性，同时引入microblock、anchorblock机制来实现交易的快速确认，以此实现扩容。

下面将对如何启动Stacks、Stacker节点和代码进行具体介绍。还有对整体架构以及其中不同组件：区块生成、交易处理、共识机制、与比特币交互、Clarity智能合约进行分析。

## 1.启动Stacks节点

Stacks支持以不同网络模式启动节点，如果想完整的运行Stacks节点并加入已有网络进行挖矿的话，可以参考《[Stacks Blockchain Miner](https://gist.github.com/wileyj/26cc0a3daf55c9b70d30301e9e4200f2)》。如果是基于Stacks进行开发或者调试，可以选择mocknet。这样并不需要启动比特币节点，能够快速把Stacks节点运行起来。下面是启动mocknet模式Stacks节点的流程：\




### 1.1 下载代码

```
git clone git@github.com:stacks-network/stacks-core.git
```

### 1.2 生成节点私钥

请将下面输出保存到安全地方

```
$ cd $HOME && npm install @stacks/cli shx rimraf
$ npx @stacks/cli make_keychain 2>/dev/null | jq
{
  "mnemonic": "frown lens very suit ocean trigger animal flip retire dose various mobile record emerge torch client sorry shy party session until planet member exclude",
  "keyInfo": {
    "privateKey": "ooxeemeitar4ahw0ca8anu4thae7aephahshae1pahtae5oocahthahho4ahn7eici",
    "address": "STTXOG3AIHOHNAEH5AU6IEX9OOTOH8SEIWEI5IJ9",
    "btcAddress": "Ook6goo1Jee5ZuPualeiqu9RiN8wooshoo",
    "wif": "rohCie2ein2chaed9kaiyoo6zo1aeQu1yae4phooShov2oosh4ox",
    "index": 0
  }
}
```

上面mnemonic是助记词，privateKey是私钥，address是stx的地址，btcAddress是对应的比特币地址，wif(wallet import format)是可导入比特币钱包格式的私钥。





## 2.启动Stacks Signer





## 3.整体架构及代码分析







