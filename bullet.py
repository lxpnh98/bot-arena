import pygame

from vector import Vector

class Bullet:
    def __init__(self, owner, pos, velocity, damage=1, size=3):
        self.owner = owner
        self.pos = pos
        self.damage = damage
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
        
