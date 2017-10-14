class World:
    def __init__(self, size):
        self.players = []
        self.bullets = []
        self.size = size

    def addPlayer(self, player):
        self.players.append(player)

    def update(self, dt):
        bots = []
        for p in self.players:
            for b in p.bots:
                bots.append(b)
        #bots = [p.bots for p in self.players]
        bot_positions = list(map(lambda b: b.getPos(), bots))
        world_distances = [
            sum(map(lambda v: v.dist2(), bot_positions)), # Top left
            sum(map(lambda v: (v - self.size).dist2(), bot_positions)), # Bottom right
            sum(map(lambda v: (v - self.size * (1 / 2.)).dist2(), bot_positions)), # Center
            sum(map(lambda v: (v - self.size.widthVector()).dist2(), bot_positions)), # Top right
            sum(map(lambda v: (v - self.size.heightVector()).dist2(), bot_positions)), # Bottom left
            sum(map(lambda v: (v - (self.size.widthVector() * (1/2.))).dist2(), bot_positions)), # Top center
            sum(map(lambda v: (v - (self.size.heightVector() * (1/2.))).dist2(), bot_positions)), # Left center
            sum(map(lambda v: (v - (self.size.widthVector() * (1/2.) + self.size.heightVector())).dist2(), bot_positions)), # Bottom center
            sum(map(lambda v: (v - (self.size.heightVector() * (1/2.) + self.size.widthVector())).dist2(), bot_positions)) # Right center
        ]

        for b in bots:
            bullet = b.update(dt, bots, self.size, world_distances)
            if bullet != None:
                self.bullets.append(bullet)
        for b in self.bullets:
            b.update(dt)

        for b1 in bots:
            for b2 in bots:
                if b1 is not b2 and b1.collidesWith(b2):
                    self.separate(b1, b2)
            self.putInBounds(b1)

        for bullet in self.bullets:
            for p in self.players:
                for bot in p.bots:
                    if bullet.owner is not bot and bullet.collidesWith(bot):
                        bot.chasis.body.hp -= bullet.damage
                        self.bullets.remove(bullet)
                        if bot.getHP() <= 0.0:
                            p.bots.remove(bot)
                if self.isOutOfBounds(bullet.pos):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

    def display(self, screen, pos):
        for b in self.bullets:
            b.display(screen, pos)
        for p in self.players:
            for b in p.bots:
                b.display(screen, pos)

    def isOutOfBounds(self, pos):
        if pos.x < 0.0 or pos.x > self.size.x:
            return True
        if pos.y < 0.0 or pos.y > self.size.y:
            return True
        return False

    def putInBounds(self, bot):
        d1 = bot.pos.x - bot.getSize()
        d2 = bot.pos.x + bot.getSize()
        if d1 < 0:
            bot.pos.x -= d1
        elif d2 > self.size.x:
            bot.pos.x -= d2 - self.size.x

        d3 = bot.pos.y - bot.getSize()
        d4 = bot.pos.y + bot.getSize()
        if d3 < 0:
            bot.pos.y -= d3
        elif d4 > self.size.y:
            bot.pos.y -= d4 - self.size.y

    def separate(self, b1, b2):
        collision_vector = b2.pos - b1.pos
        overlap_vector = collision_vector - collision_vector.normalize() * (b1.getSize() + b2.getSize())
        b2.pos -= overlap_vector * (1/2.)
        b1.pos += overlap_vector * (1/2.)
