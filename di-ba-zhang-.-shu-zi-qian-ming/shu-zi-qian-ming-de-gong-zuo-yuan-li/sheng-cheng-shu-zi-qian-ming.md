# 生成数字签名

在比特币中使用的数字签名算法中，被签名的“消息”是交易，或更准确地说是交易数据的特定子集的哈希值，称为承诺哈希（参见“签名哈希类型（SIGHASH）”第185页）。签名密钥是用户的私钥。结果是签名：

$$
Sig = F_{sig}(F_{hash}(m),x)
$$

其中：

* x 是签名的私钥
* m 是要签名的消息，即承诺哈希（例如交易的部分）
* Fhash 是哈希函数
* Fsig 是签名算法
* Sig 是生成的签名

您可以在“Schnorr Signatures”第187页和“ECDSA Signatures”第197页找到有关schnorr和ECDSA签名数学的更多详细信息。

在schnorr和ECDSA签名中，函数Fsig 生成一个由两个值组成的签名 Sig。这两个值在不同算法中存在差异，我们稍后会详细探讨。计算出这两个值后，它们被序列化成一个字节流。对于ECDSA签名，编码使用称为Distinguished Encoding Rules或DER的国际标准编码方案。对于schnorr签名，使用了更简单的序列化格式。
