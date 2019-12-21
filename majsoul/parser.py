import base64

import requests

from majsoul.record import *
from majsoul.tile import Tile


class scanner:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.len = len(data)

    def fetch(self, len=1):
        if self.pos + len > self.len:
            return None
        ret = self.data[self.pos:self.pos + len]
        self.pos += len
        return ret


class parser:
    def __init__(self, scanner):
        self.scanner = scanner
        pass

    def fetch(self, len=1):
        return self.scanner.fetch(len)

    def isEOF(self):
        return self.scanner.pos < self.scanner.len

    def getVariant(self):
        variant = []
        tmp = self.fetch()[0]
        variant.append(tmp)
        while tmp >= 128:
            tmp = self.fetch()[0]
            variant.append(tmp)
        return self.variantToInt(variant)

    def isNegative(self, i):
        return i == 1 or i // 2 == 1 or i // 4 == 1 or i // 8 == 1 or i // 16 == 1 or i // 32 == 1 or 1 // 64 == 1 or i // 128 == 1 or i // 256 == 1

    def variantToInt(self, variant):
        value = 0
        sign = 1
        if len(variant) > 5 and self.isNegative(variant[-1]):
            # work around only, not correct translate
            for i in range(len(variant)):
                variant[i] = 255 - variant[i]
            variant[0] += 1
            variant[-1] = 0
            sign = -1

        for i in range(len(variant)):
            if variant[i] >= 128:
                value += (variant[i] - 128) * (128 ** i)
            else:
                value += variant[i] * (128 ** i)
        return value * sign

    def getType(self):
        val = self.fetch()
        if val == None:
            return None
        else:
            val = val[0]
        field = val >> 3
        type = val - (field << 3)
        return field, type

    def parse(self):
        pass

    def skipString(self):
        field, type = self.getType()
        return self.fetch(self.getVariant())

    def skip(self):
        field, type = self.getType()
        return self.getVariant()


class parseGame(parser):
    def __init__(self, data, players, uuid=None):
        self.protoData = data
        self.scanner = scanner(self.protoData)
        super().__init__(self.scanner)
        self.gameRecord = []
        self.game = Game(players)
        self.players = players
        self.game.uuid = uuid.decode()

    def parse(self):
        field, type = self.getType()
        if field != 1 or type != 2:
            raise RuntimeError()
        length = self.getVariant()
        self.fetch(length).decode()
        field, type = self.getType()
        if field != 2 or type != 2:
            raise RuntimeError()
        length = self.getVariant()
        data = self.fetch(length)
        a = parseRound(data, self.players)
        self.gameRecord = a.parse()
        self.game.roundList = self.gameRecord
        return self.game


