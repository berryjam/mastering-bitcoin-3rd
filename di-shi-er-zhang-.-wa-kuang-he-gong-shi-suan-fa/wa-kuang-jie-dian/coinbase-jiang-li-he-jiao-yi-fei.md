# Coinbase奖励和交易费

为构建coinbase交易，Jing的节点首先计算交易费的总额：

<pre><code><strong>Total Fees = Sum(Inputs) − Sum(Outputs)
</strong></code></pre>

接下来，Jing的节点计算新区块的正确奖励。奖励是根据区块高度计算的，从每个区块的50比特币开始，每210,000个区块减半一次。

可以在比特币核心客户端中的GetBlockSubsidy函数中看到计算方式，如示例12-3所示。

\
示例 12-3. 计算区块奖励 —— 函数 GetBlockSubsidy，比特币核心客户端，main.cpp

<pre class="language-cpp"><code class="lang-cpp">CAmount GetBlockSubsidy(int nHeight, const Consensus::Params&#x26; consensusParams) 
{
    int halvings = nHeight / consensusParams.nSubsidyHalvingInterval;
    // Force block reward to zero when right shift is undefined.
    if (halvings >= 64)
        return 0;
    CAmount nSubsidy = 50 * COIN;
    // Subsidy is cut in half every 210,000 blocks.
<strong>    nSubsidy >>= halvings;
</strong>    return nSubsidy; 
}
</code></pre>

\
初始补贴以 satoshi 为单位计算，将 50 乘以 COIN 常量（100,000,000 satoshi）。这将初始奖励（nSubsidy）设置为 50 亿 satoshi。

接下来，该函数通过当前区块高度除以减半间隔（SubsidyHalvingInterval）来计算已发生的减半次数。

然后，函数使用二进制右移操作符，在每次减半中将奖励（nSubsidy）除以二。对于区块 277,316，这将使 50 亿 satoshi 的奖励右移一次（一次减半），结果为 25 亿 satoshi，或 25 个比特币。经过第 33 次减半后，奖励将被舍入为零。使用二进制右移操作符是因为它比多次重复的除法更有效。为了避免潜在的错误，当进行了 63 次减半后，将跳过移位操作，并将补贴设置为 0。

最后，将 coinbase 奖励（nSubsidy）与交易费用（nFees）相加，并返回总和。

{% hint style="info" %}
如果 Jing 的挖矿节点编写 coinbase 交易，是什么阻止了 Jing “奖励”自己 100 或 1,000 个比特币？答案是，夸大的奖励将导致其他所有人都认为该区块无效，从而浪费了 Jing 用于 PoW 的电力。只有在所有人接受该区块时，Jing 才能花费奖励。
{% endhint %}
