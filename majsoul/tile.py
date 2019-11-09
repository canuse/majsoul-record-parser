class Tile:
    def __init__(self, tile):
        self.name = tile
        if 'm' in tile:
            if tile[0] == '0':
                self.value = 5
            else:
                self.value = int(tile[0])
        elif 's' in tile:
            if tile[0] == '0':
                self.value = 15
            else:
                self.value = int(tile[0]) + 10
        elif 'p' in tile:
            if tile[0] == '0':
                self.value = 25
            else:
                self.value = int(tile[0]) + 20
        else:
            self.value = int(tile[0]) + 30
