# 编译比特币核心的源代码

比特币核心的源代码可以通过下载存档文件或从GitHub克隆源代码存储库来获取。在比特币核心下载页面上，选择最新版本并下载源代码的压缩存档。或者，使用Git命令行从GitHub的比特币页面创建源代码的本地副本。&#x20;

{% hint style="info" %}
在本章的许多示例中，我们将使用操作系统的命令行界面（也称为“shell”），通过“终端”应用程序访问。Shell会显示一个提示符，您输入一个命令，Shell会用一些文本和一个新的提示符来回应您的下一个命令。提示符在您的系统上可能看起来不同，但在以下示例中，它用$符号表示。在示例中，当您看到$符号后面的文本时，不要输入$符号，而是直接输入紧随其后的命令，然后按Enter执行该命令。在示例中，每个命令下面的行是操作系统对该命令的响应。当您看到下一个$前缀时，您会知道这是一个新命令，您应该重复这个过程。&#x20;
{% endhint %}

这里，我们使用git命令创建源代码的本地副本（“克隆”）：

```shell
$git clone https://github.com/bitcoin/bitcoin.git&#x20;

Cloning into 'bitcoin'...&#x20;

remote: Enumerating objects: 245912, done.&#x20;

remote: Counting objects: 100% (3/3), done.&#x20;

remote: Compressing objects: 100% (2/2), done.&#x20;

remote: Total 245912 (delta 1), reused 2 (delta 1), pack-reused 245909

Receiving objects: 100% (245912/245912), 217.74 MiB | 13.05 MiB/s, done.&#x20;

Resolving deltas: 100% (175649/175649), done.
```

{% hint style="info" %}
Git是最广泛使用的分布式版本控制系统，是任何软件开发人员工具包的必备部分。如果您尚未安装git命令或Git的图形用户界面，则可能需要在您的操作系统上安装它。
{% endhint %}

&#x20;当Git克隆操作完成后，您将在名为bitcoin的目录中拥有完整的源代码存储库的本地副本。使用cd命令切换到此目录：

$cd bitcoin
