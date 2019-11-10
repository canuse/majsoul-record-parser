# majsoul-record-parser

<a href="#english">English</a>

解析雀魂牌谱并分析

运行环境：**Python 3.5+**

## 样例说明

以此牌谱<a href="https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf">https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf</a>为例，分析结果在example文件夹下的html文件。

主要分析用户的出牌合理性，依据为其与最优出牌的进张枚数和向听（和）数。

在向听数相同时，我们可以认为一次切牌的效率为：

`η=(你的进张率)/（最优进张率）`

其中：

`进张率=1-（1-枚数/不可见牌数）/（1-枚数/（不可见牌数-1））`

在结果展示中，η越差（即本次出牌越不合理）的栏底色越深。

## 使用方式

由于诸多原因，全自动从链接直接生成分析结果的功能鸽了。

以chrome为例，具体步骤如下：

### 1. 获取牌谱数据

打开一个新的标签页，按下F12打开控制台。

在地址栏中输入牌谱链接，登录雀魂（如果需要），等待网页加载完毕。

在控制台中，切换到Network标签，在筛选条件中选择ws，应该可以看到唯一的一条ws消息。

在该消息中，找到我们需要的数据，并右键复制为base64格式。该数据一般具有以下特征：
* 是最后几条收到的消息（除去心跳包）之一
* 如果牌谱较新（3天内），该消息一般比其他消息大很多（20kb+）
* 如果牌谱较旧，该消息的末尾有```https://mj-srv-3.majsoul.com:7343/majsoul/game_record/```
* 该消息一般紧挨着内容为```lq.Lobby.fetchGameRecord （uuid）```的消息

如果你想通过登陆后的牌谱栏查看自己的牌谱，上面的4个特征一般依然符合。

![finddata.png](https://i.loli.net/2019/11/10/9wbQ6IxsMoW7hEZ.png)

### 2.运行分析

将复制的数据保存到合适的地方，之后进入项目根目录。

运行
```shell script
python3 main.py
```
在输入框中数据保存的文件路径，以及需要检查的用户名（或留空检查所有用户）

### 3. 查看结果

结果保存在当前目录下，文件名为'majsoul_record'+game_uuid+playername

模板使用了<a href="https://github.com/Ledenel/auto-white-reimu">Ledenel/auto-white-reimu</a>的模板。

注意，结果仅供参考。

## 已知问题

* 多家和了情况下程序可能异常退出
* 幺九牌过多导致的偏差。例如8种九牌时，一般此时向国士的向听数比一般型低，但是实际上正常玩家可能考虑的还是一般型。

## 接口

在`majsoul.parser` 中提供了`parseFromBase64(Filename)`，可以用来解析牌谱数据为可读的格式
在`majsoul.reasoner` 中提供了进张分析，牌理分析

<div id="english"></div>

# Readme

Decode Majsoul records and analyze it.

Require **Python3.5+**

## Example

Suppost we have this Paipu to decode: <a href="https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf">https://www.majsoul.com/1/?paipu=191105-de74c8bc-1725-4171-9587-9b91d0c6dddf</a>, teh result is saved in the example folder.

The programme mainly checks the efficiency of players' discarding tile operation. Namely, check the number of useful tiles.

Provided that both your choice and the best possible choices have the same number of steps to hule, we can define the efficiency of a discard operation as follows：

`η=(your_win_rate)/(best_possible_win_rate_)`

where,

`win_rate=1-(1-useful_tile_num/invisible_tile_num)/(1-useful_tile_num/(invisible_tile_num-1))`

In the result html files, those operations will a low η will be deeper. 

## How to use

For some reasons, the fully-automatic script is not available now, but it's in the todo list and might be finished in a couple of months.

The following steps are using a chrome browser.

### 1. Get the Paipu Record

Open a new chrome tab, and press F12 to open devtools.

Enter the paipu link in the address line and wait the website is fully loaded.(login might be required)

Switch to Network tab in the devtools window, and filter the data by ws. There should be only one ws connect.

Find the target data and copy it in base64 format. The data should contain these characteristics:

* It should be the last few received messages (except the heartbeat)
* If the record is new (match completed less than 3 days), then it should be much larger than other messages.(usually 30kb+)
* Otherwise, it should contain ```https://mj-srv-3.majsoul.com:7343/majsoul/game_record/```
* The message usually follows the ```lq.Lobby.fetchGameRecord （uuid）```message

![finddata.png](https://i.loli.net/2019/11/10/RwXYUQkduc1EJO3.png)

### 2. Run Programme

Save the copied message into a file, and then return to the root folder of this programme.

execute
```shell script
python3 main.py
```
Enter that file path and the player name to check (or leave it empty to check all users).

### 3. Results

It should be save in the same folder, whose filename should be 'majsoul_record'+game_uuid+playername

The templates is from <a href="https://github.com/Ledenel/auto-white-reimu">Ledenel/auto-white-reimu</a>.

Notice that the results should only be a suggestion, it should never be consider as the only right choice or the guideline to play mahjong.

## Known Bugs

* Multiple player hule in the same game. That will cause a crash. This bug would be fixed recently.
* Bias on yaojiu(幺九) tiles. Suppose we have 8 yaojiu tiles now, usually the number of step to guoshiwusuang(国士无双) is smaller than normal type wins, but most players prefers normal win types.

## api

The programme also provided some useful api.

The `parseFromBase64(Filename)` in `majsoul.parser` can decode the base64 protobuf majsoul record into readable format.

Useful tile count and analyze functions can be found in `majsoul.reasoner`