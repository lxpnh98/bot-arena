import sys
import random
import pygame

from vector import Vector
import world
import bot 
import components
import player

pygame.init()

def main():
    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    fps = 30
    dt = 0.0

    w = world.World(Vector(*screen_size))

    p1 = player.Player(None)
    p2 = player.Player(None)

    b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                components.Chasis(None, 5, None),
                color=(200, 200, 200))
    b.chasis.addBody(components.Body(None, 20, 10, 10))
    b.chasis.body.addWeapon(components.Weapon(None))
    p1.addBot(b)

    b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                components.Chasis(None, 5, None),
                color=(200, 200, 200))
    b.chasis.addBody(components.Body(None, 20, 10, 10))
    b.chasis.body.addWeapon(components.Weapon(None))
    p2.addBot(b)

    w.addPlayer(p1)
    w.addPlayer(p2)

    #for i in range(4):
    #    b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)), color=(30*i, 30*i, 30*i))
    #    b.setVelocity(Vector(random.random() - 0.5, random.random() - 0.5).dot(Vector(200.0, 200.0)))
    #    w.addBot(b)

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
        w.display(screen, Vector(0, 0))
        pygame.display.update()
        dt = clock.tick(fps) / 1000.
    #pygame.display.quit()
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
