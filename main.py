import sys
import random
import pygame

from vector import Vector
import world
import bot 
import components
import player

pygame.init()

class Build:
    NORMAL=0
    TANK=1
    LIGHT=2
    ULTRA_TANK=3
    ULTRA_LIGHT=4

def add_rand_bot(player, screen_size, bot_color, build=0):
    if build == Build.NORMAL:
        b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                    components.Chasis(None, 5, None),
                    color=bot_color)
        b.chasis.addBody(components.Body(None, 17, 10, 10))
        b.chasis.body.addWeapon(components.Weapon(None, bullet_size=4, bullet_speed=110, bullet_damage=1, reload_time=1))
    if build == Build.TANK:
        b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                    components.Chasis(None, 5, None),
                    color=bot_color)
        b.chasis.addBody(components.Body(None, 30, 15, 17.5))
        b.chasis.body.addWeapon(components.Weapon(None, bullet_size=6, bullet_speed=70, bullet_damage=3.25, reload_time=2.5))
    if build == Build.LIGHT:
        b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                    components.Chasis(None, 5, None),
                    color=bot_color)
        b.chasis.addBody(components.Body(None, 10, 7, 7.5))
        b.chasis.body.addWeapon(components.Weapon(None, bullet_size=3, bullet_speed=150, bullet_damage=0.2, reload_time=0.3))
    if build == Build.ULTRA_TANK:
        b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                    components.Chasis(None, 5, None),
                    color=bot_color)
        b.chasis.addBody(components.Body(None, 50, 40, 50))
        b.chasis.body.addWeapon(components.Weapon(None, bullet_size=15, bullet_speed=40, bullet_damage=15, reload_time=6))
    if build == Build.ULTRA_LIGHT:
        b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                    components.Chasis(None, 5, None),
                    color=bot_color)
        b.chasis.addBody(components.Body(None, 7, 5, 3))
        b.chasis.body.addWeapon(components.Weapon(None, bullet_size=2, bullet_speed=300, bullet_damage=0.05, reload_time=0.1))
    player.addBot(b)

def main():
    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    fps = 60
    dt = 0.0

    w = world.World(Vector(*screen_size))

    p1 = player.Player(None)
    p2 = player.Player(None)
    p3 = player.Player(None)
    p4 = player.Player(None)

    add_rand_bot(p1, screen_size, (255, 0, 0), build=Build.NORMAL)
    add_rand_bot(p1, screen_size, (255, 0, 0), build=Build.NORMAL)
    add_rand_bot(p1, screen_size, (255, 0, 0), build=Build.NORMAL)
    add_rand_bot(p1, screen_size, (255, 0, 0), build=Build.ULTRA_LIGHT)

    add_rand_bot(p2, screen_size, (0, 255, 0), build=Build.ULTRA_TANK)
    add_rand_bot(p2, screen_size, (0, 255, 0), build=Build.LIGHT)
    add_rand_bot(p2, screen_size, (0, 255, 0), build=Build.LIGHT)
    add_rand_bot(p2, screen_size, (0, 255, 0), build=Build.LIGHT)

    add_rand_bot(p3, screen_size, (0, 0, 255), build=Build.TANK)
    add_rand_bot(p3, screen_size, (0, 0, 255), build=Build.TANK)
    add_rand_bot(p3, screen_size, (0, 0, 255), build=Build.TANK)
    add_rand_bot(p3, screen_size, (0, 0, 255), build=Build.LIGHT)

    add_rand_bot(p4, screen_size, (0, 0, 0),   build=Build.TANK)
    add_rand_bot(p4, screen_size, (0, 0, 0),   build=Build.TANK)
    add_rand_bot(p4, screen_size, (0, 0, 0),   build=Build.NORMAL)
    add_rand_bot(p4, screen_size, (0, 0, 0),   build=Build.ULTRA_LIGHT)

    w.addPlayer(p1)
    w.addPlayer(p2)
    w.addPlayer(p3)
    w.addPlayer(p4)

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
        pygame.display.set_caption("FPS: %i" % (1 / dt))
    #pygame.display.quit()
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
