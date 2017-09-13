class World:
    def __init__(self):
        self.bots = []

    def add_bot(self, bot):
        self.bots.append(bot)

    def display(self, screen, pos):
        for b in self.bots:
            b.display(screen, pos)
