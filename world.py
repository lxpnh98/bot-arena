class World:
    def __init__(self, size):
        self.bots = []
        self.bullets = []
        self.size = size

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
                    bot.chasis.hp -= bullet.damage
                    self.bullets.remove(bullet)
                    if bot.chasis.hp <= 0.0:
                        self.bots.remove(bot)
            if self.isOutOfBounds(bullet.pos):
                self.bullets.remove(bullet)

    def display(self, screen, pos):
        for b in self.bots:
            b.display(screen, pos)
        for b in self.bullets:
            b.display(screen, pos)

    def isOutOfBounds(self, pos):
        if pos.x < 0.0 or pos.x > self.size[0]:
            return True
        if pos.y < 0.0 or pos.y > self.size[1]:
            return True
        return False
