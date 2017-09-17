import random
import pygame
from vector import Vector
import world
import bot

pygame.init()

def main():
    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    fps = 30
    dt = 0.0

    w = world.World()
    for _ in range(4):
        b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)))
        b.set_velocity(Vector(random.random() - 0.5, random.random() - 0.5).dot(Vector(10.0, 10.0)))
        w.add_bot(b)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
        #w.bots[0].accelerate(Vector(10.0, 0) * dt)
        w.update(dt)
        screen.fill(pygame.color.Color("white"))
        w.display(screen, Vector(50, 40))
        pygame.display.update()
        dt = clock.tick(fps) / 1000.

if __name__ == "__main__":
    main()
