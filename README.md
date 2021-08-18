# TypingCodingResearch

## Problems

由于不同汉字的使用频率和输入方式不同，使用全拼输入法撰写文章时，26 个字母键盘的使用频率并不均衡。

评价使用全拼时 26 字母按键的均衡性和输入效率，并尝试设计一种新的拼写编码方法，使得输入同样文章时按键使用更加均衡、输入更加高效。

## Presupposition

为了简化问题方便分析，预先做以下分析与假设：

忽略使用全拼输入法时的多种分词对应关系，如“xinan”可以对应“西南”或“新安”。也可以理解为一次只打一个字。

忽略使用键盘过程中相邻两个按键距离对输入效率的影响。

对于键盘配列的相关问题，在标准 QWERTY 键盘中，按照大部分人的使用习惯，手指常态下应该放在中排，即字母区域的 “ASDFJKL” 七个键周围。而这七个键的使用频率并不都是最高的，所以要想实现更好的打字效果往往需要更改键盘配列，需要把最常用的字母放在上述七个键的位置（实际中的特殊配列一般会将分号位置也改为字母，在此不考虑），以使手指移动距离最短；而其他字母的热力图应均匀分布，以避免局部重复使用引起疲劳。

在对全拼输入的优化上遵循的原则是重新编码前后符号能够一一对应，即通过拼音可以确定唯一的重编码拼音，反之亦然。同时应方便记忆。即不改变大部分字母的对应关系，修改后的编码长度要短、重码率要低、字根分布均匀。

## Definition

本部分对于一些模糊性的概念进行量化定义，以便于方案优化与对比。

### 均衡性

定义使用全拼输入法撰写一篇文章的过程中，使用键盘输入中文的均衡度为各字母按键使用频率的样本标准差，即：

