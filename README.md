# majsoul-record-parser

<a href="#english">English</a>

解析雀魂牌谱并分析

运行环境：**Python 3.5+**, Chrome/Firefox, Tampermonkey

## 样例说明

以此牌谱<a href="https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf">https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf</a>为例，分析结果在example文件夹下的html文件。

主要分析用户的出牌合理性，依据为其与最优出牌的进张枚数和向听（和）数。

在向听数相同时，我们可以认为一次切牌的效率为：

`η=(你的进张率)/（最优进张率）`

其中：

`进张率=1-（1-枚数/不可见牌数）/（1-枚数/（不可见牌数-1））`

在结果展示中，η越差（即本次出牌越不合理）的栏底色越深。

## 使用方式

以Chrome为例，具体步骤如下：

### 1. 安装Tampermonkey插件以及脚本

通过Chrome应用商店或其他教程安装Tampermonkey插件。

在Tampermonkey中选择添加新脚本，将<a href="https://github.com/canuse/majsoul-record-parser/blob/master/js/majsoul.js">js/majsoul.js</a>中的内容复制到弹出的窗口中并保存。

该脚本会自动将雀魂websocket中的数据转发到本地，以供分析。

理论上该脚本对于网站性能及数据没有影响，如果开启后玄学变卡或脱欧入非，请考虑在分析牌谱以外的时间在Tampermonkey中关闭此脚本并刷新页面。

### 2. 牌谱分析

我们使用一个简单的HTTP server处理收到的数据，运行```main.py```开启服务器。
```shell script
python3 main.py
```
之后，在雀魂网页中选择期望分析的牌谱并点击查看即自动开始分析。

### 3. 查看结果

结果保存在当前目录下，文件名为'majsoul_record'+game_uuid+playername。由于windows文件名限制，部分特殊符号会被转换。

模板使用了<a href="https://github.com/Ledenel/auto-white-reimu/blob/master/mahjong/templates/record_checker_template.html">Ledenel/auto-white-reimu</a>的模板。

注意，结果仅供参考。

## 已知问题

* 多家和了情况下程序可能异常退出
* 幺九牌过多导致的偏差。例如8种九牌时，一般此时向国士的向听数比一般型低，但是实际上正常玩家可能考虑的还是一般型。

## 自动化（实验）

我们使用selenium完成输入牌谱的完整自动化分析，脚本位于<a href="https://github.com/canuse/majsoul-record-parser/blob/master/auto/auto.py">auto/auto.py</a>.

关于selenium的安装与配置，请参考官方文档。

我们还使用selenium加载了chrome的默认配置，请参考<a href="https://stackoverflow.com/questions/31062789/how-to-load-default-profile-in-chrome-using-python-selenium-webdriver">How to load default profile in chrome using Python Selenium Webdriver?
</a>补充auto.py中的部分路径。

目前此方法打开浏览器等操作较缓慢，正常使用请用第一种方法。

## 接口

在`majsoul.parser` 中提供了`parseFromBase64(Filename)`，可以用来解析牌谱数据为可读的格式
在`majsoul.reasoner` 中提供了进张分析，牌理分析

<div id="english"></div>

# Readme

Decode Majsoul records and analyze it.

Require **Python3.5+**, Chrome/Firefox, Tampermonkey

## Example

Suppost we have this Paipu to decode: <a href="https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf">https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf</a>, teh result is saved in the example folder.

The programme mainly checks the efficiency of players' discarding tile operation. Namely, check the number of useful tiles.

Provided that both your choice and the best possible choices have the same number of steps to hule, we can define the efficiency of a discard operation as follows：

`η=(your_win_rate)/(best_possible_win_rate_)`

where,

`win_rate=1-(1-useful_tile_num/invisible_tile_num)/(1-useful_tile_num/(invisible_tile_num-1))`

In the result html files, those operations will a low η will be deeper. 

## How to use

The following steps are using a chrome browser.

### 1. Install Tampermonkey and scripts

Tampermonkey in an extension of Chrome and Firefox, you can install it easily from the Chrome online extension store.

To add the scripts into Tampermonkey, you need to click the Tampermonkey icon on the top right of the tool bar, and select 'add script'.
Then please copy the script <a href="https://github.com/canuse/majsoul-record-parser/blob/master/js/majsoul.js">js/majsoul.js</a> into the window and press save button.

Restart the browser if needed.

The script will automatically forward the data in the majsoul websocket connection to the localhost, which can be analyzed later.

The script should affect neither the performance nor the data of the website, but if you are facing that problem, please turn off the script. 

### 2. Paipu Analyze

We use a simple HTTP server to process the received data. You can execute ```main.py``` to start the server.
```shell script
python3 main.py
```

Then you can visit the Paipu link and the analyze programme will automatically start.

### 3. Results

It should be save in the same folder, whose filename should be 'majsoul_record'+game_uuid+playername. Note that some symbols will be renamed due to the naming restrictions of windows.

The templates is from <a href="https://github.com/Ledenel/auto-white-reimu">Ledenel/auto-white-reimu</a>.

Notice that the results should only be a suggestion, it should never be consider as the only right choice or the guideline to play mahjong.

## Link-to-result script (experimental)

We use selenium to finish this task. The script can be found at <a href="https://github.com/canuse/majsoul-record-parser/blob/master/auto/auto.py">auto/auto.py</a>.

To install and config Selenium, you can refer to the official documents.

You also need to complete the path in auto.py, please refer to <a href="https://stackoverflow.com/questions/31062789/how-to-load-default-profile-in-chrome-using-python-selenium-webdriver">How to load default profile in chrome using Python Selenium Webdriver?
</a>.

There are some problems including low performance currently in this script, **so the first method is recommended**.

## Known Bugs

* Multiple player hule in the same game. That will cause a crash. This bug would be fixed recently.
* Bias on yaojiu(幺九) tiles. Suppose we have 8 yaojiu tiles now, usually the number of step to guoshiwusuang(国士无双) is smaller than normal type wins, but most players prefers normal win types.

## api

The programme also provided some useful api.

The `parseFromBase64(Filename)` in `majsoul.parser` can decode the base64 protobuf majsoul record into readable format.

Useful tile count and analyze functions can be found in `majsoul.reasoner`