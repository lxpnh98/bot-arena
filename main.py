import sys
import random
import pygame

from pgu import text, gui as pgui

from vector import Vector

import campaign
import level
import world
import bot 
import components
import player

pygame.init()

def logRadioAction(arg):
    print("Hello, ")

def logCheckAction(arg):
    print("world!")

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
        self.screen_state = Main.MAIN
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0.0
        self.campaign = None
        self.init_gui()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.display()
            self.tick()
        self.exit(0)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running = False
            # pass event to gui
            self.gui.event(e)

    def update(self):
        if self.screen_state == Main.PLAYING:
            self.campaign.update(self.dt)

    def display(self):
        self.screen.fill(pygame.color.Color("white"))
        if self.screen_state == Main.PLAYING:
            self.campaign.display(self.screen, Vector(0, 0))
        # draw gui
        self.gui.paint(self.screen)

    def tick(self):
        pygame.display.update()
        self.dt = self.clock.tick(self.fps) / 1000.
        pygame.display.set_caption("FPS: %i" % (1 / self.dt))

    def exit(self, return_value):
        pygame.quit()
        sys.exit(return_value)

    def init_gui(self):
        font = pygame.font.SysFont("default", 18)
        fontBig = pygame.font.SysFont("default", 24)
        fontSub = pygame.font.SysFont("default", 20)

        self.gui = pgui.App()
        layout = pgui.Container(width=self.screen_size[0], height=self.screen_size[1])

        title = pgui.Label("Bot Fight", font=fontBig)
        layout.add(title, 20, 20)

        # Check button
        check_button_table = pgui.Table()
        check_button = pgui.Switch()
        check_button.connect(pgui.CHANGE, logCheckAction, (check_button, "Check box"))
        check_button_label = pgui.Label("Check box")
        check_button_table.add(check_button)
        check_button_table.add(check_button_label)
        check_button_table.tr()

        #layout.add(check_button_table, 50, 50)

        # Radio buttons
        radio_button_table = pgui.Table()
        radio_group = pgui.Group()
        radio_button1 = pgui.Radio(radio_group, 1)
        radio_button1_label = pgui.Label("Radio button 1")
        radio_button_table.add(radio_button1)
        radio_button_table.add(radio_button1_label)
        radio_button_table.tr()

        radio_button2 = pgui.Radio(radio_group, 2)
        radio_button2_label = pgui.Label("Radio button 2")
        radio_button_table.add(radio_button2)
        radio_button_table.add(radio_button2_label)
        radio_button_table.tr()

        #layout.add(radio_button_table, 70, 50)
        radio_group.connect(pgui.CHANGE, logRadioAction, (radio_group, "Radio buttons"))

        # Other gui elements
        # Normal Buttons
        new_game_button = pgui.Button("New game")
        new_game_button.connect(pgui.CLICK, self.new_game, ())
        layout.add(new_game_button, 20, 40)

        if self.screen_state == Main.PLAYING:
            main_menu_button = pgui.Button("Main menu")
            main_menu_button.connect(pgui.CLICK, self.main_menu, ())
            layout.add(main_menu_button, 20, 70)

        self.gui.init(layout)

    def new_game(self, *args):
        self.screen_state = Main.PLAYING

        if not self.campaign:
            p1 = player.HumanPlayer(None)
            p2 = player.Player(None)
            p3 = player.Player(None)
            p4 = player.Player(None)
            w = world.World(Vector(*self.screen_size))
            self.campaign = campaign.Campaign(p1, [level.Level(w, 10)])

            self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
            self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
            #self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
            #self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.ULTRA_TANK)

            self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.LIGHT)
            #self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.LIGHT)
            #self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.ULTRA_LIGHT)
            self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.TANK)
            w.addPlayer(p1)
            w.addPlayer(p2)


        else:
            self.campaign.player.bots = []
            p1 = self.campaign.player
            p2 = player.Player(None)
            p3 = player.Player(None)
            p4 = player.Player(None)
            w = world.World(Vector(*self.screen_size))
            self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
            self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
            #self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.NORMAL)
            #self.add_bot(p1, self.screen_size, (255, 0, 0), build=Build.ULTRA_TANK)

            self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.LIGHT)
            #self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.LIGHT)
            #self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.ULTRA_LIGHT)
            self.add_bot(p2, self.screen_size, (0, 255, 0), build=Build.TANK)
            w.addPlayer(p1)
            w.addPlayer(p2)
            self.campaign.levels = [level.Level(w, 10)]

        self.campaign.play_level(self.campaign.levels[0])
        self.init_gui()

    def main_menu(self, *args):
        self.screen_state = Main.MAIN
        self.campaign = None
        self.init_gui()

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
