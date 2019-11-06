from enum import Enum


class Players:
    def __init__(self, names=None):
        if names == None:
            self.playernames = ['player 1', 'player 2', 'player 3', 'player 4']
        else:
            self.playernames = names


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
    def __init__(self, player, tile, op, source, isliqi,players:Players):
        """
        :param player: 1.east 2.south 3.west 4.north
        :param tile: string
        :param op: 1:deal 2:discard -1.chi -2.peng -3.gang -4 addgang -5 angang 0.hu 10,babei -10 liuju
        :param source: 1.east 2.south 3.west 4.north 0.prev
        """
        self.player = Position(player)
        self.playername=players.playernames[self.player.value - 1]
        self.tile = tile
        self.op = Operation(op)
        self.isliqi = isliqi

    def __str__(self):
        if self.op.value == 1 or self.op.value == 2:
            return "{0} {1} tile {2} {3}".format(self.playername, self.op, self.tile,
                                                 'lizhi' if self.isliqi == 1 else '')
        elif self.op.value == 0:
            return "{0} hule".format(self.playername)
        elif self.op.value == 10:
            return "{0} babei".format(self.playername)
        elif self.op.value == -10:
            return "流局"
        else:
            return "player {0} {1} tile {2}".format(self.playername, self.op,
                                                              self.tile)


class Round:
    def __init__(self, chang, ju, ben, handTiles,players:Players):
        self.ju = ju
        self.chang = chang
        self.ben = ben
        self.handTiles = handTiles
        self.winner = None
        self.isZiMo = None
        self.point = None
        self.itemList = []
        self.players=players

    def addItem(self, player, tile, op, source, isliqi):
        self.itemList.append(Item(player, tile, op, source, isliqi,self.players))

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
        if self.winner == None:
            return
        if self.isZiMo:
            print('{0} 自摸 {1} 点'.format(self.players.playernames[int(self.winner) - 1], self.point))
        else:
            print('{0} 和牌 {1} 点'.format(self.players.playernames[int(self.winner) - 1], self.point))

    def __str__(self):
        if self.winner == None:
            return '{0} {1} 局 {2} 本场 '.format(['东', '南', '西', '北'][self.chang], self.ju + 1, self.ben) + '流局'

        if self.isZiMo:
            return '{0} {1} 局 {2} 本场 '.format(['东', '南', '西', '北'][self.chang], self.ju + 1,
                                              self.ben) + '{0} 自摸 {1} 点'.format(self.players.playernames[int(self.winner) - 1],
                                                                                self.point)
        else:
            return '{0} {1} 局 {2} 本场 '.format(['东', '南', '西', '北'][self.chang], self.ju + 1,
                                              self.ben) + '{0} 和牌 {1} 点'.format(self.players.playernames[int(self.winner) - 1],
                                                                                self.point)


class Game:
    def __init__(self, players: Players):
        self.roundList = []
        self.players = players.playernames

    def __str__(self):
        for i in self.roundList:
            print(i)
