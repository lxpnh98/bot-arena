class World:
    def __init__(self):
        self.bots = []
        self.bullets = []

    def add_bot(self, bot):
        self.bots.append(bot)

    def update(self, dt):
        for b in self.bots:
            bullet = b.update(dt)
            if bullet != None:
                self.bullets.append(bullet)
        for b in self.bullets:
            b.update(dt)

    def display(self, screen, pos):
        for b in self.bots:
            b.display(screen, pos)
        for b in self.bullets:
            b.display(screen, pos)
