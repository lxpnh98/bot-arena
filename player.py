class Player:
    def __init__(self, name):
        self.name = name
        self.bots = []

    def addBot(self, bot):
        bot.player = self
        self.bots.append(bot)

class HumanPlayer(Player):
    def __init__(self, name, init_cash=0, init_inventory=[]):
        self.cash = init_cash
        self.inventory = inventory
        super().__init__(name)
