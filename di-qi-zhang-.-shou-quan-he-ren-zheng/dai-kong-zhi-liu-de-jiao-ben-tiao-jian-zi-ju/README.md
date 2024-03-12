# 带控制流的脚本（条件子句）

比特币脚本中的一个更强大的特性是流程控制，也称为条件子句。你可能熟悉使用IF...THEN...ELSE构造的各种编程语言中的流程控制。比特币的条件子句看起来有些不同，但实质上是相同的构造。

在基本层面上，比特币的条件操作码允许我们构造一个脚本，根据逻辑条件的TRUE/FALSE结果有两种解锁方式。例如，如果x为TRUE，则执行代码路径为A，否则执行代码路径为B。

此外，比特币的条件表达式可以“嵌套”无限，意味着一个条件子句可以包含另一个条件子句，后者又包含另一个条件子句，以此类推。比特币脚本流程控制可用于构造具有数百种可能执行路径的非常复杂的脚本。嵌套没有限制，但共识规则对脚本的最大字节大小施加了限制。

比特币使用OP\_IF、OP\_ELSE、OP\_ENDIF和OP\_NOTIF操作码实现流程控制。此外，条件表达式可以包含布尔运算符，如OP\_BOOLAND、OP\_BOOLOR和OP\_NOT。

乍一看，你可能会觉得比特币的流程控制脚本很令人困惑。这是因为比特币脚本是一种栈语言。就像1 + 1被表达为1 1 OP\_ADD一样“向后”，在比特币中的流程控制子句也看起来“向后”。

在大多数传统（过程式）编程语言中，流程控制看起来像这样：

```
if (condition):
 code to run when condition is true
else:
 code to run when condition is false
endif
code to run in either case
```

在像比特币脚本这样的基于栈的语言中，逻辑条件位于IF之前，这使得它看起来“向后”：

```
condition
IF
 code to run when condition is true
OP_ELSE
 code to run when condition is false
OP_ENDIF
code to run in either case
```

在阅读比特币脚本时，请记住正在评估的条件出现在IF操作码之前。
