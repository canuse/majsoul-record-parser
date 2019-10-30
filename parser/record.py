from enum import Enum


class Operation(Enum):
    deal = 1
    discard = 2
    chi = -1
    peng = -2
    gang = -3
    hu = 0

    def __str__(self):
        return self.name


class Position(Enum):
    east = 1
    south = 2
    west = 3
    north = 4

    def __str__(self):
        return self.name


class Item:
    def __init__(self, player, tile, op, source):
        """
        :param player: 1.east 2.south 3.west 4.north
        :param tile: string
        :param op: 1:deal 2:discard -1.chi -2.peng -3.gang 0.hu
        :param source: 1.east 2.south 3.west 4.north
        """
        self.player = Position(player)
        self.tile = tile
        self.op = Operation(op)
        self.source = Position(source)

    def __str(self):
        if self.op.value == 1 or self.op.value == 2:
            return "player {0} {1} tile {2}".format(self.player, self.op, self.tile)
        else:
            return "player {0} {1} tile {2}, from player{3}".format(self.player, self.op, self.tile, self.source)


class Round:
    def __init__(self, chang, ju, ben, handTiles):
        self.ju = ju
        self.chang = chang
        self.ben = ben
        self.handTiles = handTiles
        self.winner = None
        self.isZiMo = None
        self.looser = None
        self.point = None
        self.itemList = []

    def addItem(self, player, tile, op, source):
        self.itemList.append(Item(player, tile, op, source))

    def endRound(self, winner, looser, isZiMo, point):
        self.winner = Position(winner)
        self.looser = Position(looser)
        self.isZiMo = isZiMo
        self.point = point

    def __str__(self):
        print('{0} {1} 局 {2} 本场'.format(self.chang, self.ju, self.ben))
        print('玩家手牌：')
        for i in self.handTiles:
            print(i)
        for i in self.itemList:
            print(i)
        if self.isZiMo:
            print('player {0} 自摸 {1}'.format(self.winner, self.point))
        else:
            print('player {0} 和牌{1}，放铳者 player {2}'.format(self.winner, self.point, self.looser))


class Game:
    def __init__(self):
        self.roundList = []

    def addRound(self, chang, ju, ben, handTiles):
        self.roundList.append(Round(chang, ju, ben, handTiles))

    def __str__(self):
        for i in self.roundList:
            print(i)
