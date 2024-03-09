# 选择比特币核心版本

默认情况下，本地副本将与最新的代码同步，这可能是比特币的一个不稳定或测试版本。在编译代码之前，请通过检出一个发布标签来选择一个特定版本。这将会将本地副本与代码存储库的特定快照同步，该快照由关键标签标识。标签被开发人员用于按版本号标记代码的特定发布。首先，要查找可用的标签，我们使用git tag命令：

\
$ git tag&#x20;

v0.1.5&#x20;

v0.1.6test1&#x20;

v0.10.0&#x20;

...&#x20;

v0.11.2&#x20;

v0.11.2rc1&#x20;

v0.12.0rc1&#x20;

v0.12.0rc2&#x20;

...

标签列表显示了所有已发布的比特币版本。按照惯例，用于测试的预发布候选版本后缀为“rc”。可以在生产系统上运行的稳定版本没有后缀。从上述列表中选择最高版本的发布版本，在撰写本文时为v24.0.1。要将本地代码与此版本同步，请使用git checkout命令：

$ git checkout v24.0.1&#x20;

Note: switching to 'v24.0.1'.&#x20;

You are in 'detached HEAD' state. You can look around, make experimental changes and commit them, and you can discard any commits you make in this state without impacting any branches by switching back to a branch.&#x20;

HEAD is now at b3f866a8d Merge bitcoin/bitcoin#26647: 24.0.1 final changes

您可以通过输入git status命令来确认您已经“检出”了所需的版本：

HEAD detached at v24.0.1&#x20;

nothing to commit, working tree clean
