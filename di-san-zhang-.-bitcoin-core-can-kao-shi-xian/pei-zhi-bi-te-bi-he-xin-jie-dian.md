# 配置比特币核心节点

比特币核心在每次启动时都会在其数据目录中寻找配置文件。在本节中，我们将研究各种配置选项并设置一个配置文件。要查找配置文件，请在终端中运行bitcoind -printtoconsole，并查找前几行：

$ bitcoind -printtoconsole&#x20;

2023-01-28T03:21:42Z Bitcoin Core version v24.0.1&#x20;

2023-01-28T03:21:42Z Using the 'x86\_shani(1way,2way)' SHA256 implementation&#x20;

2023-01-28T03:21:42Z Using RdSeed as an additional entropy source&#x20;

2023-01-28T03:21:42Z Using RdRand as an additional entropy source&#x20;

2023-01-28T03:21:42Z Default data directory /home/harding/.bitcoin&#x20;

2023-01-28T03:21:42Z Using data directory /home/harding/.bitcoin&#x20;

2023-01-28T03:21:42Z Config file: /home/harding/.bitcoin/bitcoin.conf&#x20;

...&#x20;

\[a lot more debug output]&#x20;

...

\
你可以按 Ctrl-C 关闭节点，一旦确定配置文件的位置。通常，配置文件位于用户的主目录下的 .bitcoin 数据目录中。用你喜欢的编辑器打开配置文件。Bitcoin Core 提供了100多个配置选项，可以修改网络节点的行为、区块链的存储以及其操作的许多其他方面。要查看这些选项的列表，请运行 `bitcoind --help：`

$ bitcoind --help&#x20;

Bitcoin Core version v24.0.1

Usage: bitcoind \[options] Start Bitcoin Core&#x20;

Options:&#x20;

&#x20;   \-?&#x20;

&#x20;            Print this help message and exit&#x20;

\-alertnotify=\<cmd>

&#x20;            Execute command when an alert is raised (%s in cmd is replaced by message)&#x20;

...&#x20;

\[many more options]

以下是您可以在配置文件中设置的一些最重要的选项，或作为 bitcoind 的命令行参数：

alertnotify

&#x20;      运行指定的命令或脚本，向此节点的所有者发送紧急警报。

conf

&#x20;      配置文件的替代位置。这只有作为 bitcoind 的命令行参数才有意义，因为它不能在所指的配置文件内部。

datadir

&#x20;     选择存储所有区块链数据的目录和文件系统。默认情况下，这是您的主目录下的 .bitcoin 子目录。根据您的配置，到目前为止，这可能使用约 10 GB 到接近 1 TB 的空间，预计最大大小每年将增加数百 GB。

prune

&#x20;     通过删除旧的区块，将区块链磁盘空间要求减少到这么多兆字节。在资源受限的节点上使用此选项，无法容纳完整的区块链。系统的其他部分将使用其他磁盘空间，目前无法进行修剪，因此您仍然需要至少 datadir 选项中提到的最小空间量。\


txindex

&#x20;     维护所有交易的索引。这使您能够通过其ID以编程方式检索任何交易，前提是包含该交易的区块尚未被修剪。

dbcache

&#x20;     UTXO 缓存的大小。默认值为 450 Mebibytes（MiB）。在高端硬件上增加此大小，以减少磁盘读写次数，或者在低端硬件上减小大小，以节省内存，但会增加磁盘的使用频率。

blocksonly

&#x20;    通过仅接受经过确认的交易的区块，而不是中继未经确认的交易，来最大限度地减少带宽使用。

maxmempool

&#x20;    限制交易内存池到指定的兆字节数。这可用于减少内存受限节点上的内存使用。

{% hint style="info" %}
**交易数据库索引和txindex选项**

默认情况下，Bitcoin Core构建一个仅包含与用户钱包相关的交易的数据库。如果您想要能够使用诸如getrawtransaction（请参阅“探索和解码交易”）之类的命令访问任何交易，则需要配置Bitcoin Core以构建完整的交易索引，可以通过txindex选项实现。在Bitcoin Core配置文件中设置txindex=1。如果一开始没有设置此选项，而后来将其设置为完整索引，则需要等待其重建索引。
{% endhint %}

示例3-1  展示了如何将前面的选项与一个完全索引的节点结合起来，作为比特币应用程序的API后端运行。&#x20;

示例3-1。完全索引节点的示例配置

alertnotify=myemailscript.sh "Alert: %s"&#x20;

datadir=/lotsofspace/bitcoin&#x20;

txindex=1

