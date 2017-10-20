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
    ULTRA_LIGHT=0
    LIGHT=1
    NORMAL=2
    TANK=3
    ULTRA_TANK=4

class Main:
    MAIN=0
    PLANNING=0
    PLAYING=1
    def __init__(self):
        self.screen_size = (640, 480)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen_state = Main.PLAYING
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0.0
        self.create_world()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.display()
            self.tick()
        self.exit()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        if self.screen_state == Main.PLAYING:
            self.world.update(self.dt)

    def display(self):
        self.screen.fill(pygame.color.Color("white"))
        if self.screen_state == Main.PLAYING:
            self.world.display(self.screen, Vector(0, 0))

    def tick(self):
        pygame.display.update()
        self.dt = self.clock.tick(self.fps) / 1000.
        pygame.display.set_caption("FPS: %i" % (1 / self.dt))

    def exit(self):
        pygame.quit()
        sys.exit(0)

    def create_world(self):
        self.world = world.World(Vector(*self.screen_size))

        p1 = player.HumanPlayer(None)
        p2 = player.Player(None)
        p3 = player.Player(None)
        p4 = player.Player(None)

        self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
        self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
        self.add_bot(p1,self.screen_size, (255, 0, 0), build=Build.NORMAL)
        self.add_bot(p1,self.screen_size, (255, 0, 0), build=Build.ULTRA_TANK)

        self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.LIGHT)
        self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.LIGHT)
        self.add_bot(p2,self.screen_size, (0, 255, 0), build=Build.ULTRA_LIGHT)
        self.add_bot(p2,self.screen_size, (0, 255, 0), build=Build.TANK)

        self.world.addPlayer(p1)
        self.world.addPlayer(p2)

    def add_bot(self, player, screen_size, bot_color, build=0):
        if build == Build.ULTRA_LIGHT:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=7, weight=4, hp=4))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=2, bullet_speed=300, bullet_damage=0.05, reload_time=0.1))
        if build == Build.LIGHT:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=10, weight=7, hp=7))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=3, bullet_speed=140, bullet_damage=0.2, reload_time=0.3))
        if build == Build.NORMAL:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=17, weight=10, hp=10))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=4, bullet_speed=110, bullet_damage=1, reload_time=1))
        if build == Build.TANK:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=30, weight=15, hp=17.5))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=6, bullet_speed=70, bullet_damage=3.25, reload_time=2.5))
        if build == Build.ULTRA_TANK:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=50, weight=40, hp=50))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=15, bullet_speed=40, bullet_damage=15, reload_time=6))
        player.addBot(b)

if __name__ == "__main__":
    Main().run()
