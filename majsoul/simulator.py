from majsoul.record import *
from majsoul.parser import *
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
        for i in range(len(self.handtile)):
            if self.handtile[i] in ['0s','0m','0p']:
                self.handtile[i]=Tile.valueToTile(Tile.tileToValue(self.handtile[i]))
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
        if item.playername == self.playername:
            self.handtile.remove(item.tile)
            # todo check
            # todo richi
            return
        self.visibleTile[Tile.tileToValue(item.tile)] += 1

    def discard(self, item: Item):
        if item.playername != self.playername:
            return
        if item.tile in ['0s', '0m', '0p']:
            self.handtile.append(Tile.valueToTile(Tile.tileToValue(item.tile)))
        else:
            self.handtile.append(item.tile)
        self.handtile.sort(key=Tile.tileToValue)
        self.visibleTile[Tile.tileToValue(item.tile)] += 1


    def babei(self, item: Item):
        if item.playername == self.playername:
            return
        self.visibleTile[34] += 1

    def chi(self, item: Item):
        if item.playername == self.playername:
            if item.eatstatus == 1:
                self.handtile.remove(Tile.nextTile(item.tile))
                self.handtile.remove(Tile.nextTile(Tile.nextTile(item.tile)))
            if item.eatstatus == 2:
                self.handtile.remove(Tile.nextTile(item.tile))
                self.handtile.remove(Tile.prevTile(item.tile))
            if item.eatstatus == 3:
                self.handtile.remove(Tile.prevTile(item.tile))
                self.handtile.remove(Tile.prevTile(Tile.prevTile(item.tile)))
            return
        else:
            if item.eatstatus == 1:
                self.visibleTile[Tile.tileToValue(Tile.nextTile(item.tile))] += 1
                self.visibleTile[Tile.tileToValue(Tile.nextTile(Tile.nextTile(item.tile)))] += 1
            if item.eatstatus == 2:
                self.visibleTile[Tile.tileToValue(Tile.nextTile(item.tile))] += 1
                self.visibleTile[Tile.tileToValue(Tile.prevTile(item.tile))] += 1
            if item.eatstatus == 3:
                self.visibleTile[Tile.tileToValue(Tile.prevTile(item.tile))] += 1
                self.visibleTile[Tile.tileToValue(Tile.prevTile(Tile.prevTile(item.tile)))] += 1

    def peng(self, item: Item):
        if item.playername == self.playername:
            self.handtile.remove(item.tile)
            self.handtile.remove(item.tile)
            return
        self.visibleTile[Tile.tileToValue(item.tile)] += 2

    def gang(self, item: Item):
        self.doraNum += 1
        if self.playernum == 3:
            self.visibleTile[Tile.tileToValue(self.paishan[-7 - 2 * self.doraNum])] += 1
        else:
            self.visibleTile[Tile.tileToValue(self.paishan[-3 - 2 * self.doraNum])] += 1
        if item.playername == self.playername:
            self.handtile.remove(item.tile)
            self.handtile.remove(item.tile)
            self.handtile.remove(item.tile)
            return
        self.visibleTile[Tile.tileToValue(item.tile)] += 3

    def addGang(self, item: Item):
        self.doraNum += 1
        if self.playernum == 3:
            self.visibleTile[Tile.tileToValue(self.paishan[-7 - 2 * self.doraNum])] += 1
        else:
            self.visibleTile[Tile.tileToValue(self.paishan[-3 - 2 * self.doraNum])] += 1
        if item.playername == self.playername:
            self.handtile.remove(item.tile)
            return
        else:
            self.visibleTile[Tile.tileToValue(item.tile)] += 3

    def anGang(self, item: Item):
        self.doraNum += 1
        if self.playernum == 3:
            self.visibleTile[Tile.tileToValue(self.paishan[-7 - 2 * self.doraNum])] += 1
        else:
            self.visibleTile[Tile.tileToValue(self.paishan[-3 - 2 * self.doraNum])] += 1
        if item.playername == self.playername:
            self.handtile.remove(item.tile)
            self.handtile.remove(item.tile)
            self.handtile.remove(item.tile)
            self.handtile.remove(item.tile)
            return
        else:
            self.visibleTile[Tile.tileToValue(item.tile)] += 4

    def simulateRound(self, roundData: Round):
        self.initround(roundData)
        print('new round!!!')
        for i in roundData.itemList:
            print(self.handtile)
            #print(self.visibleTile)
            if i.op.value == 1:
                self.deal(i)
            if i.op.value == 2:
                self.discard(i)
            if i.op.value == 10:
                self.babei(i)
            if i.op.value == -1:
                self.chi(i)
            if i.op.value == -2:
                self.peng(i)
            if i.op.value == -3:
                self.gang(i)
            if i.op.value == -4:
                self.addGang(i)
            if i.op.value == -5:
                self.anGang(i)
            if i.op.value == 0 or i.op.value == -10:
                pass

if __name__ == "__main__":
    a = parseFromBase64('../test/b643.txt')
    a.print()
    b=simulator(a,'||||||')
    b.simulate()