## 伪目标的介绍
- [x] “伪目标”并不是一个文件，只是一个标签;
- [x]  make无法生成它的依赖关系和决定它是否要执行。因此make是默认不执行伪目标的，除非你显示指明它才生效；
- [x]  伪目标的取名不能和文件名重名，不然其就失去了“伪目标”的意义了。

## 举例说明
让我们先看看Makefile文件:
```bashrc
.PHONY: premake precompiling Compiling release 

premake:
	echo "premake"

precompiling: premake
	echo "precompiling"

Compiling: precompiling
	echo "Compiling"

release: Compiling
	echo "release"
```
当我们默认执行它的时候
```bashrc
$ make
echo "premake"
premake
```
发现居然执行了第一个标签，但是按道理来说，应该是什么都不执行才对。这是因为make永远会执行Makefile里的第一个命令(通常是终极目标)。如果我们显示地指定第二个命令，结果为：
```bashrc
$ make precompiling
echo "premake"
premake
echo "precompiling"
precompiling
```
这是因为在执行第二个命令时对第一个命令有依赖，所以也执行了第一个命令。

## 去掉.PHONY
那假如去掉伪命令标识符呢，Makefile内容如下:
```bashrc
# .PHONY: premake precompiling Compiling release 

premake:
	echo "premake"

precompiling: premake
	echo "precompiling"

Compiling: precompiling
	echo "Compiling"

release: Compiling
	echo "release"
```
然后执行:
```
$ make
echo "premake"
premake
```
结果依然是只执行了第一个命令，这是因为第一个命令没有任何依赖。假如将Makefile换成如下内容:
```bashrc
# .PHONY: premake precompiling Compiling release 

release: Compiling
	echo "release"

premake:
	echo "premake"

Compiling: precompiling
	echo "Compiling"

precompiling: premake
	echo "precompiling"
```
然后执行
```
$ make
echo "premake"
premake
echo "precompiling"
precompiling
echo "Compiling"
Compiling
echo "release"
release
```
这是候全部执行了，这是因为其他三个命令对第一个都有依赖，并且他们的位置顺序可以不是执行顺序。对此，我们得出结论：**输出终极目标的命令应该放在首位，其他命令可以没有顺序**
