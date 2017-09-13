import pygame

class Chasis:
    def __init__(self, capacity):
        self.capacity = capacity

class Bot:
    def __init__(self, pos, chasis):
        self.chasis = chasis
        self.pos = pos

    def display(self, screen, pos):
        pygame.draw.circle(screen, pygame.color.Color("black"), (self.pos + pos).tuple(), 10, 0)
