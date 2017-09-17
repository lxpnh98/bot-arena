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

        for b1 in self.bots:
            for b2 in self.bots:
                if b1 is not b2 and b1.collidesWith(b2):
                    print("Bots collided.")

        for bullet in self.bullets:
            for bot in self.bots:
                if bullet.owner is not bot and bullet.collidesWith(bot):
                    print("Bullet and bot collided.")
                    self.bullets.remove(bullet)

    def display(self, screen, pos):
        for b in self.bots:
            b.display(screen, pos)
        for b in self.bullets:
            b.display(screen, pos)
