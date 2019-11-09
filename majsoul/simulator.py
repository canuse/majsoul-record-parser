from majsoul.record import *
from majsoul.tile import *


class simulator:
    def __init__(self, record: Game, username):
        self.record = record
        self.playername = username
        self.users = record.players.playernames
        self.posInUser = self.users.index(self.playername)
        self.gametype = 0
        self.playernum = record.players.num

    def simulate(self):
        for i in self.record.roundList:
            self.simulateRound(i)

    def initround(self, roundData: Round):
        self.handtile = roundData.handTiles[self.posInUser]
        self.visibleTile = [0 for i in range(38)]
        self.doraNum = 1
        self.paishan = roundData.paishan
        for i in self.handtile:
            self.visibleTile[Tile.tileToValue(i)] += 1
        if self.playernum == 3:
            self.visibleTile[Tile.tileToValue(self.paishan[-9])] += 1
        else:
            self.visibleTile[Tile.tileToValue(self.paishan[-5])] += 1

    def deal(self, item: Item):
        if item.playername != self.playername:
            return
        self.handtile.append(item.tile)
        self.visibleTile[Tile.tileToValue(item.tile)] += 1

    def discard(self, item: Item):
        if item.playername == self.playername:
            self.handtile.remove(item.tile)
            # todo check
            return
        self.visibleTile[Tile.tileToValue(item.tile)] += 1

    def babei(self, item: Item):
        if item.playername == self.playername:
            return
        self.visibleTile[34] += 1

    def simulateRound(self, roundData: Round):
        self.initround(roundData)
        for i in roundData.itemList:
            i: Item
            if i.op == 1:
                self.deal(i)
            if i.op == 2:
                self.discard(i)
            if i.op == 10:
                self.babei(i)
