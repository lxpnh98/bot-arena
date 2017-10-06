class Player:
    _player_id = 0
    def __init__(self, name):
        self.id = Player._player_id
        Player._player_id += 1
        self.name = name
        self.bots = []

    def addBot(self, bot):
        self.bots.append(bot)

