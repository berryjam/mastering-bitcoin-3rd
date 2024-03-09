# 探索区块

探索区块与探索交易类似。然而，区块可以通过区块高度或区块哈希来引用。首先，让我们通过区块高度找到一个区块。我们使用getblockhash命令，该命令以区块高度作为参数，并返回该区块的区块头哈希：

$ bitcoin-cli getblockhash 123456

0000000000002917ed80650c6174aac8dfc46f5fe36480aaef682ff6cd83c3ca

现在我们知道了我们选择的区块的区块头哈希，我们可以查询该区块。我们使用getblock命令，并将区块哈希作为参数：

$ bitcoin-cli getblock 0000000000002917ed80650c6174aac8dfc46f5fe36480aaef682f\
f6cd83c3ca

```json
{
	"hash": "0000000000002917ed80650c6174aac8dfc46f5fe36480aaef682ff6cd83c3ca",
	"confirmations": 651742,
	"height": 123456,
	"version": 1,
	"versionHex": "00000001",
	"merkleroot": "0e60651a9934e8f0decd1c[...]48fca0cd1c84a21ddfde95033762d86c",
	"time": 1305200806,
	"mediantime": 1305197900,
	"nonce": 2436437219,
	"bits": "1a6a93b3",
	"difficulty": 157416.4018436489,
	"chainwork": "[...]00000000000000000000000000000000000000541788211ac227bc",
	"nTx": 13,
	"previousblockhash": "[...]60bc96a44724fd72daf9b92cf8ad00510b5224c6253ac40095",
	"nextblockhash": "[...]00129f5f02be247070bf7334d3753e4ddee502780c2acaecec6d66",
	"strippedsize": 4179,
	"size": 4179,
	"weight": 16716,
	"tx": [
		"5b75086dafeede555fc8f9a810d8b10df57c46f9f176ccc3dd8d2fa20edd685b",
		"e3d0425ab346dd5b76f44c222a4bb5d16640a4247050ef82462ab17e229c83b4",
		"137d247eca8b99dee58e1e9232014183a5c5a9e338001a0109df32794cdcc92e",
		"5fd167f7b8c417e59106ef5acfe181b09d71b8353a61a55a2f01aa266af5412d",
		"60925f1948b71f429d514ead7ae7391e0edf965bf5a60331398dae24c6964774",
		"d4d5fc1529487527e9873256934dfb1e4cdcb39f4c0509577ca19bfad6c5d28f",
		"7b29d65e5018c56a33652085dbb13f2df39a1a9942bfe1f7e78e97919a6bdea2",
		"0b89e120efd0a4674c127a76ff5f7590ca304e6a064fbc51adffbd7ce3a3deef",
		"603f2044da9656084174cfb5812feaf510f862d3addcf70cacce3dc55dab446e",
		"9a4ed892b43a4df916a7a1213b78e83cd83f5695f635d535c94b2b65ffb144d3",
		"dda726e3dad9504dce5098dfab5064ecd4a7650bfe854bb2606da3152b60e427",
		"e46ea8b4d68719b65ead930f07f1f3804cb3701014f8e6d76c4bdbc390893b94",
		"864a102aeedf53dd9b2baab4eeb898c5083fde6141113e0606b664c41fe15e1f"
	]
}
```

确认（confirmations）条目告诉我们这个区块的深度——有多少个区块是在其之上构建的，这表明改变该区块中任何交易的难度。高度告诉我们在该区块之前有多少个区块。我们看到了该区块的版本、创建时间（根据其矿工）、之前的11个区块的中位时间（对矿工来说更难以操纵的时间测量），以及区块的大小以三种不同的度量方式（其传统的剥离大小、完整大小和权重单位中的大小）。我们还看到了一些用于安全性和工作证明的字段（默克尔根、随机数、位、难度和链工作量）；我们将在第12章中对这些进行详细探讨。

\
