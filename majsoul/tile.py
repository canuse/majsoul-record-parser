class Tile:
    def __init__(self, tile):
        self.name = tile
        if 'm' in tile:
            if tile[0] == '0':
                self.value = 5
            else:
                self.value = int(tile[0])
        elif 'p' in tile:
            if tile[0] == '0':
                self.value = 15
            else:
                self.value = int(tile[0]) + 10
        elif 's' in tile:
            if tile[0] == '0':
                self.value = 25
            else:
                self.value = int(tile[0]) + 20
        else:
            self.value = int(tile[0]) + 30

    @staticmethod
    def tileToValue(tile):
        if 'm' in tile:
            if tile[0] == '0':
                return 5
            else:
                return int(tile[0])
        elif 'p' in tile:
            if tile[0] == '0':
                return 15
            else:
                return int(tile[0]) + 10
        elif 's' in tile:
            if tile[0] == '0':
                return 25
            else:
                return int(tile[0]) + 20
        else:
            return int(tile[0]) + 30

    @staticmethod
    def valueToTile(value):
        if value < 10:
            return str(value) + 'm'
        elif value < 20:
            return str(value - 10) + 'p'
        elif value < 30:
            return str(value - 20) + 's'
        else:
            return str(value - 30) + 'z'

    @staticmethod
    def nextTile(tile):
        return str(int(tile[0]) + 1) + tile[1]

    @staticmethod
    def prevTile(tile):
        return str(int(tile[0]) - 1) + tile[1]
