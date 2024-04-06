# 调整难度的重新定位

正如我们所见，目标确定了难度，因此影响了寻找解决方案的时间。这引出了一个显而易见的问题：为什么需要调整难度，谁来进行调整，以及如何进行调整呢？&#x20;

比特币的区块平均每 10 分钟产生一个。这是比特币的节拍，支撑着货币发行频率和交易结算速度。它不仅在短期内必须保持恒定，而且在数十年的时间跨度内也必须保持稳定。随着时间的推移，预计计算机算力将继续快速增长。此外，参与挖矿的参与者数量和他们使用的计算机也将不断变化。为了保持区块生成时间在 10 分钟左右，挖矿的难度必须进行调整，以适应这些变化。 实际上，工作证明目标是一个动态参数，定期调整以满足每 10 分钟一个区块的目标。简单来说，目标被设置为当前挖矿算力会产生 10 分钟一个区块的时间间隔。&#x20;

那么，在完全去中心化的网络中如何进行这样的调整呢？重新调整难度在每个节点上都会自动进行。每产生 2,016 个区块，所有节点都会重新调整工作证明。计算实际时间跨度与期望的每个区块 10 分钟时间跨度之间的比例，并对目标进行相应的调整（增加或减少）。简单来说：如果网络发现区块生成速度比每 10 分钟快，难度会增加（目标减少）。如果区块的发现速度比预期的慢，难度会减少（目标增加）。&#x20;

该方程可以总结为：&#x20;

新目标 = 旧目标 \*（上一个 2,015 个区块的实际时间 / 20,160 分钟 ） 【原翻译：New Target = Old Target \* (20,160 minutes / Actual Time of Last 2015 Blocks)， 个人认为是写错了，即新目标 = 旧目标 \*（ 20,160 分钟 / 上一个 2,015 个区块的实际时间 ），因为如果实际时间小，说明需要提升难度，即减少新目标的值。而且下面代码也是先乘以实际值再除以20160。】

{% hint style="info" %}
尽管每产生 2,016 个区块就进行一次目标校准，但由于比特币软件中的一个偏移错误，实际上是基于前 2,015 个区块的总时间（而不是应该的 2,016 个区块），导致难度朝更高方向偏差 0.05%。&#x20;
{% endhint %}

示例 12-5 展示了比特币核心客户端使用的代码。

示例 12-5. 调整工作证明目标：pow.cpp 中的 CalculateNextWorkRequired()

```cpp
// Limit adjustment step
int64_t nActualTimespan = pindexLast->GetBlockTime() - nFirstBlockTime;
LogPrintf(" nActualTimespan = %d before bounds\n", nActualTimespan);
if (nActualTimespan < params.nPowTargetTimespan/4)
    nActualTimespan = params.nPowTargetTimespan/4;
if (nActualTimespan > params.nPowTargetTimespan*4)
    nActualTimespan = params.nPowTargetTimespan*4;
// Retarget
const arith_uint256 bnPowLimit = UintToArith256(params.powLimit);
arith_uint256 bnNew;
arith_uint256 bnOld;
bnNew.SetCompact(pindexLast->nBits);
bnOld = bnNew;
bnNew *= nActualTimespan;
bnNew /= params.nPowTargetTimespan;

if (bnNew > bnPowLimit)
    bnNew = bnPowLimit;
```

\
为了避免难度的极端波动，每个周期内的重新调整幅度必须小于四倍（4）。如果所需的目标调整超过四倍，它将被调整为四倍，不会更多。任何进一步的调整将在下一个重新调整周期内完成，因为不平衡将持续到接下来的2,016个区块。因此，哈希功率和难度之间的巨大差异可能需要多个2,016个区块周期来平衡。

请注意，目标与交易数量或交易价值无关。这意味着用于保护比特币的哈希功率和因此消耗的电力完全独立于交易数量。比特币可以扩展并保持安全性，而无需从当前水平增加哈希功率。哈希功率的增加代表了市场力量，因为新的矿工进入市场。只要足够多的哈希功率由诚实的矿工控制以追求奖励，就足以防止“接管”攻击，因此足以保护比特币。

挖矿的难度与电力成本和比特币与用于支付电力的货币的汇率密切相关。高性能的挖矿系统在当前一代硅制造技术下尽可能高效，以最高速率将电力转换为哈希计算。对挖矿市场的主要影响是一千瓦时电力的价格与比特币之间的汇率，因为这决定了挖矿的盈利能力，从而影响了进入或退出挖矿市场的激励。
