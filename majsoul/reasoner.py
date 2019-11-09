import numpy as np


def relu(a, b):
    if a > b:
        return 0
    return b - a


class reasoner:
    def __init__(self):
        self.xh = 100
        self.saveList = []

    @staticmethod
    def xhpd(singleNumber, quetou, doubleNumber, tripleNuber, tileList):
        def _qidui(tileList):
            uniquePair = 0
            tlist = np.array(tileList)
            key = np.unique(tlist)
            for i in key:
                if tlist[tlist == i].size >= 2:
                    uniquePair += 1
            return uniquePair

        def _guoshi(tileList):
            yaojiu_num = 0
            tlist = np.array(tileList)
            double = False
            key = (1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37)
            for i in key:
                tmp = tlist[tlist == i].size
                if tmp == 1:
                    yaojiu_num += 1
                if tmp > 1:
                    yaojiu_num += 1
                    if not double:
                        yaojiu_num += 1
                        double = True
            return yaojiu_num

        triple = (singleNumber + 2 * doubleNumber + 2 * quetou) // 3 + tripleNuber

        if triple == 4:
            # menqing check qidui and guoshi
            axh = 14 - _guoshi(tileList)
            bxh = 7 - _qidui(tileList)
        else:
            axh = 100
            bxh = 100

        cxh = 100
        if quetou == 0:
            cxh = triple + 1 - tripleNuber + relu(doubleNumber, triple - tripleNuber)
        if quetou == 1:
            cxh = triple - tripleNuber + relu(doubleNumber, triple - tripleNuber)
        if quetou >= 2:
            cxh = triple - tripleNuber + relu(doubleNumber + quetou - 1, triple - tripleNuber)

        minxh = min(axh, bxh, cxh)
        # print(axh,bxh,cxh,sig_num, quetou, bi_num, tri_num)
        return minxh

    def caipai(self, tileList):
        self.xh = 100
        self.saveList = tileList
        tlist = np.array(tileList)
        self._caipaidfs(0, 0, 0, 0, tlist)
        return self.xh

    def _caipaidfs(self, singleNumber, quetou, doubleNumber, tripleNumber, tileList):
        tileList.sort()
        length = tileList.size
        if self.xh == 0:
            return
        if singleNumber > self.xh:
            return
        if length == 0:
            xh = self.xhpd(singleNumber, quetou, doubleNumber, tripleNumber, self.saveList)
            if xh < self.xh:
                self.xh = xh
                return

        # kezi
        if length >= 3 and tileList[0] == tileList[1] and tileList[1] == tileList[2]:
            self._caipaidfs(singleNumber, quetou, doubleNumber, tripleNumber + 1, tileList[3:])
        # sunzi
        unique_tile_list = np.unique(tileList)
        length2 = unique_tile_list.size
        if length2 >= 3 and unique_tile_list[0] == unique_tile_list[1] - 1 and unique_tile_list[1] == \
                unique_tile_list[2] - 1 and unique_tile_list[2] < 30:
            self._caipaidfs(singleNumber, quetou, doubleNumber, tripleNumber + 1, np.delete(tileList, (
                np.where(tileList == unique_tile_list[0])[0][0], np.where(tileList == unique_tile_list[1])[0][0],
                np.where(tileList == unique_tile_list[2])[0][0])))
        # duizi
        if length >= 2 and tileList[0] == tileList[1]:
            self._caipaidfs(singleNumber, quetou + 1, doubleNumber, tripleNumber, tileList[2:])
        # dazi1
        if length2 >= 2 and unique_tile_list[0] == unique_tile_list[1] - 1 and unique_tile_list[1] < 30:
            self._caipaidfs(singleNumber, quetou, doubleNumber + 1, tripleNumber, np.delete(tileList, (
                np.where(tileList == unique_tile_list[0])[0][0], np.where(tileList == unique_tile_list[1])[0][0])))
        # dazi2
        if length2 >= 2 and ((unique_tile_list[0] + 2) in unique_tile_list) and unique_tile_list[
            0] % 10 != 9 and unique_tile_list[0] < 30:
            self._caipaidfs(singleNumber, quetou, doubleNumber + 1, tripleNumber, np.delete(tileList, (
                np.where(tileList == unique_tile_list[0])[0][0],
                np.where(tileList == unique_tile_list[0] + 2)[0][0])))
        # danzhang
        if length >= 1:
            self._caipaidfs(singleNumber + 1, quetou, doubleNumber, tripleNumber, tileList[1:])
