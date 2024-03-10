# 确定性密钥生成

当给定相同的输入时，哈希函数总是会产生相同的输出，但是如果输入稍有改变，输出将会不同。如果函数是加密安全的，那么没有人应该能够预测新的输出，即使他们知道新的输入。

这使我们能够将一个随机值转换为几乎无限数量的看似随机值。更有用的是，稍后使用相同的哈希函数和相同的输入（称为种子）将产生相同的看似随机值：

```sh
# Collect some entropy (randomness)
$ dd if=/dev/random count=1 status=none | sha256sum
f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73 -
# Set our seed to the random value
$ seed=f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73
# Deterministically generate derived values
$ for i in {0..2} ; do echo "$seed + $i" | sha256sum ; done
50b18e0bd9508310b8f699bad425efdf67d668cb2462b909fdb6b9bd2437beb3 -
a965dbcd901a9e3d66af11759e64a58d0ed5c6863e901dfda43adcd5f8c744f3 -
19580c97eb9048599f069472744e51ab2213f687d4720b0efc5bb344d624c3aa -
```

如果我们将这些派生的值用作我们的私钥，那么稍后我们可以使用之前使用的算法和我们的种子值生成完全相同的私钥。使用确定性密钥生成的用户可以通过简单地记录他们的种子和他们使用的确定性算法的引用来备份他们钱包中的每个密钥。例如，即使Alice有一百万个比特币分别存放在一百万个不同的地址中，她只需要备份以下内容，以便稍后恢复对这些比特币的访问：

f1cc 3bc0 3ef5 1cb4 3ee7 8444 60fa 5049&#x20;

e779 e742 5a63 49c8 e89d fbb0 fd97 bb73

基本顺序确定性密钥生成的逻辑图如图5-2所示。然而，现代钱包应用程序有一种更聪明的方法来实现这一点，允许公钥与其相应的私钥分别派生，从而使得私钥比公钥更安全地存储成为可能。

<figure><img src="../../.gitbook/assets/5.2.png" alt=""><figcaption><p>图 5-2. 确定性密钥生成：从钱包数据库的种子派生出的确定性密钥序列。</p></figcaption></figure>

