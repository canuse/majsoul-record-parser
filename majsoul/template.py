class games:
    def __init__(self, uuid):
        self.url = 'https://www.majsoul.com/1/?paipu=' + uuid
        self.game = []

    def __str__(self):
        return self.url


class game:
    def __init__(self, name):
        self.name = name
        self.round = []

    def __str__(self):
        return self.name


class round:
    def __init__(self, somebody_richii, wrong_rate, melds, hand, your_choice, expected_choice, good_choice, yxh, xh,
                 xun):
        self.yxh = yxh
        self.xh = xh
        self.good_choice = good_choice
        self.your_choice = your_choice

        self.hand = hand
        self.melds = melds
        self.wrong_rate = wrong_rate
        self.somebody_richii = somebody_richii
        self.expected_choice = expected_choice
        self.xun = xun

    def __str__(self):
        return str(self.xun)
