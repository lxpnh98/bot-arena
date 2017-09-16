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
    w.add_bot(bot.Bot(Vector(10, 10)))
    w.bots[0].set_velocity((5.0, 3.0))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
        w.bots[0].accelerate(Vector(10.0, 0) * dt)
        w.update(dt)
        screen.fill(pygame.color.Color("white"))
        w.display(screen, Vector(50, 40))
        pygame.display.update()
        dt = clock.tick(fps) / 1000.

if __name__ == "__main__":
    main()
