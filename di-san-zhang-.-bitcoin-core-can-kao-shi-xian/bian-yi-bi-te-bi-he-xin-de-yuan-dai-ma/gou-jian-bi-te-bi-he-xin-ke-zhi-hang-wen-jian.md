# 构建比特币核心可执行文件

下一步，您将编译源代码，这个过程可能需要长达一小时才能完成，具体取决于您的CPU速度和可用内存。如果出现错误或编译过程中断，可以随时通过再次键入 make 来恢复。输入 make 开始编译可执行应用程序：

$ make&#x20;

Making all in src&#x20;

CXX bitcoind-bitcoind.o&#x20;

CXX libbitcoin\_node\_a-addrdb.o&#x20;

CXX libbitcoin\_node\_a-addrman.o

CXX libbitcoin\_node\_a-banman.o&#x20;

CXX libbitcoin\_node\_a-blockencodings.o&#x20;

CXX libbitcoin\_node\_a-blockfilter.o&#x20;

\[... many more compilation messages follow ...]\
\
在性能较快且具有多个CPU的系统上，您可能希望设置并行编译作业的数量。例如，`make -j 2` 将使用两个可用的核心。如果一切顺利，比特币核心现在已经编译完成。您应该使用 `make check` 运行单元测试套件，以确保链接的库没有明显的问题。最后一步是使用 `make install` 命令在您的系统上安装各种可执行文件。由于此步骤需要管理员权限，因此您可能需要输入您的用户密码：

$ make check && sudo make install&#x20;

Password:&#x20;

Making install in src&#x20;

../build-aux/install-sh -c -d '/usr/local/lib'&#x20;

libtool: install: /usr/bin/install -c bitcoind /usr/local/bin/bitcoind&#x20;

libtool: install: /usr/bin/install -c bitcoin-cli /usr/local/bin/bitcoin-cli&#x20;

libtool: install: /usr/bin/install -c bitcoin-tx /usr/local/bin/bitcoin-tx&#x20;

...

默认情况下，bitcoind 的安装位置是 `/usr/local/bin`。您可以通过询问系统执行文件的路径来确认 Bitcoin Core 是否正确安装，方法如下：

$ which bitcoind&#x20;

/usr/local/bin/bitcoind&#x20;

$ which bitcoin-cli&#x20;

/usr/local/bin/bitcoin-cli
