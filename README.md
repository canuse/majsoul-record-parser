# majsoul-record-parser
Translate Majsoul records into readable docs.

Require Python3

## Example

Suppose we have a paipu to decode:```https://www.majsoul.com/1/?paipu=190919-e9603e54-e79d-425b-a99c-c2f0a1df9d72_a89008372```

An example of the result should like <a href="https://github.com/canuse/majsoul-record-parser/blob/master/example/example.txt">example/example.txt</a>.

## How to use

The programme mainly support 2 types of input: from an URL or from a base64 file.

Since the majsoul paipu archive server only saves paipu older than 7 days and there are some missing fields in the archived files, **I recommend to decode from a base64 file**.
 
### Decode from a Base64 File (recommend)

You can use ```parseFromBase64(Filename)``` function to decode from a base64 file.

#### step 1. get the Base64 File

In this step, you need to copy the paipu string from the websocket and save it.

Take the above link as an example.
1. You need to open a modern browser(like chrome) first, then press the F12 button.
2. Paste the link into the address line and wait for the page completely loaded.
3. Find the only websocket in the **Network** tab of the **devtool** window.
4. Find the message we need from that websocket.
5. Right click that message and select ```copy message--copy as base64```, then paste and save it to your disk.

Basically, that message has these features:
* If the paipu is less than 7 days, the message size should be much bigger than others. Typically, it should be around 30~50kb while other messages are less than 10 kb. If it's old, the size should around 500B.
* The message should contain the uuid in the link. In this example, it should contain ```190919-e9603e54-e79d-425b-a99c-c2f0a1df9d72```.
* Usually, the message should be the last or the second to last received message.

Two examples of that message should like :
![message_old.png](https://i.loli.net/2019/11/06/6zYUkrCcEtiaxXg.png)

![message_new.png](https://i.loli.net/2019/11/06/7VjZkrHfG6TsRID.png)

#### step 2. decode the file

Suppose you have successfully download the message and save it to ```message.txt```, you can run the following code to decode the message.

```python
from majsoul.parser import *
a=parseFromBase64('/path/to/base64/file')
```

The record is saved in ```a```, whose structure should be:
```
Game━┳━━━━playernames
     ┃
     ┗━━━━roundList ━┳━━━Round 1 ━━━━━━itemList ━┳━━━ operation 1
                     ┣━━━Round 2                 ┣━━━ operation 2
                     ┃                           ┃
                     ┃                           ┃
                     ┗━━━Round m                 ┗━━━operation m
```

You can run ```a.print()``` to see the result, as is showed in <a href="https://github.com/canuse/majsoul-record-parser/blob/master/example/example.txt">example/example.txt</a> in this example.

### Decode from URL

You can use the ```parseFromURL(URL)``` function to decode directly from URL.

```python
from majsoul.parser import *
a=parseFromURL('https://www.majsoul.com/1/?paipu=190919-e9603e54-e79d-425b-a99c-c2f0a1df9d72_a89008372')
```

Notice that this method get records from the majsoul paipu archive server, so it is not suitable to new records (less than 7 days). 

The records also have missing field (player name) and they will be replaced by player 1,2,3 and 4.

## Konwn Bugs

* Multiple player hule(多家和了)
