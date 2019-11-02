from record import *
import numpy,math

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

    def getVariant(self):
        variant = []
        tmp = self.scanner.fetch()[0]
        variant.append(tmp)
        while tmp >= 128:
            tmp = self.scanner.fetch()[0]
            variant.append(tmp)
        return self.variantToInt(variant)

    def variantToInt(self, variant):
        value = 0
        for i in range(len(variant)):
            if variant[i] > 128:
                value += (variant[i] - 128) * (128 ** i)
            else:
                value += variant[i] * (128 ** i)
        return value

    def getType(self):
        val = self.scanner.fetch()
        if val == None:
            return None
        else:
            val = val[0]
        field = val >> 3
        type = val - (field << 3)
        return field, type

    def parse(self):
        pass


class parseGame(parser):
    def __init__(self, filename):
        with open(filename, 'rb') as file:
            self.protoData = file.read()
        self.scanner = scanner(self.protoData)
        super().__init__(self.scanner)
        self.gameRecord = []

    def parse(self):
        field, type = self.getType()
        if field!=1 or type!=2:
            raise RuntimeError()
        length = self.getVariant()
        self.scanner.fetch(length).decode()
        field, type = self.getType()
        if field!=2 or type!=2:
            raise RuntimeError()
        length = self.getVariant()
        data = self.scanner.fetch(length)
        a=parseRound(data)
        self.gameRecord=a.parse()




class parseRound(parser):
    def __init__(self, data):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.roundRecord = []

    def parse(self):
        field, type = self.getType()
        if field != 1 or type != 2:
            raise RuntimeError()
        length = self.getVariant()
        # start game
        tsc=parser(scanner(self.scanner.fetch(length)))
        field, type = tsc.getType()
        if field != 1 or type != 2:
            raise RuntimeError()
        data = tsc.scanner.fetch(tsc.getVariant())
        while 'NewRound' in data.decode():
            field, type = tsc.getType()
            if field != 2 or type != 2:
                raise RuntimeError()
            length = tsc.getVariant()
            tsc = parser(scanner(tsc.scanner.fetch(length)))
            field, type = tsc.getType()
            chang = tsc.getVariant()
            field, type = tsc.getType()
            ju = tsc.getVariant()
            field, type = tsc.getType()
            ben = tsc.getVariant()
            field, type = tsc.getType()
            while field<=5:
                length = tsc.getVariant()
                tsc.scanner.fetch(length)
                field, type = tsc.getType()
            if field==6:
                tsc.getVariant()
                field, type = tsc.getType()
            ttile=[]
            handtile=[]
            while field==7:
                length = tsc.getVariant()
                ttile.append(tsc.scanner.fetch(length).decode())
                field, type = tsc.getType()
            handtile.append(ttile)
            ttile = []
            while field==8:
                length = tsc.getVariant()
                ttile.append(tsc.scanner.fetch(length).decode())
                field, type = tsc.getType()
            handtile.append(ttile)
            ttile = []
            while field == 9:
                length = tsc.getVariant()
                ttile.append(tsc.scanner.fetch(length).decode())
                field, type = tsc.getType()
            handtile.append(ttile)
            if field==10:
                ttile = []
                while field == 10:
                    length = tsc.getVariant()
                    ttile.append(tsc.scanner.fetch(length).decode())
                    field, type = tsc.getType()
                handtile.append(ttile)
            roundRecord=Round(chang,ju,ben,handtile)
            print(handtile)
            field, type = self.getType()
            length = self.getVariant()
            # start game
            tsc = parser(scanner(self.scanner.fetch(length)))
            field, type = tsc.getType()
            leng=tsc.getVariant()
            data=tsc.scanner.fetch(leng).decode()
            while ('Discard' in data) or ('Deal' in data) or ('Chi' in data) or ('Gang' in data) or('BaBei'in data):
                tsc.getType()
                thisItem=parseitem(tsc.scanner.fetch(tsc.getVariant()),data)
                player, tile, op, source,isliqi=thisItem.parse()
                roundRecord.addItem(player, tile, op, source,isliqi)
                field, type = self.getType()
                length = self.getVariant()
                tsc = parser(scanner(self.scanner.fetch(length)))
                field, type = tsc.getType()
                leng = tsc.getVariant()
                data = tsc.scanner.fetch(leng).decode()

            if 'Hule' in data:
                field, type = tsc.getType()
                itf=parser(scanner(tsc.scanner.fetch(tsc.getVariant())))
                field, type = itf.getType()
                itf1 = parser(scanner(itf.scanner.fetch(itf.getVariant())))
                field, type = itf1.getType()
                while field!=4:
                    leng = itf1.getVariant()
                    aaa=itf1.scanner.fetch(leng)
                    field, type = itf1.getType()
                player = itf1.getVariant()+1
                field, type = itf1.getType()
                iszimo = itf1.getVariant()
                field, type = itf.getType()
                oldscore=[]
                itf.getVariant()
                for i in handtile:
                    oldscore.append(itf.getVariant())
                field, type = itf.getType()
                leng = itf.getVariant()
                aaa = itf.scanner.fetch(leng)
                field, type = itf.getType()
                leng = itf.getVariant()
                field, type = itf.getType()
                newscore = []
                itf.getVariant()
                for i in range(len(handtile)):
                    newscore.append(itf.getVariant())
                point=max([abs(newscore[i]-oldscore[i]) for i in range(len(newscore))])
                roundRecord.addItem(player, '', 0, 0, 0)
                roundRecord.winner = player
                roundRecord.iszimo=iszimo
                roundRecord.point=point
            if ('LiuJu' in data) or ('NoTile' in data):
                roundRecord.addItem(0, '', -10, 0, 0)
            roundRecord.print()
            self.roundRecord.append(roundRecord)
            tmp = self.getType()
            if tmp==None:
                break
            field, type = tmp
            if field != 1 or type != 2:
                raise RuntimeError()
            length = self.getVariant()
            # start game
            tsc = parser(scanner(self.scanner.fetch(length)))
            field, type = tsc.getType()
            if field != 1 or type != 2:
                raise RuntimeError()
            data = tsc.scanner.fetch(tsc.getVariant())

        return self.roundRecord


