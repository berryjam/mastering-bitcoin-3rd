# 哈希时间锁合约（Hash Time Lock Contracts -HTLC）

\
支付通道可以通过一种特殊的智能合约进一步扩展，该合约允许参与者将资金锁定到一个可赎回的秘密，并设置一个到期时间。这个特性被称为哈希时间锁合约，简称HTLC，它被用于双向和路由的支付通道。

首先解释一下HTLC中的“哈希”部分。要创建一个HTLC，支付的预期接收者首先会生成一个秘密R。然后，他们计算这个秘密的哈希H：

```
H = Hash(R)
```

\
这产生了一个哈希H，可以包含在输出的脚本中。谁知道这个秘密，就可以用它来赎回输出。这个秘密R也被称为哈希函数的原像。原像只是作为哈希函数输入的数据。

HTLC的第二部分是“时间锁”组件。如果秘密没有被揭示，支付HTLC的一方可以在一段时间后获得“退款”。这是通过使用CHECKLOCKTIMEVERIFY实现的绝对时间锁。

实施HTLC的脚本可能如下所示：

```
IF
     # Payment if you have the secret R
     HASH160 <H> EQUALVERIFY
     <Receiver Public Key> CHECKSIG
ELSE
     # Refund after timeout.
     <lock time> CHECKLOCKTIMEVERIFY DROP
     <Payer Public Key> CHECKSIG
ENDIF
```

任何知道秘密R的人，当其哈希等于H时，都可以通过执行IF流程的第一条子句来赎回此输出。&#x20;

如果秘密没有被揭示，并且在一定数量的区块之后HTLC被要求，支付方可以使用IF流程中的第二个子句来要求退款。&#x20;

这是HTLC的一个基本实现。这种类型的HTLC可以被任何知道秘密R的人兑现。HTLC可以采取许多不同的形式，脚本略有变化。例如，通过在第一条子句中添加CHECKSIG运算符和一个公钥，可以将哈希的兑现限制为特定的接收方，后者也必须知道秘密R。
