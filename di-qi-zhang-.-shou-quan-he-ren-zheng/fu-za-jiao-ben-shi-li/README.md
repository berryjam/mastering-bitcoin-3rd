# 复杂脚本示例

在本节中，我们将本章中的许多概念结合到一个示例中。

穆罕默德是迪拜的一家公司的所有者，经营着一家进出口公司；他希望建立一个具有灵活规则的公司资本账户。他创建的方案根据时间锁定需要不同级别的授权。多签名方案的参与者是穆罕默德，他的两个合作伙伴赛义德和扎伊拉，以及他们的公司律师。这三个合作伙伴根据多数原则做出决定，因此三个中的两个必须同意。但是，如果他们的密钥出现问题，他们希望他们的律师能够在三个合作伙伴签名中的任何一个的情况下恢复资金。最后，如果所有合作伙伴在一段时间内不可用或无能为力，他们希望律师在获得对资本账户的交易记录的访问权限后能够直接管理该账户。

示例 7-1 是穆罕默德设计的赎回脚本，以实现这一目标（行号已添加前缀）。

示例 7-1. 可变多重签名与时间锁定

```
01 OP_IF
02 OP_IF
03 2
04 OP_ELSE
05 <30 days> OP_CHECKSEQUENCEVERIFY OP_DROP
06 <Lawyer's Pubkey> OP_CHECKSIGVERIFY
07 1
08 OP_ENDIF
09 <Mohammed's Pubkey> <Saeed's Pubkey> <Zaira's Pubkey> 3 OP_CHECKMULTISIG
10 OP_ELSE
11 <90 days> OP_CHECKSEQUENCEVERIFY OP_DROP
12 <Lawyer's Pubkey> OP_CHECKSIG
13 OP_ENDIF
```

Mohammed的脚本使用嵌套的OP\_IF...OP\_ELSE流程控制子句实现了三条执行路径。

在第一条执行路径中，该脚本作为一个简单的2-of-3多重签名与三个合作伙伴一起操作。这个执行路径包括第3行和第9行。第3行将多重签名的法定人数设置为2（2-of-3）。可以通过在输入脚本末尾放置OP\_TRUE OP\_TRUE来选择此执行路径：

OP\_0 \<Mohammed's Sig> \<Zaira's Sig> OP\_TRUE OP\_TRUE

{% hint style="danger" %}
这个输入脚本开头的OP\_0是因为OP\_CHECKMULTISIG存在一个奇怪的特性，它会从栈中弹出一个额外的值。虽然OP\_CHECKMULTISIG会忽略这个额外的值，但它必须存在，否则脚本会失败。使用OP\_0推送一个空字节数组是对这个奇怪特性的一种变通方法，详情请参见第152页的“CHECKMULTISIG执行中的一个奇特现象”。
{% endhint %}

第二个执行路径只能在从UTXO创建起经过30天后才能使用。在那时，它需要律师的签名和三个合作伙伴中的一个签名（即1-of-3的多重签名）。这通过第7行实现，该行将多重签名的法定人数设置为1。要选择这个执行路径，输入脚本的结尾应为OP\_FALSE OP\_TRUE：

OP\_0 \<Saeed's Sig> \<Lawer's Sig> OP\_FALSE OP\_TRUE

{% hint style="danger" %}
为什么是 OP\_FALSE OP\_TRUE？这不是倒过来了吗？首先将 FALSE 推送到堆栈上，然后在其上方推送 TRUE。因此，第一个 OP\_IF 操作码首先弹出 TRUE。
{% endhint %}

最后，第三个执行路径允许律师独自花费资金，但只能在90天后。要选择此执行路径，输入脚本必须以 OP\_FALSE 结束：

\<Lawyer's Sig> OP\_FALSE

尝试在纸上运行脚本，看看它在堆栈上的行为。
