# 交易的独立验证

\
在第6章中，我们看到钱包软件通过收集UTXO（未使用的交易输出）、提供适当的身份验证数据，然后构建分配给新所有者的新输出来创建交易。然后，生成的交易被发送到比特币网络中的相邻节点，以便在整个比特币网络中传播。

然而，在将交易转发到其邻居之前，每个接收到交易的比特币节点都会首先验证该交易。这确保只有有效的交易才会在网络中传播，而无效的交易则会在首个遇到它们的节点处被丢弃。

每个节点都会根据长长的检查清单验证每个交易(可对比[tx\_check.cpp](https://github.com/bitcoin/bitcoin/blob/8f1185feec3efdb8d0e3f6b7d0aee67bbdc3d653/src/consensus/tx\_check.cpp#L11)的CheckTransaction、[validation.cpp](https://github.com/bitcoin/bitcoin/blob/8f1185feec3efdb8d0e3f6b7d0aee67bbdc3d653/src/validation.cpp#L2262)来分析)：

* 交易的语法和数据结构必须正确。
* 输入和输出列表都不为空。
* 交易的重量足够小，以便使其适合在一个区块中。
* 每个输出值以及总值必须在允许的值范围内（大于等于零，但不超过2100万比特币）。
* 锁定时间等于INT\_MAX，或者锁定时间和序列值符合锁定时间和BIP68规则。
* 交易中包含的签名操作（SIGOPS）的数量少于签名操作限制
* 花费的输出与内存池中的输出或主分支中未花费的输出匹配。&#x20;
* 对于每个输入，如果引用的输出交易是coinbase输出，则必须至少有COINBASE\_MATURITY（100）次确认。任何绝对或相对锁定时间也必须满足。节点可能在它们成熟之前转发交易到一个区块，因为如果包含在下一个区块中，它们就会成熟。&#x20;
* 如果输入值的总和小于输出值的总和，则拒绝。&#x20;
* 每个输入的脚本必须针对相应的输出脚本进行验证。&#x20;

请注意，这些条件随着时间的推移而改变，以添加新功能或解决新类型的拒绝服务攻击。

通过在收到每个交易并在传播之前进行独立验证，每个节点构建了一个有效但尚未确认的交易池，称为内存池或mempool。



tx\_check.cpp::CheckTransaction

```
bool CheckTransaction(const CTransaction& tx, TxValidationState& state)
{
    // 输入和输出列表都不为空。
    // Basic checks that don't depend on any context
    if (tx.vin.empty())
        return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-vin-empty");
    if (tx.vout.empty())
        return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-vout-empty");
    // 交易的重量足够小，以便使其适合在一个区块中。
    // Size limits (this doesn't take the witness into account, as that hasn't been checked for malleability)
    if (::GetSerializeSize(TX_NO_WITNESS(tx)) * WITNESS_SCALE_FACTOR > MAX_BLOCK_WEIGHT) {
        return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-oversize");
    }

    // 每个输出值以及总值必须在允许的值范围内（大于等于零，但不超过2100万比特币）。
    // Check for negative or overflow output values (see CVE-2010-5139)
    CAmount nValueOut = 0;
    for (const auto& txout : tx.vout)
    {
        if (txout.nValue < 0)
            return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-vout-negative");
        if (txout.nValue > MAX_MONEY)
            return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-vout-toolarge");
        nValueOut += txout.nValue;
        if (!MoneyRange(nValueOut))
            return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-txouttotal-toolarge");
    }

    // Check for duplicate inputs (see CVE-2018-17144)
    // While Consensus::CheckTxInputs does check if all inputs of a tx are available, and UpdateCoins marks all inputs
    // of a tx as spent, it does not check if the tx has duplicate inputs.
    // Failure to run this check will result in either a crash or an inflation bug, depending on the implementation of
    // the underlying coins database.
    std::set<COutPoint> vInOutPoints;
    for (const auto& txin : tx.vin) {
        if (!vInOutPoints.insert(txin.prevout).second)
            return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-inputs-duplicate");
    }

    if (tx.IsCoinBase())
    {
        if (tx.vin[0].scriptSig.size() < 2 || tx.vin[0].scriptSig.size() > 100)
            return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-cb-length");
    }
    else
    {
        for (const auto& txin : tx.vin)
            if (txin.prevout.IsNull())
                return state.Invalid(TxValidationResult::TX_CONSENSUS, "bad-txns-prevout-null");
    }

    return true;
}
```

validation.cpp::CheckBlock

```
bool CheckBlock(const CBlock& block, BlockValidationState& state, const Consensus::Params& consensusParams, bool fCheckPOW, bool fCheckMerkleRoot)
{
    // These are checks that are independent of context.

    if (block.fChecked)
        return true;

    // Check that the header is valid (particularly PoW).  This is mostly
    // redundant with the call in AcceptBlockHeader.
    if (!CheckBlockHeader(block, state, consensusParams, fCheckPOW))
        return false;

    // Signet only: check block solution
    if (consensusParams.signet_blocks && fCheckPOW && !CheckSignetBlockSolution(block, consensusParams)) {
        return state.Invalid(BlockValidationResult::BLOCK_CONSENSUS, "bad-signet-blksig", "signet block signature validation failure");
    }

    // Check the merkle root.
    if (fCheckMerkleRoot && !CheckMerkleRoot(block, state)) {
        return false;
    }

    // All potential-corruption validation must be done before we do any
    // transaction validation, as otherwise we may mark the header as invalid
    // because we receive the wrong transactions for it.
    // Note that witness malleability is checked in ContextualCheckBlock, so no
    // checks that use witness data may be performed here.

    // Size limits
    if (block.vtx.empty() || block.vtx.size() * WITNESS_SCALE_FACTOR > MAX_BLOCK_WEIGHT || ::GetSerializeSize(TX_NO_WITNESS(block)) * WITNESS_SCALE_FACTOR > MAX_BLOCK_WEIGHT)
        return state.Invalid(BlockValidationResult::BLOCK_CONSENSUS, "bad-blk-length", "size limits failed");

    // First transaction must be coinbase, the rest must not be
    if (block.vtx.empty() || !block.vtx[0]->IsCoinBase())
        return state.Invalid(BlockValidationResult::BLOCK_CONSENSUS, "bad-cb-missing", "first tx is not coinbase");
    for (unsigned int i = 1; i < block.vtx.size(); i++)
        if (block.vtx[i]->IsCoinBase())
            return state.Invalid(BlockValidationResult::BLOCK_CONSENSUS, "bad-cb-multiple", "more than one coinbase");

    // Check transactions
    // Must check for duplicate inputs (see CVE-2018-17144)
    for (const auto& tx : block.vtx) {
        TxValidationState tx_state;
        if (!CheckTransaction(*tx, tx_state)) {
            // CheckBlock() does context-free validation checks. The only
            // possible failures are consensus failures.
            assert(tx_state.GetResult() == TxValidationResult::TX_CONSENSUS);
            return state.Invalid(BlockValidationResult::BLOCK_CONSENSUS, tx_state.GetRejectReason(),
                                 strprintf("Transaction check failed (tx hash %s) %s", tx->GetHash().ToString(), tx_state.GetDebugMessage()));
        }
    }
    unsigned int nSigOps = 0;
    for (const auto& tx : block.vtx)
    {
        nSigOps += GetLegacySigOpCount(*tx);
    }
    if (nSigOps * WITNESS_SCALE_FACTOR > MAX_BLOCK_SIGOPS_COST)
        return state.Invalid(BlockValidationResult::BLOCK_CONSENSUS, "bad-blk-sigops", "out-of-bounds SigOpCount");

    if (fCheckPOW && fCheckMerkleRoot)
        block.fChecked = true;

    return true;
}
```
