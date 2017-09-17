import pygame

from vector import *

class Chasis:
    def __init__(self, bot, capacity):
        self.bot = bot
        self.capacity = capacity

class Body:
    def __init__(self, bot, weight):
        self.bot = bot
        self.weight = weight
        self.camera = None
        self.weapon = Weapon(bot)
        self.motor = Motor(bot)

    def update(self, dt):
        self.weapon.update(dt)

class Weapon:
    def __init__(self, bot, power=100, reload_time=1):
        self.bot = bot
        self.power = power
        self._reload_time = reload_time
        self._time_till_reload = None

    def update(self, dt):
        if self._time_till_reload != None:
            self._time_till_reload -= dt
            if self._time_till_reload < 0.0:
                self._time_till_reload = None
        
    def shoot(self, direction):
        if self._time_till_reload == None:
            self._time_till_reload = self._reload_time
            return Bullet(self.bot, self.bot.pos, direction.normalize() * self.power)

class Motor:
    def __init__(self, bot, torque=1):
        self.bot = bot
        self.torque = torque

class Bullet:
    def __init__(self, owner, pos, velocity, size=3):
        self.owner = owner
        self.pos = pos
        self.size = size
        self.velocity = (velocity if type(velocity) == Vector else Vector(*velocity))

    def update(self, dt):
        self.pos += self.velocity * dt

    def display(self, screen, pos):
        pygame.draw.circle(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), self.size, 0)

    def collidesWith(self, bot):
        if (bot.pos - self.pos).dist2() <= (bot.size + self.size)**2:
            return True
        else:
            return False
        
class Bot:
    def __init__(self, pos, chasis=None, body=None, size=10):
        self.pos = pos
        self.chasis = (chasis if chasis != None else Chasis(self, 0))
        self.body = (body if body != None else Body(self, 0))
        self.size = size
        self.velocity = Vector(0.0, 0.0)

    def update(self, dt):
        self.body.update(dt)
        self.pos += self.velocity * dt
        return self.shoot(self.velocity)

    def display(self, screen, pos):
        pygame.draw.circle(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), self.size, 0)

    def set_velocity(self, velocity):
        if type(velocity) == Vector:
            self.velocity = velocity
        else:
            self.velocity = Vector(*velocity)

    def accelerate(self, acceleration):
        if type(acceleration) == Vector:
            self.velocity += acceleration
        else:
            self.velocity += Vector(*acceleration)

    def shoot(self, direction):
        return self.body.weapon.shoot(direction)

    def collidesWith(self, bot):
        if (bot.pos - self.pos).dist2() <= (bot.size + self.size)**2:
            return True
        else:
            return False
