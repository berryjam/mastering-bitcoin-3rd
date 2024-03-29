# 安全原则

比特币的核心原则是去中心化，这对安全性有重要影响。传统的银行或支付网络等集中化模型依赖于访问控制和审核来阻止不良行为者进入系统。相比之下，像比特币这样的去中心化系统将责任和控制权交给了用户。由于网络的安全性基于独立验证，因此比特币流量不需要加密（尽管加密仍然有用）。

在传统的支付网络（如信用卡系统）中，支付是开放式的，因为其中包含用户的私人标识符（信用卡号码）。在初始收费后，任何拥有该标识符的人都可以“拉取”资金并多次向所有者收费。因此，支付网络必须通过端到端加密进行安全保护，并确保在传输过程中或存储时（静态时）没有窃听者或中间人可以 compromise 支付流量。如果恶意行为者获得系统访问权，则他可以 compromise 当前的交易和可用于创建新交易的支付令牌。更糟糕的是，当客户数据遭到 compromise 时，客户会暴露于身份盗窃风险，并必须采取措施防止被盗账户被用于欺诈行为。

比特币与此截然不同。比特币交易仅授权特定金额给特定收款人，不能伪造。它不会透露任何私人信息，如交易各方的身份，并且不能用于授权额外的付款。因此，比特币支付网络不需要加密或受到窃听的保护。实际上，您可以通过开放的公共频道（如不安全的WiFi或蓝牙）广播比特币交易，而不会丧失安全性。

比特币的去中心化安全模型赋予用户很大的权力。随之而来的是保护他们密钥机密性的责任。对于大多数用户来说，这并不容易做到，特别是在像互联网连接的智能手机或笔记本电脑这样的通用计算设备上。尽管比特币的去中心化模型可以防止信用卡一样的大规模 compromise，但许多用户仍然无法充分保护好自己的密钥，并逐个遭受黑客攻击。
