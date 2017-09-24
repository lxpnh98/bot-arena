class World:
    def __init__(self, size):
        self.bots = []
        self.bullets = []
        self.size = size

    def addBot(self, bot):
        self.bots.append(bot)

    def update(self, dt):
        for b in self.bots:
            bullet = b.update(dt, self.bots)
            if bullet != None:
                self.bullets.append(bullet)
        for b in self.bullets:
            b.update(dt)

        for b1 in self.bots:
            for b2 in self.bots:
                if b1 is not b2 and b1.collidesWith(b2):
                    self.separate(b1, b2)
            self.putInBounds(b1)

        for bullet in self.bullets:
            for bot in self.bots:
                if bullet.owner is not bot and bullet.collidesWith(bot):
                    bot.chasis.hp -= bullet.damage
                    self.bullets.remove(bullet)
                    if bot.getHP() <= 0.0:
                        self.bots.remove(bot)
            if self.isOutOfBounds(bullet.pos):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

    def display(self, screen, pos):
        for b in self.bots:
            b.display(screen, pos)
        for b in self.bullets:
            b.display(screen, pos)

    def isOutOfBounds(self, pos):
        if pos.x < 0.0 or pos.x > self.size.x:
            return True
        if pos.y < 0.0 or pos.y > self.size.y:
            return True
        return False

    def putInBounds(self, bot):
        d1 = bot.pos.x - bot.size 
        d2 = bot.pos.x + bot.size 
        if d1 < 0:
            bot.pos.x -= d1
        elif d2 > self.size.x:
            bot.pos.x -= d2 - self.size.x

        d3 = bot.pos.y - bot.size 
        d4 = bot.pos.y + bot.size 
        if d3 < 0:
            bot.pos.y -= d3
        elif d4 > self.size.y:
            bot.pos.y -= d4 - self.size.y

    def separate(self, b1, b2):
        collision_vector = b2.pos - b1.pos
        overlap_vector = collision_vector - collision_vector.normalize() * (b1.size + b2.size)
        b2.pos -= overlap_vector * (1/2.)
        b1.pos += overlap_vector * (1/2.)
