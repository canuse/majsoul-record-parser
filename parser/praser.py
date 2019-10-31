from record import *


class scanner:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.len = len(data)

    def fetch(self, len=1):
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
        val = self.scanner.fetch()[0]
        field = val >> 3
        type = val - (field << 3)
        return field, type


class parseGame(parser):
    def __init__(self, filename):
        with open(filename, 'rb') as file:
            self.protoData = file.read()
        self.scanner = scanner(self.protoData)
        super().__init__(self.scanner)
        self.gameRecord = Game()

    def parse(self):
        field, type = self.getType()
        if field!=1 or type!=2:
            raise RuntimeError()
        length = self.getVariant()
        self.scanner.fetch(length)
        field, type = self.getType()
        if field!=2 or type!=2:
            raise RuntimeError()
        length = self.getVariant()
        data = self.scanner.fetch(length)
        newRound = parseRound(data)
        newRound.parse()


class parseRound(parser):
    def __init__(self, data):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.roundRecord = None

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
        tsc.scanner.fetch(tsc.getVariant())
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
        while field!=7:
            length = tsc.getVariant()
            tsc.scanner.fetch(length)
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
        thisround=Round(chang,ju,ben,handtile)
        print(handtile)


class parseitem(parser):
    def __init__(self, data):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.itemRecord = None

if __name__=="__main__":
    a=parseGame('../test/1')
    a.parse()