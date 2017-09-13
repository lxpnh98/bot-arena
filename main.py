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

    w = world.World()
    w.add_bot(bot.Bot(Vector(10, 10), None))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
        screen.fill(pygame.color.Color("white"))
        w.display(screen, Vector(50, 40))
        pygame.display.update()
        dt = clock.tick(fps)

if __name__ == "__main__":
    main()
