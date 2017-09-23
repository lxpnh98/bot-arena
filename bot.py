import pygame

from vector import *
from components import *
from bullet import *

class Bot:
    def __init__(self, pos, chasis=None, body=None, size=10):
        self.pos = pos
        self.chasis = (chasis if chasis != None else Chasis(self, 0, 5))
        self.body = (body if body != None else Body(self, 0))
        self.size = size
        self.velocity = Vector(0.0, 0.0)


    def update(self, dt, bot_list):
        self.body.update(dt)

        # Decision making
        min_length_bot = None
        min_length = None
        for b in bot_list:
            if b is not self:
                b_dist = (b.pos - self.pos).length()
                if min_length_bot == None or min_length > b_dist:
                    min_length_bot = b
                    min_length = b_dist
        
        self.pos += self.velocity * dt
        if min_length_bot != None:
            shoot_direction = min_length_bot.pos - self.pos
            self.body.weapon.turn(shoot_direction.angle())
            return self.shoot()
        else:
            return None

    def display(self, screen, pos):
        pygame.draw.circle(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), self.size, 0)
        weapon_pos = (self.pos + pos) + self.body.weapon.getDirection() * (self.size + 2)
        pygame.draw.line(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), weapon_pos.toInt().toTuple(), 1)

    def setVelocity(self, velocity):
        if type(velocity) == Vector:
            self.velocity = velocity
        else:
            self.velocity = Vector(*velocity)

    def getHP(self):
        return self.chasis.hp

    def accelerate(self, acceleration):
        if type(acceleration) == Vector:
            self.velocity += acceleration
        else:
            self.velocity += Vector(*acceleration)

    def shoot(self):
        return self.body.weapon.shoot()

    def collidesWith(self, bot):
        if (bot.pos - self.pos).dist2() <= (bot.size + self.size)**2:
            return True
        else:
            return False