class parseRound(parser):
    def __init__(self, data, players):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.roundRecord = []
        self.players = players

    def parse(self):
        field, type = self.getType()
        if field != 1 or type != 2:
            raise RuntimeError()
        length = self.getVariant()
        # start game
        tsc = parser(scanner(self.fetch(length)))
        field, type = tsc.getType()
        if field != 1 or type != 2:
            raise RuntimeError()
        data = tsc.fetch(tsc.getVariant())
        while 'NewRound' in data.decode():
            field, type = tsc.getType()
            if field != 2 or type != 2:
                raise RuntimeError()
            length = tsc.getVariant()
            tsc = parser(scanner(tsc.fetch(length)))
            field, type = tsc.getType()
            chang = tsc.getVariant()
            field, type = tsc.getType()
            ju = tsc.getVariant()
            field, type = tsc.getType()
            ben = tsc.getVariant()
            field, type = tsc.getType()
            while field <= 5:
                length = tsc.getVariant()
                tsc.fetch(length)
                field, type = tsc.getType()
            if field == 6:
                tsc.getVariant()
                field, type = tsc.getType()
            ttile = []
            handtile = []
            while field == 7:
                length = tsc.getVariant()
                ttile.append(tsc.fetch(length).decode())
                field, type = tsc.getType()
            handtile.append(ttile)
            ttile = []
            while field == 8:
                length = tsc.getVariant()
                ttile.append(tsc.fetch(length).decode())
                field, type = tsc.getType()
            handtile.append(ttile)
            ttile = []
            while field == 9:
                length = tsc.getVariant()
                ttile.append(tsc.fetch(length).decode())
                field, type = tsc.getType()
            handtile.append(ttile)
            if field == 10:
                ttile = []
                while field == 10:
                    length = tsc.getVariant()
                    ttile.append(tsc.fetch(length).decode())
                    field, type = tsc.getType()
                handtile.append(ttile)
            roundRecord = Round(chang, ju, ben, handtile, self.players)
            if field == 12:
                tsc.fetch(tsc.getVariant())
                tsc.skipString()
                paishan = tsc.skipString().decode()
                for i in range(int(0.5 * len(paishan))):
                    roundRecord.paishan.append(paishan[2 * i:2 * i + 2])
            # print(handtile)
            field, type = self.getType()
            length = self.getVariant()
            # start game
            tsc = parser(scanner(self.fetch(length)))
            field, type = tsc.getType()
            leng = tsc.getVariant()
            data = tsc.fetch(leng).decode()
            while ('Discard' in data) or ('Deal' in data) or ('Chi' in data) or ('Gang' in data) or ('BaBei' in data):
                tsc.getType()
                thisItem = parseitem(tsc.fetch(tsc.getVariant()), data)
                player, tile, op, source, isliqi, tts = thisItem.parse()
                roundRecord.addItem(player, tile, op, source, isliqi, tts)
                field, type = self.getType()
                length = self.getVariant()
                tsc = parser(scanner(self.fetch(length)))
                field, type = tsc.getType()
                leng = tsc.getVariant()
                data = tsc.fetch(leng).decode()

            if 'Hule' in data:
                field, type = tsc.getType()
                itf = parser(scanner(tsc.fetch(tsc.getVariant())))
                field, type = itf.getType()
                itf1 = parser(scanner(itf.fetch(itf.getVariant())))
                field, type = itf1.getType()
                while field != 4:
                    leng = itf1.getVariant()
                    aaa = itf1.fetch(leng)
                    field, type = itf1.getType()
                player = itf1.getVariant() + 1
                field, type = itf1.getType()
                iszimo = itf1.getVariant()
                field, type = itf.getType()
                oldscore = []
                ta=itf.getVariant()
                if ta > 12:
                    itf.fetch(ta)
                    field, type = itf.getType()
                    ta = itf.getVariant()
                for i in handtile:
                    oldscore.append(itf.getVariant())
                itf.skipString()
                itf.skip()

                newscore = []
                itf.skip()
                for i in range(len(handtile)):
                    newscore.append(itf.getVariant())
                point = max([abs(newscore[i] - oldscore[i]) for i in range(len(newscore))])
                roundRecord.addItem(player, '', 0, 0, 0)
                roundRecord.winner = player
                roundRecord.isZiMo = iszimo
                roundRecord.point = point
            if ('LiuJu' in data) or ('NoTile' in data):
                roundRecord.addItem(0, '', -10, 0, 0)
            # roundRecord.print()
            self.roundRecord.append(roundRecord)
            tmp = self.getType()
            if tmp == None:
                break
            field, type = tmp
            if field != 1 or type != 2:
                raise RuntimeError()
            length = self.getVariant()
            # start game
            tsc = parser(scanner(self.fetch(length)))
            field, type = tsc.getType()
            if field != 1 or type != 2:
                raise RuntimeError()
            data = tsc.fetch(tsc.getVariant())

        return self.roundRecord


