# BTC二层网络Stacks介绍及代码分析

随着2024年初BTC的大热，各种BTC二层网络如雨后春笋般出现。在个人博客里[《BTC Layer2的3种方案（转载+翻译）》](https://berryjam.github.io/2024/02/\(%E8%BD%AC%E8%BD%BD+%E7%BF%BB%E8%AF%91\)BTC-Layer2%E6%96%B9%E6%A1%88%E6%B1%87%E6%80%BB/)，对当前火热的三个项目：**B²、Merlin、BEVM**进行了初步介绍**。**其中B²、BEVM实现原理是类似ethereum的ZK-Rollup的扩容方案，但局限于比特币脚本并不是图灵完备，实现上挑战还是比较高的。而Merlin是基于质押BTC的方式，质押节点是由Merlin指定的，不够去中心化。

接下来要介绍的Stacks与Merlin类似，也是基于质押的方式，但是任何人都能成为Stacker，实现去中心化。并且通过“链锚定”的方式，利用BTC主链的**PoW**来保护Stacks子链的安全性，同时引入microblock、anchorblock机制来实现交易的快速确认，以此实现扩容。