示例3-2 展示了在较小服务器上运行的资源受限节点的示例配置。&#x20;

示例3-2。资源受限系统的示例配置

alertnotify=myemailscript.sh "Alert: %s"&#x20;

blocksonly=1&#x20;

prune=5000&#x20;

dbcache=150&#x20;

maxmempool=150\


在编辑配置文件并设置最符合您需求的选项后，您可以使用这个配置测试bitcoind。使用 printtoconsole 选项运行Bitcoin Core，以在前台输出到控制台：

$ bitcoind -printtoconsole&#x20;

2023-01-28T03:43:39Z Bitcoin Core version v24.0.1&#x20;

2023-01-28T03:43:39Z Using the 'x86\_shani(1way,2way)' SHA256 implementation&#x20;

2023-01-28T03:43:39Z Using RdSeed as an additional entropy source&#x20;

2023-01-28T03:43:39Z Using RdRand as an additional entropy source&#x20;

2023-01-28T03:43:39Z Default data directory /home/harding/.bitcoin&#x20;

2023-01-28T03:43:39Z Using data directory /lotsofspace/bitcoin&#x20;

2023-01-28T03:43:39Z Config file: /home/harding/.bitcoin/bitcoin.conf&#x20;

2023-01-28T03:43:39Z Config file arg: \[main] blockfilterindex="1"&#x20;

2023-01-28T03:43:39Z Config file arg: \[main] maxuploadtarget="1000"&#x20;

2023-01-28T03:43:39Z Config file arg: \[main] txindex="1"&#x20;

2023-01-28T03:43:39Z Setting file arg: wallet = \["msig0"]&#x20;

2023-01-28T03:43:39Z Command-line arg: printtoconsole=""&#x20;

2023-01-28T03:43:39Z Using at most 125 automatic connections&#x20;

2023-01-28T03:43:39Z Using 16 MiB out of 16 MiB requested for signature cache&#x20;

2023-01-28T03:43:39Z Using 16 MiB out of 16 MiB requested for script execution&#x20;

2023-01-28T03:43:39Z Script verification uses 3 additional threads&#x20;

2023-01-28T03:43:39Z scheduler thread start&#x20;

2023-01-28T03:43:39Z \[http] creating work queue of depth 16&#x20;

2023-01-28T03:43:39Z Using random cookie authentication.&#x20;

2023-01-28T03:43:39Z Generated RPC cookie /lotsofspace/bitcoin/.cookie&#x20;

2023-01-28T03:43:39Z \[http] starting 4 worker threads&#x20;

2023-01-28T03:43:39Z Using wallet directory /lotsofspace/bitcoin/wallets&#x20;

2023-01-28T03:43:39Z init message: Verifying wallet(s)…&#x20;

2023-01-28T03:43:39Z Using BerkeleyDB version Berkeley DB 4.8.30&#x20;

2023-01-28T03:43:39Z Using /16 prefix for IP bucketing&#x20;

2023-01-28T03:43:39Z init message: Loading P2P addresses…&#x20;

2023-01-28T03:43:39Z Loaded 63866 addresses from peers.dat 114ms&#x20;

\[... more startup messages ...]

\
您可以在满意加载了正确设置并且运行如您所期望的情况下，按下 Ctrl-C 来中断该过程。

要将Bitcoin Core作为后台进程运行，请使用守护进程选项启动它，例如 `bitcoind -daemon`。

要监视您的Bitcoin节点的进度和运行时状态，请以守护进程模式启动它，然后使用命令 `bitcoin-cli getblockchaininfo`。

$ bitcoin-cli getblockchaininfo

```json
{
	"chain": "main",
	"blocks": 0,
	"headers": 83999,
	"bestblockhash": "[...]19d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
	"difficulty": 1,
	"time": 1673379796,
	"mediantime": 1231006505,
	"verificationprogress": 3.783041623201835e-09,
	"initialblockdownload": true,
	"chainwork": "[...]000000000000000000000000000000000000000000000100010001",
	"size_on_disk": 89087,
	"pruned": false,
	"warnings": ""
}
```

这显示了一个区块链高度为0个区块和83,999个头部的节点。节点首先从其对等节点获取块头，以找到具有最多工作量证明的区块链，然后继续下载完整的块，并在此过程中进行验证。

一旦您对所选择的配置选项感到满意，您应该将Bitcoin Core添加到操作系统的启动脚本中，以便它持续运行，并在操作系统重新启动时重新启动。您会在Bitcoin Core的源目录中的contrib/init下找到各种操作系统的示例启动脚本，以及一个README.md文件，显示哪个系统使用哪个脚本。

\
\
\






\
