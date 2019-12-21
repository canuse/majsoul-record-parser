# majsoul-record-parser

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

* (fixed)~~Multiple player hule in the same game. That will cause a crash. This bug would be fixed recently.~~
* Bias on yaojiu(幺九) tiles. Suppose we have 8 yaojiu tiles now, usually the number of step to guoshiwusuang(国士无双) is smaller than normal type wins, but most players prefers normal win types.

## api

The programme also provided some useful api.

The `parseFromBase64(Filename)` in `majsoul.parser` can decode the base64 protobuf majsoul record into readable format.

Useful tile count and analyze functions can be found in `majsoul.reasoner`

## Declaration

This project is just for learning and practising purpose, and I am **not** interested in cheating script or majsoul server hacking.

If you want to use this project for those illegal usages, that would be **at your own risk**.