class parseitem(parser):
    def __init__(self, data, type):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.itemRecord = None
        self.type = 0
        self.d0 = type
        if 'Discard' in type:
            self.type = 1
        if 'Deal' in type:
            self.type = 2
        if 'Chi' in type:
            self.type = 3
        if 'AnGang' in type:
            self.type = -1
        if 'BaBei' in type:
            self.type = 10

    def parse(self):
        tts = None
        if self.type == 10:
            field, type = self.getType()
            player = self.getVariant() + 1
            return player, '', 10, 0, 0, 0
        if self.type == 1 or self.type == 2:
            field, type = self.getType()
            player = self.getVariant() + 1
            field, type = self.getType()
            tile = self.fetch(self.getVariant()).decode()
            field, type = self.getType()
            isliqi = self.getVariant()
            field, type = self.getType()
            op = self.type
            source = player
        elif self.type == 3:
            field, type = self.getType()
            player = self.getVariant() + 1
            field, type = self.getType()
            tt = self.getVariant()
            '''
            tt=0 chi
            tt=1 peng
            tt=2 gang
            '''
            op = -tt - 1
            field, type = self.getType()
            tile = self.fetch(self.getVariant()).decode()
            if tt == 0:
                tile2 = self.skipString().decode()
                tile3 = self.skipString().decode()
                if Tile.tileToValue(tile3) > Tile.tileToValue(tile2):
                    tts = 3  # a a+1 eat a+2
                elif Tile.tileToValue(tile3) < Tile.tileToValue(tile):
                    tts = 1  # a+1 a+2 eat a
                else:
                    tts = 2
                tile = tile3
            source = 0
            isliqi = 0

        else:
            field, type = self.getType()
            player = self.getVariant() + 1
            field, type = self.getType()
            tt = self.getVariant()
            '''
            tt=3 an gang
            tt=2 add gang
            '''
            op = -tt - 2
            field, type = self.getType()
            tile = self.fetch(self.getVariant()).decode()
            source = 0
            isliqi = 0

        return player, tile, op, source, isliqi, tts


'''
def parseFromURL(url):
    uuid = url.split('paipu=')[-1].split('_')[0]
    r = requests.get('https://mj-srv-3.majsoul.com:7343/majsoul/game_record/' + uuid)
    players = Players()
    if 'NoSuchKey' in r.content.decode():
        print("The record is too new and the majsoul server hasn't updated it yet. Please refer to other methods.")
    else:
        a = parseGame(r.content, players)
        return a.parse()


def parseFromDisk(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    players = Players()
    a = parseGame(data, players)
    return a.parse()
'''


def parseFromBase64data(data):
    tsc = parser(scanner(data))
    tsc.skip()
    field, type = tsc.getType()
    content = tsc.fetch(tsc.getVariant())
    tsc = parser(scanner(content))
    field, type = tsc.getType()

    content = tsc.fetch(tsc.getVariant())
    tt = parser(scanner(content))
    uuid = tt.skipString()
    startTime = tt.skip()
    endTime = tt.skip()
    tt.skipString()
    field, type = tt.getType()
    players = Players()
    while field == 11:
        tdata = tt.fetch(tt.getVariant())
        tt1 = parser(scanner(tdata))
        accountID = tt1.skip()
        seat = tt1.skip()
        field, type = tt1.getType()
        name = tt1.fetch(tt1.getVariant()).decode()
        tt1.skip()
        tt1.skipString()
        tt1.skip()
        tt2 = parser(scanner(tt1.skipString()))
        level4 = tt2.skip()
        score4 = tt2.skip()
        tt2 = parser(scanner(tt1.skipString()))
        level3 = tt2.skip()
        score3 = tt2.skip()
        players.add(name, seat, level3, score3, level4, score4)
        field, type = tt.getType()
    result = tt.fetch(tt.getVariant())
    resultPar = parser(scanner(result))
    while resultPar.isEOF():
        playerItem = parser(scanner(resultPar.skipString()))
        seat = playerItem.skip()
        endPoint = playerItem.skip() / 1000
        endScore = playerItem.skip()
        players.player[seat].endGame(endScore, endPoint)

    field, type = tsc.getType()
    length = tsc.getVariant()
    if length > 2000:
        data = tsc.fetch(length)
        a = parseGame(data, players, uuid)
        return a.parse()
    else:
        tsc.fetch(length)
        field, type = tsc.getType()
        data = tsc.fetch(tsc.getVariant()).decode()
        r = requests.get(data)
        a = parseGame(r.content, players, uuid)
        return a.parse()


def parseFromBase64(filename):
    with open(filename, 'r') as f:
        raw = f.read()
    data = base64.b64decode(raw)[3:]
    return parseFromBase64data(data)


if __name__ == "__main__":
    a = parseFromBase64('../test/b643.txt')
    a.print()
    # parseFromDisk('../test/191023-b677c111-742f-4cd7-a7ee-31efef2b1928')
