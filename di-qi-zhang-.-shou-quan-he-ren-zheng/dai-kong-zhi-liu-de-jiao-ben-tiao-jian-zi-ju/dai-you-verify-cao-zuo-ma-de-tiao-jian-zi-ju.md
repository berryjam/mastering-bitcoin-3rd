# 带有VERIFY操作码的条件子句

另一种比特币脚本中的条件形式是以VERIFY结尾的任何操作码。VERIFY后缀意味着如果评估的条件不为TRUE，则脚本的执行立即终止，并将事务视为无效。

与提供替代执行路径的IF子句不同，VERIFY后缀充当了一个守卫子句，只有在满足前提条件时才继续执行。

例如，以下脚本要求Bob的签名和产生特定哈希的预图像（秘密）。只有满足这两个条件才能解锁：

OP\_HASH160 \<expected hash> OP\_EQUALVERIFY \<Bob's Pubkey> OP\_CHECKSIG

为了花费这笔交易，Bob必须提供一个有效的预影像和一个签名：

\<Bob's Sig> \<hash pre-image>\


没有提供预影像，Bob无法进入检查他签名的脚本部分。&#x20;

这个脚本也可以用OP\_IF来编写：

```
OP_HASH160 <expected hash> OP_EQUAL
OP_IF
 <Bob's Pubkey> OP_CHECKSIG
OP_ENDIF
```

Bob的身份验证数据是相同的：

\
\<Bob's Sig> \<hash pre-image>

使用OP\_IF的脚本与使用带有VERIFY后缀的操作码执行相同的操作；它们都作为守卫子句运行。然而，VERIFY的构造更高效，使用了两个较少的操作码。&#x20;

那么，我们什么时候使用VERIFY，什么时候使用OP\_IF呢？如果我们只是想要附加一个前提条件（守卫子句），那么VERIFY更好。然而，如果我们想要有多个执行路径（流程控制），那么我们需要一个OP\_IF…OP\_ELSE的流程控制子句。