![](https://latex.codecogs.com/svg.image?B=\sqrt{\frac{\sum_{i=1}^{n}{(p_i&space;-&space;\overline{p})^2}}{n-1}})

其中 $n=26$ 为英文字母数量，$p_i$ 为每个英文字母出现的频率，$\overline{p}$ 为平均频率。

若考虑重新配列，即简单的取使用频率最高的七个键放置在高频使用区域，其他按键划分为另一个区域，则：

![](https://latex.codecogs.com/svg.image?B_r=\sqrt{\frac{\sum_{i=1}^{n}{(p_i&space;-&space;\overline{p_H})^2}}{n-1}&space;&plus;&space;\frac{\sum_{j=1}^{m}{(p_j&space;-&space;\overline{p_L})^2}}{m-1}})

其中 $n=7, m=20$ 分别为高频区和低频区英文字母数量，$p_i, p_j$ 为对应区域内每个英文字母出现的频率，$\overline{p_H}, \overline{p_H}$ 为高频区与低频区的平均频率。

显然，各均衡度越小，说明均衡性越好。

### 输入效率

定义使用全拼输入法撰写一篇文章的过程中，使用键盘输入中文的效率为字数与字母数的比值，即：

![](https://latex.codecogs.com/svg.image?\eta&space;=&space;\frac{N_C}{N_T}&space;\times&space;100\%)

其中 $N_C$ 为录入中文字符的个数，$N_T$ 为敲击键盘英文字母的次数。

## Procedure

### Heatmap

由输入的 PDF 文本文件得到其全拼输入的键盘使用热力图。

Input: 包含中文内容的文字型 PDF

Output: 热力图

### Evaluation

采用上述量化定义对输入的 PDF 文本文件进行均衡性分析与输入效率分析。

Input: 包含中文内容的文字型 PDF

Output: 量化评价标准及结果

### TypeCode

由输入的 PDF 文本文件得到其合适的优化输入编码方式及有关分析。

Input: 包含中文内容的文字型 PDF

Output: 打字编码方案及与全拼在均衡性和输入效率方面的对比

## Program

### Heatmap

此部分为明确的任务流程，实现起来也比较简单。先从 PDF 文件中读取文字，然后解析其拼音，统计每个字母出现的频率绘图即可。

为了能够快速完成任务，选用 Python 编写程序，使用 `pdfminer` 库进行 PDF 读取；使用 `xpinyin` 库进行拼音解析；使用 `tapmap` 库进行热力图绘制；使用 `matplotlib` 库实现图片显示。

### Evaluation

对各评价标准进行量化定义后，求值部分也比较任意时间，此处不再赘述。

### TypeCode

对全拼的优化我主要分为三个方面来实现：

- 对常用字的最短缩写。所提供示例中，拼音 "de" 的占比达 7.89%，对此类拼音应尽可能缩短，可以使输入效率大幅提高，所以将其直接缩短为对应的声母。

- 对固定字符串的替换。汉字输入使用的最频繁的两个键就是 "i" 和 "n"，要想使使用键盘更加均衡，首先就要解决这种极端性的问题。"n" 的使用大部分是由 "-ng" 词根贡献的，直接使用 "m" 来替换，在读音相似且不会引起误解的情况下，既缩短了长度，又降低了字母 "n" 的极端使用率；同样的，使用 "eo" 代替 "iao"、"on" 代替 "uan"，取其相似的发音并减少长度或降低极端字母的使用率。由于此部分内容的完善需要对汉语拼音做更为深入的研究，此处仅使用了上述的三个用例。

- 对不常用字符的利用。除了上述使用频率极端高的字母外，还有一些使用频率极端低的字母。对这部分的处理比较麻烦，也无奈只好放弃部分对任意记忆的要求。此部分较好的方法就是自己创造一些词根，和现有的词根做替换，并检查其均衡性，通过不断迭代找出最优的方案。毫无疑问要实现各个按键的绝对平等，大部分词根都会被替代掉，相当于重新制定了一套拼音方案。而我对此题的理解是对现有全拼拼音的“优化”，即不改变其大部分规则。所以此处使用了另一种方法，即把常用的字设置为“快捷键”，来利用上使用比较少的字母。由于拼音中的 "ü" ，一般使用键盘上的 "v"，使用频率是最低的，而且没有以 "v" 开头的拼音，所以使用 "v" 开头加上另一个不常用字母作为组合，来对应一个比较常用的拼音。如示例文件中 "gong" "chan" 出现的频率是很高的，将此类词组设置为快捷输入，既提高了输入效率，又使键盘的使用更加均衡。

### TypeCode2

很明显上述的做法是有很大局限性的，尝试优化了一段时间后，发现输入效率仍然不足 0.5，于是便想到了使用双拼。经过查阅资料和研究，发现双拼几乎已经把输入效率优化到了极致。

当然此处对双拼的研究和优化仍是基于之前的假设，即要求输入前后能够一对一恢复。由于双拼是定长编码，所以如果实现的话还能够额外解决分词多解的问题。

双拼是将全拼的声母和介母韵母部分分开，如果没有声母则称为零声母。以一个声母按键和一个介母韵母按键完成对一个全拼的编码。声母有 23 个，介母韵母有 34 个。由于零声母的情况只能由 "aoe" 三个字母开头，和 23 个声母加起来刚好把 26 个字母用完。介母韵母的个数超过了 26 个，处理方法如下。

经过对汉语拼音读音的统计，可以出现的音节如下图：

![声母和介母韵母配对统计](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Stat0.png?raw=true)

其中浅蓝色代表可配对，浅橙色代表无此配对，蓝色代表声母读音。明显可见有部分介母韵母和声母的搭配使用是不会重复的（其实大多也比较容易理解，介母的加入是根据声母决定），根据相似性原则找到所有不会重复的配对组合如下图：

![可替换介母韵母](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Stat1.png?raw=true)

一共有 7 对（"ang"），又由于 "er" 音节只能零声母使用，这样 34 个介母韵母刚好对应到 26 个字母键，经过对比发现，和现有的 26 键双拼方案基本一致（部分双拼配列是 27 键，额外使用了 ";" 键）。

对于零声母的处理方式有两种，一种就是将零声母的 "a" "o" "e" "ai" "ou" "ei" "an" "en" "ang" "eng" "ao" "er" 固定使用一个零声母的键，在双拼输入法中一般为 "O"，然后再加上介母韵母本来的键，当然 "er" 是没有对应的键的，所以要给它额外安排一个；另一种处理方案就是自然码，保持开头字母不变，把长度变成 2，即单字母双写，双字母不变，三字母缩写。 

对双拼的优化思路有以下几个方向：

- 零声母不同处理方式会影响键盘使用均衡性，但是由于零声母字符占比较少，可能对均衡性的影响不大。

- 介母韵母分为 26 组，和 26 个键盘字母按键一一对应，可以通过对比得出最均衡性最佳的方案。

- 若不考虑分词问题，对双拼进行改造可以使输入效率超过 0.5。

由于穷举训练耗时较大，这里给出一种比较简化的方案：即将声母和介母韵母部分的概率分别统计一遍，然后倒置组合，即声母部分用的最多，在韵母介母部分用的就最少，以得到较为合适的方案。

## Results

文件目录结构中，`heatmap` 是绘制热力图， `evaluation` 是计算评价指标，其功能均包含于完整的工程 `typecode` 中。`resouces` 为本文档所使用的图片文件。

`heatmap` 和 `evaluation` 用法分别为：

```
python heatmap.py ./data/test.pdf ./data/img.png
python evaluation.py ./data/test.pdf
```

下面重点介绍 `typecode` 工程。

### 基于全拼的优化

使用第一个版本的优化的命令如下：

```
python typecode.py ./data/test.pdf ./data/img.png
```

两个参数分别为输入的 PDF 和输出优化后热力图路径。命令行输出部分结果如下：

```
====== Original ======

Lenth of Chinese characters: 18118
Lenth of type coding: 53475
Input efficiency: 0.3388
Balance: 0.0378
Balance_r: 0.0297

====== Re-encode ======

Replace with b : bu
...
Replace with d : de
...
Replace with w : wei
Replace with zz : zh
Replace with cc : ch
Replace with ss : sh
Replace with m : ng
Replace with on : uan
Replace with eo : iao
Replace with vp : ccan
...
Replace with vx : zzem

Lenth of Chinese characters: 18118
Lenth of type coding: 39012
Input efficiency: 0.4644
Balance: 0.0222
Balance_r: 0.0158
```

输入效率从 0.3388 优化到了 0.4644，即从约三个字母一个汉字优化到约两个字母一个汉字。均衡度从 0.0378 优化到了 0.0222；重配列均衡度从 0.0297 优化到了 0.0158。

绘制优化前后的热力图如下图：

![方案一热力图](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Res0.png?raw=true)

从热力图可以看出此方案仍未完全拜摆脱拼音原生的不均匀性，会造成在一些按键上集中，而部分按键仍使用较少。

### 基于双拼思想的优化

使用第二个版本的优化的命令如下：

```
python typecode2.py ./data/test.pdf ./data/img.png
```

两个参数分别为输入的 PDF 和输出优化后热力图路径。命令行输出部分结果如下：

```
====== Original ======

Lenth of Chinese characters: 18118
Lenth of type coding: 53475
Input efficiency: 0.3388
Balance: 0.0378
Balance_r: 0.0297

====== Re-encode ======

Notice: "iang" same with "uang"
Notice: "ong" same with "iong"
Notice: "ing" same with "uai"
Notice: "ia" same with "ua"
Notice: "ue" same with "ve"
Notice: "o" same with "uo"
Notice: "v" same with "ui"
Replace with AA : a
Replace with AI : ai
Replace with AN : an
Replace with AH : ang
Replace with AO : ao
Replace with EE : e
Replace with EI : ei
Replace with EN : en
Replace with EG : eng
Replace with ER : er
Replace with OO : o
Replace with OU : ou
Replace with V : zh
Replace with U : sh
Replace with I : ch
Replace with N : n
Replace with G : g
Replace with D : d
Replace with J : j
Replace with Y : y
Replace with Z : z
Replace with L : l
Replace with X : x
Replace with H : h
Replace with B : b
Replace with T : t
Replace with M : m
Replace with W : w
Replace with Q : q
Replace with F : f
Replace with R : r
Replace with C : c
Replace with S : s
Replace with K : k
Replace with P : p
Replace with Y : iang
Replace with V : iao
Replace with Z : uan
Replace with L : ang
Replace with B : ing
Replace with T : ian
Replace with R : eng
Replace with P : ong
Replace with N : ue
Replace with G : iu
Replace with D : un
Replace with J : ia
Replace with U : in
Replace with I : ei
Replace with X : ao
Replace with H : ou
Replace with F : ai
Replace with C : ie
Replace with S : en
Replace with K : an
Replace with M : v
Replace with W : a
Replace with Q : o
Replace with A : u
Replace with E : e
Replace with O : i

Lenth of Chinese characters: 18118
Lenth of type coding: 36236
Input efficiency: 0.5000
Balance: 0.0182
Balance_r: 0.0203
```

使用完全符合双拼规则的优化方式，可以将均衡度进一步优化到 0.0182，而且定长编码，输入效率恒为 0.5。而且重配列均衡度已经大于均衡度，说明使用频率极端高的按键数量已经大幅减少。考虑到分词问题，如果将其进一步改为部分编码长度是 1 的话，虽然会进一步提升输入效率，但是得不偿失，故不再考虑缩短编码。

其热力图对比如下：

![方案二热力图](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Res1.png?raw=true)

可以看到热力分布已经较为均匀。由于代码中绘制的热力图区域较小，看起来不够直观，我在一个基于 `heatmap.js` 的网站 [Keyboard Heatmap](https://www.patrick-wied.at/projects/heatmap-keyboard/) 上重新绘制了原始热力图和两张优化方案的热力图：

![原始热力图](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Tapmap0.png?raw=true)

![方案一热力图](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Tapmap1.png?raw=true)

![方案二热力图](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Tapmap2.png?raw=true)


以上测试都是基于提供的附件《共产党宣言》进行，换为《马克思主义基本原理概论》使用方案二测试数据如下：

```
====== Original ======

Lenth of Chinese characters: 191249
Lenth of type coding: 573600
Input efficiency: 0.3334
Balance: 0.0383
Balance_r: 0.0292

====== Re-encode ======

Lenth of Chinese characters: 191249
Lenth of type coding: 382498
Input efficiency: 0.5000
Balance: 0.0185
Balance_r: 0.0198
```

![热力图](https://github.com/Moby-C/TypingCodingResearch/blob/main/resources/Res2.png?raw=true)
