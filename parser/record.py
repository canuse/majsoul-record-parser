from enum import Enum

playernames = []


def updatePlayername(names):
    global playernames
    playernames = names


class Operation(Enum):
    deal = 1
    discard = 2
    chi = -1
    peng = -2
    gang = -3
    addGang = -4
    anGang = -5
    hu = 0
    babei = 10
    liuju = -10

    def __str__(self):
        return self.name


class Position(Enum):
    east = 1
    south = 2
    west = 3
    north = 4
    prev = 0

    def __str__(self):
        return self.name


class Item:
    def __init__(self, player, tile, op, source, isliqi):
        """
        :param player: 1.east 2.south 3.west 4.north
        :param tile: string
        :param op: 1:deal 2:discard -1.chi -2.peng -3.gang -4 addgang -5 angang 0.hu 10,babei -10 liuju
        :param source: 1.east 2.south 3.west 4.north 0.prev
        """
        self.player = Position(player)
        self.tile = tile
        self.op = Operation(op)
        self.source = Position(source)
        self.isliqi = isliqi

    def __str__(self):
        if len(playernames) == 0:
            if self.op.value == 1 or self.op.value == 2:
                return "player {0} {1} tile {2} {3}".format(self.player, self.op, self.tile,
                                                            'lizhi' if self.isliqi == 1 else '')
            elif self.op.value == 0:
                return "player {0} hule".format(self.player)
            elif self.op.value == 10:
                return "player {0} babei".format(self.player)
            elif self.op.value == -10:
                return "流局"
            else:
                return "player {0} {1} tile {2}, from player{3}".format(self.player, self.op, self.tile, self.source)
        else:
            if self.op.value == 1 or self.op.value == 2:
                return "{0} {1} tile {2} {3}".format(playernames[self.player.value-1], self.op, self.tile,
                                                     'lizhi' if self.isliqi == 1 else '')
            elif self.op.value == 0:
                return "{0} hule".format(playernames[self.player.value-1])
            elif self.op.value == 10:
                return "{0} babei".format(playernames[self.player.value-1])
            elif self.op.value == -10:
                return "流局"
            else:
                return "player {0} {1} tile {2}, from {3}".format(playernames[self.player.value-1], self.op, self.tile,
                                                                        playernames[self.source.value-1])


class Round:
    def __init__(self, chang, ju, ben, handTiles):
        self.ju = ju
        self.chang = chang
        self.ben = ben
        self.handTiles = handTiles
        self.winner = None
        self.isZiMo = None
        self.point = None
        self.itemList = []

    def addItem(self, player, tile, op, source, isliqi):
        self.itemList.append(Item(player, tile, op, source, isliqi))

    def endRound(self, winner, looser, isZiMo, point):
        self.winner = Position(winner)
        self.looser = Position(looser)
        self.isZiMo = isZiMo
        self.point = point

    def print(self):
        print('{0} {1} 局 {2} 本场'.format(['东', '南', '西', '北'][self.chang], self.ju + 1, self.ben))
        print('玩家手牌：')
        for i in self.handTiles:
            print(i)
        for i in self.itemList:
            print(str(i))
        if self.winner==None:
            return
        if len(playernames) == 0:
            if self.isZiMo:
                print('player {0} 自摸 {1} 点'.format(self.winner, self.point))
            else:
                print('player {0} 和牌 {1} 点'.format(self.winner, self.point))
        else:
            if self.isZiMo:
                print('{0} 自摸 {1} 点'.format(playernames[int(self.winner) -1], self.point))
            else:
                print('{0} 和牌 {1} 点'.format(playernames[int(self.winner) -1], self.point))


class Game:
    def __init__(self):
        self.roundList = []

    def addRound(self, round):
        self.roundList.append(round)

    def __str__(self):
        for i in self.roundList:
            print(i)
