# 配置比特币核心构建

源代码包括文档，可以在许多文件中找到。查看位于bitcoin目录中的README.md中的主要文档。在本章中，我们将在Linux上构建比特币核心守护进程（服务器），也称为bitcoind（类Unix系统）。通过阅读doc/build-unix.md上的指南来审阅有关在您的平台上编译bitcoind命令行客户端的说明。备用说明可在doc目录中找到；例如，Windows说明可在build-windows.md中找到。截至撰写本文时，Android、FreeBSD、NetBSD、OpenBSD、macOS（OSX）、Unix和Windows的说明均可用。

仔细查看构建文档的第一部分，其中包含构建先决条件。这些是必须在您的系统上存在的库，然后您才能开始编译比特币。如果这些先决条件缺失，构建过程将失败并显示错误。如果由于您遗漏了某些先决条件而导致此问题，则可以安装它，然后从中断处恢复构建过程。假设已安装了先决条件，则可以通过使用autogen.sh脚本生成一组构建脚本来启动构建过程：

\
$ ./autogen.sh&#x20;

libtoolize: putting auxiliary files in AC\_CONFIG\_AUX\_DIR, 'build-aux'.&#x20;

libtoolize: copying file 'build-aux/ltmain.sh'&#x20;

libtoolize: putting macros in AC\_CONFIG\_MACRO\_DIRS, 'build-aux/m4'.&#x20;

...&#x20;

configure.ac:58: installing 'build-aux/missing'&#x20;

src/Makefile.am: installing 'build-aux/depcomp'&#x20;

parallel-tests: installing 'build-aux/test-driver'

autogen.sh脚本创建一组自动配置脚本，将查询您的系统以发现正确的设置，并确保您具有编译代码所需的所有必要库。其中最重要的是configure脚本，它提供了许多不同的选项来定制构建过程。使用--help标志查看各种选项：

$ ./configure --help&#x20;

\`configure' configures Bitcoin Core 24.0.1 to adapt to many kinds of systems.&#x20;

Usage: ./configure \[OPTION]... \[VAR=VALUE]...&#x20;

...&#x20;

Optional Features:

&#x20;  \--disable-option-checking ignore unrecognized --enable/--with options&#x20;

&#x20;  \--disable-FEATURE do not include FEATURE (same as --enable-FEATURE=no)

&#x20;  \--enable-FEATURE\[=ARG] include FEATURE \[ARG=yes]&#x20;

&#x20;  \--enable-silent-rules less verbose build output (undo: "make V=1")&#x20;

&#x20;  \--disable-silent-rules verbose build output (undo: "make V=0")&#x20;

...

configure脚本允许您通过--enable-FEATURE和--disable-FEATURE标志启用或禁用bitcoind的某些功能，其中FEATURE被替换为功能名称，如帮助输出中所列。在本章中，我们将使用所有默认功能构建bitcoind客户端。我们不会使用配置标志，但您应该查看它们以了解客户端的可选功能。如果您处于学术环境中，计算机实验室的限制可能要求您在您的主目录中安装应用程序（例如，使用--prefix=$HOME）。

以下是一些有用的选项，可以覆盖configure脚本的默认行为：

\--prefix=$HOME

这将覆盖生成的可执行文件的默认安装位置（默认为/usr/local/）。使用$HOME将所有内容放在您的主目录中，或者使用其他路径。

\--disable-wallet

这用于禁用参考钱包实现。

\--with-incompatible-bdb

如果要构建钱包，则允许使用不兼容版本的 Berkeley DB 库。

\--with-gui=no

不构建图形用户界面，这需要 Qt 库。这将仅构建服务器和命令行 Bitcoin Core。

\
接下来，运行配置脚本，自动发现所有必要的库，并为您的系统创建一个定制的构建脚本：

\
$ ./configure&#x20;

checking for pkg-config... /usr/bin/pkg-config&#x20;

checking pkg-config is at least version 0.9.0... yes&#x20;

checking build system type... x86\_64-pc-linux-gnu&#x20;

checking host system type... x86\_64-pc-linux-gnu checking for a BSD-compatible install... /usr/bin/install -c&#x20;

...&#x20;

\[many pages of configuration tests follow]&#x20;

...

如果一切顺利，configure命令将结束，并创建定制的构建脚本，使我们能够编译bitcoind。如果存在任何缺少的库或错误，configure命令将以错误而不是创建构建脚本结束。如果出现错误，这很可能是由于缺少或不兼容的库引起的。再次查看构建文档，确保安装了缺少的先决条件，然后重新运行configure，看看是否解决了错误。\
\


