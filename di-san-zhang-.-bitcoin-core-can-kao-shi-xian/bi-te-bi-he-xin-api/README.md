# 比特币核心 API

比特币核心 API 提供了一组命令，用于通过编程方式与运行中的比特币核心节点进行交互。这些命令可以通过 JSON-RPC 接口或使用 `bitcoin-cli` 命令行工具访问。以下是比特币核心 API 中常见的一些命令：

$ bitcoin-cli help&#x20;

\+== Blockchain ==&#x20;

getbestblockhash&#x20;

getblock "blockhash" ( verbosity )&#x20;

getblockchaininfo&#x20;

...&#x20;

walletpassphrase "passphrase" timeout&#x20;

walletpassphrasechange "oldpassphrase" "newpassphrase"&#x20;

walletprocesspsbt "psbt" ( sign "sighashtype" bip32derivs finalize )

每个命令都可以接受多个参数。要获取更多帮助、详细描述以及有关参数的信息，请在 `help` 后面添加命令名称。例如，要查看关于 `getblockhash` RPC 命令的帮助：

$ bitcoin-cli help getblockhash

getblockhash height

Returns hash of block in best-block-chain at height provided.&#x20;

Arguments:

1. height (numeric, required) The height index&#x20;

Result: "hex" (string) The block hash&#x20;

Examples:

\>bitcoin-cli getblockhash 1000

\> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id": "curltest",&#x20;

"method": "getblockhash",&#x20;

"params": \[1000]}' -H 'content-type: text/plain;' http://127.0.0.1:8332/

在帮助信息的末尾，你会看到两个RPC命令的示例，使用了bitcoin-cli助手或HTTP客户端curl。这些示例演示了如何调用该命令。复制第一个示例并查看结果：

$ bitcoin-cli getblockhash 1000 00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09

结果是一个区块哈希，在接下来的章节中将会详细介绍。但是目前，该命令应该在你的系统上返回相同的结果，表明你的Bitcoin Core节点正在运行，接受命令，并且有关于区块 1,000 的信息返回给你。&#x20;

在接下来的章节中，我们将演示一些非常有用的RPC命令及其预期的输出。\