class parseitem(parser):
    def __init__(self, data,type):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.itemRecord = None
        self.type=0
        self.d0=type
        if 'Discard' in type:
            self.type =1
        if 'Deal' in type:
            self.type = 2
        if  'Chi' in type:
            self.type = 3
        if 'AnGang' in type:
            self.type=-1
        if 'BaBei' in type:
            self.type = 10

    def parse(self):
        if self.type == 10:
            field, type = self.getType()
            player = self.getVariant()+1
            return player,'', 10, 0, 0
        if self.type==1 or self.type==2:
            field, type = self.getType()
            player = self.getVariant()+1
            field, type = self.getType()
            tile = self.scanner.fetch(self.getVariant())
            field, type = self.getType()
            isliqi=self.getVariant()
            field, type = self.getType()
            op = self.type
            source = player
        elif self.type == 3:
            field, type = self.getType()
            player = self.getVariant()+1
            field, type = self.getType()
            tt = self.getVariant()
            '''
            tt=0 chi
            tt=1 peng
            tt=2 gang
            '''
            op = -tt-1
            field, type = self.getType()
            tile = self.scanner.fetch(self.getVariant())
            source = 0
            isliqi = 0
        else:
            field, type = self.getType()
            player = self.getVariant()+1
            field, type = self.getType()
            tt = self.getVariant()
            '''
            tt=3 an gang
            tt=2 add gang
            '''
            op = -tt -2
            field, type = self.getType()
            tile = self.scanner.fetch(self.getVariant())
            source = 0
            isliqi = 0


        return player, tile, op, source,isliqi





if __name__=="__main__":
    a=parseGame('../test/191023-b677c111-742f-4cd7-a7ee-31efef2b1928')
    a.parse()