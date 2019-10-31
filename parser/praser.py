from .record import *

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
        tmp = self.scanner.fetch()
        variant.append(tmp)
        while tmp[0] >= 128:
            tmp = self.scanner.fetch()
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


class parseGame(parser):
    def __init__(self, filename):
        with open(filename, 'rb') as file:
            self.protoData = file.read()
        self.scanner = scanner(self.protoData)
        super().__init__(self.scanner)
        self.gameRecord=Game()


class praseRound(parser):
    def __init__(self, data):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.roundRecord=None


class praseitem(parser):
    def __init__(self, data):
        self.scanner = scanner(data)
        super().__init__(self.scanner)
        self.itemRecord = None
