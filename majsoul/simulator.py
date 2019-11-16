from majsoul.parser import *
from majsoul.reasoner import *
from majsoul.template import *


class simulator:
    def __init__(self, record: Game, username):
        self.record = record
        self.playername = username
        self.users = record.players.playernames
        self.posInUser = self.users.index(self.playername)
        self.gametype = 0
        self.playernum = record.players.num
        self.isrichi = False
        self.report = [games(record.uuid)]
        self.melds = []

    def simulate(self):
        for i in self.record.roundList:
            self.simulateRound(i)

    def initround(self, roundData: Round):
        self.handtile = roundData.handTiles[self.posInUser]
        for i in range(len(self.handtile)):
            if self.handtile[i] in ['0s', '0m', '0p']:
                self.handtile[i] = Tile.valueToTile(Tile.tileToValue(self.handtile[i]))
        self.visibleTile = [0 for i in range(38)]
        self.doraNum = 1
        self.paishan = roundData.paishan
        self.isrichi = False
        self.melds = []
        self.game = game(str(roundData))
        for i in self.handtile:
            self.visibleTile[Tile.tileToValue(i)] += 1
        if self.playernum == 3:
            self.visibleTile[Tile.tileToValue(self.paishan[-9])] += 1
        else:
            self.visibleTile[Tile.tileToValue(self.paishan[-5])] += 1

    def deal(self, item: Item):
        if item.isliqi == 1:
            self.isrichi = True
        if item.playername == self.playername:
            xh, choices = self.calculateBest()
            allchoice = [i[0] for i in choices]
            goodchoice = []
            for i in choices:
                if i[1] == choices[0][1]:
                    goodchoice.append(i[0])
            cc = []
            for i in choices:
                tmp = ''
                for j in i[-1]:
                    tmp = tmp + Tile.tileToUtf(Tile.valueToTile(j))
                cc.append((Tile.tileToUtf(i[0]), i[1], i[2], tmp))
            if Tile.valueToTile(Tile.tileToValue(item.tile)) in allchoice:
                invisibleTiles = 0
                for i in range(38):
                    if i in [0, 10, 20, 30]:
                        continue
                    if self.playernum == 3:
                        if i in [2, 3, 4, 5, 6, 7, 8]:
                            continue
                    invisibleTiles += 4 - self.visibleTile[i]
                bestRateP = choices[0][1]
                yourRateP = choices[allchoice.index(Tile.valueToTile(Tile.tileToValue(item.tile)))][1]
                bestRate = 1 - (1 - bestRateP / invisibleTiles) * (1 - bestRateP / (invisibleTiles - 1))
                yourRate = 1 - (1 - yourRateP / invisibleTiles) * (1 - yourRateP / (invisibleTiles - 1))
                wrong_rate = 1 - yourRate / bestRate
                melds = []
                for i in self.melds:
                    melds.extend(i)
                ht = ''
                for i in self.handtile:
                    ht = ht + Tile.tileToUtf(i)

                tround = round(self.isrichi, wrong_rate, melds, ht,
                               Tile.tileToUtf(item.tile), [Tile.tileToUtf(i) for i in allchoice],
                               [Tile.tileToUtf(i) for i in goodchoice],
                               choices[allchoice.index(Tile.valueToTile(Tile.tileToValue(item.tile)))][2],
                               choices[0][2], len(self.game.round) + 1, bestRateP, yourRateP, cc)
                self.game.round.append(tround)
                print(
                    'Your choice:{0},{1} Best choices:{2},{3}'.format(item.tile, choices[
                        allchoice.index(Tile.valueToTile(Tile.tileToValue(item.tile)))][1],
                                                                      choices[0][0], choices[0][1]))
            else:
                invisibleTiles = 0
                for i in range(38):
                    if i in [0, 10, 20, 30]:
                        continue
                    if self.playernum == 3:
                        if i in [2, 3, 4, 5, 6, 7, 8]:
                            continue
                    invisibleTiles += 4 - self.visibleTile[i]
                bestRateP = choices[0][1]
                melds = []
                for i in self.melds:
                    melds.extend(i)
                ht = ''
                for i in self.handtile:
                    ht = ht + Tile.tileToUtf(i)
                tround = round(self.isrichi, 1, melds, ht,
                               Tile.tileToUtf(item.tile), [Tile.tileToUtf(i) for i in allchoice],
                               [Tile.tileToUtf(i) for i in goodchoice], choices[0][2] + 1, choices[0][2],
                               len(self.game.round) + 1,
                               bestRateP, -1, cc)
                self.game.round.append(tround)
                print('wrong')
            # todo check
            print(item.tile, self.handtile)
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            return
        self.visibleTile[Tile.tileToValue(item.tile)] += 1

    def discard(self, item: Item):
        if item.playername != self.playername:
            return
        if item.tile in ['0s', '0m', '0p']:
            self.handtile.append(Tile.valueToTile(Tile.tileToValue(item.tile)))
        else:
            self.handtile.append(Tile.valueToTile(Tile.tileToValue(item.tile)))
        self.handtile.sort(key=Tile.tileToValue)
        self.visibleTile[Tile.tileToValue(item.tile)] += 1

    def babei(self, item: Item):
        if item.playername == self.playername:
            self.handtile.remove('4z')
            self.melds.append((Tile.tileToUtf('4z')))
            return
        self.visibleTile[34] += 1

    def chi(self, item: Item):
        if item.playername == self.playername:
            if item.eatstatus == 1:
                self.handtile.remove(Tile.nextTile(item.tile))
                self.handtile.remove(Tile.nextTile(Tile.nextTile(item.tile)))
                self.melds.append((Tile.tileToUtf(item.tile), Tile.tileToUtf(Tile.nextTile(item.tile)),
                                   Tile.tileToUtf(Tile.nextTile(Tile.nextTile(item.tile)))))
            if item.eatstatus == 2:
                self.handtile.remove(Tile.nextTile(item.tile))
                self.handtile.remove(Tile.prevTile(item.tile))
                self.melds.append((Tile.tileToUtf(item.tile), Tile.tileToUtf(Tile.nextTile(item.tile)),
                                   Tile.tileToUtf(Tile.prevTile(item.tile))))
            if item.eatstatus == 3:
                self.handtile.remove(Tile.prevTile(item.tile))
                self.handtile.remove(Tile.prevTile(Tile.prevTile(item.tile)))
                self.melds.append((Tile.tileToUtf(item.tile), Tile.tileToUtf(Tile.prevTile(item.tile)),
                                   Tile.tileToUtf(Tile.prevTile(Tile.prevTile(item.tile)))))
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
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.melds.append((Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile)))
            return
        self.visibleTile[Tile.tileToValue(item.tile)] += 2

    def gang(self, item: Item):
        self.doraNum += 1
        if self.playernum == 3:
            self.visibleTile[Tile.tileToValue(self.paishan[-7 - 2 * self.doraNum])] += 1
        else:
            self.visibleTile[Tile.tileToValue(self.paishan[-3 - 2 * self.doraNum])] += 1
        if item.playername == self.playername:
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.melds.append((Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile),
                               Tile.tileToUtf(item.tile)))
            return
        self.visibleTile[Tile.tileToValue(item.tile)] += 3

    def addGang(self, item: Item):
        self.doraNum += 1
        if self.playernum == 3:
            self.visibleTile[Tile.tileToValue(self.paishan[-7 - 2 * self.doraNum])] += 1
        else:
            self.visibleTile[Tile.tileToValue(self.paishan[-3 - 2 * self.doraNum])] += 1
        if item.playername == self.playername:
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.melds.remove((Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile)))
            self.melds.append((Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile),
                               Tile.tileToUtf(item.tile)))
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
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.handtile.remove(Tile.valueToTile(Tile.tileToValue(item.tile)))
            self.melds.append(
                (Tile.tileToUtf('8z'), Tile.tileToUtf(item.tile), Tile.tileToUtf(item.tile), Tile.tileToUtf('8z')))
            return
        else:
            self.visibleTile[Tile.tileToValue(item.tile)] += 4

    def calculateBest(self):
        a = reasoner()
        choices, xh = a.discardTileList([Tile.tileToValue(i) for i in self.handtile], self.playernum)
        bestChoices = []
        for i in choices.keys():
            tmp = 0
            for j in choices[i][0]:
                tmp += 4 - self.visibleTile[j]
            bestChoices.append((i, tmp, choices[i][1], choices[i][0]))
        bestChoices.sort(key=lambda x: x[1], reverse=True)
        return xh, bestChoices

    def simulateRound(self, roundData: Round):
        self.initround(roundData)
        print('new round!!!')
        for i in roundData.itemList:
            # print(self.handtile)
            # print(self.visibleTile)
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
                self.report[0].game.append(self.game)


if __name__ == "__main__":
    a = parseFromBase64('../test/b643.txt')
    # a.print()
    b = simulator(a, '||||||')
    b.simulate()
