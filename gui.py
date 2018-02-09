import sys
import random
import pygame

from pgu import text, gui as pgui

from vector import Vector
import campaign
import world
import player
import store
import components
import bot
import level

pygame.init()

class Build:
    ULTRA_LIGHT=0
    LIGHT=1
    NORMAL=2
    TANK=3
    ULTRA_TANK=4

def logRadioAction(arg):
    print("Hello, ")

def logCheckAction(arg):
    print("world!")

font = pygame.font.SysFont("default", 18)
fontBig = pygame.font.SysFont("default", 24)
fontSub = pygame.font.SysFont("default", 20)

class State(pgui.App):
    def __init__(self, gui, screen):
        super().__init__()
        self.gui = gui
        self.screen = screen

    def update(self, dt):
        pass

    def display(self):
        self.screen.fill(pygame.color.Color("white"))
        self.paint(self.screen)

class PlayingState(State):
    def __init__(self, gui, screen, screen_size, campaign):
        super().__init__(gui, screen)
        self.campaign = campaign

        self.campaign.player.bots = []
        p1 = self.campaign.player
        p2 = player.Player(None)
        p3 = player.Player(None)
        p4 = player.Player(None)
        w = world.World(Vector(*screen_size))

        for b in p1.getAssembly():
            p1.addBot(b)
        #self.add_bot(p1, screen_size, (255, 0, 0), build=Build.NORMAL)
        #self.add_bot(p1, screen_size, (255, 0, 0), build=Build.NORMAL)
        #self.add_bot(p1, screen_size, (255, 0, 0), build=Build.NORMAL)
        #self.add_bot(p1, screen_size, (255, 0, 0), build=Build.ULTRA_TANK)
        #self.add_bot(p1, screen_size, (255, 0, 0))

        self.add_bot(p2, screen_size, (0, 255, 0), build=Build.LIGHT)
        #self.add_bot(p2, screen_size, (0, 255, 0), build=Build.LIGHT)
        #self.add_bot(p2, screen_size, (0, 255, 0), build=Build.ULTRA_LIGHT)
        self.add_bot(p2, screen_size, (0, 255, 0), build=Build.TANK)
        self.add_bot(p2, screen_size, (0, 255, 0))
        w.addPlayer(p1)
        w.addPlayer(p2)
        self.campaign.levels = [level.Level(w, 10)]

        self.campaign.play_level(self.campaign.levels[0])

        layout = pgui.Container(width=screen_size[0], height=screen_size[1])
        main_menu_button = pgui.Button("Main menu")
        main_menu_button.connect(pgui.CLICK, self.gui.main_menu, None)
        layout.add(main_menu_button, 20, 70)
        play_button = pgui.Button("Plan")
        play_button.connect(pgui.CLICK, self.gui.plan_screen, self.campaign)
        layout.add(play_button, 20, 100)
        self.init(layout)

    def update(self, dt):
        self.campaign.update(dt)
        if self.campaign.current_level == None:
            self.gui.plan_screen(self.campaign)

    def add_bot(self, player, screen_size, bot_color, build=-1):
        if build == -1:
            build = random.randint(Build.ULTRA_LIGHT, Build.ULTRA_TANK)
        if build == Build.ULTRA_LIGHT:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=7, weight=4, hp=4))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=2, bullet_speed=300, bullet_damage=0.05, reload_time=0.1))
        elif build == Build.LIGHT:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=10, weight=7, hp=7))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=3, bullet_speed=140, bullet_damage=0.2, reload_time=0.3))
        elif build == Build.NORMAL:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=17, weight=10, hp=10))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=4, bullet_speed=110, bullet_damage=1, reload_time=1))
        elif build == Build.TANK:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=30, weight=15, hp=17.5))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=6, bullet_speed=70, bullet_damage=3.25, reload_time=2.5))
        elif build == Build.ULTRA_TANK:
            b = bot.Bot(Vector(random.random(), random.random()).dot(Vector(*screen_size)),
                        components.Chasis(None, 5, None),
                        color=bot_color)
            b.chasis.addBody(components.Body(None, size=50, weight=40, hp=50))
            b.chasis.body.addWeapon(components.Weapon(None, bullet_size=15, bullet_speed=40, bullet_damage=15, reload_time=6))
        player.addBot(b)

    def display(self):
        self.screen.fill(pygame.color.Color("white"))
        self.campaign.display(self.screen, Vector(0, 0))
        self.paint(self.screen)

class MainState(State):
    def __init__(self, gui, screen, screen_size):
        super().__init__(gui, screen)

        layout = pgui.Container(width=screen_size[0], height=screen_size[1])
        play_button = pgui.Button("Plan")
        play_button.connect(pgui.CLICK, self.gui.plan_screen, None)
        layout.add(play_button, 20, 100)
        self.init(layout)

class PlanningState(State):
    def __init__(self, gui, screen, screen_size, current_campaign):
        super().__init__(gui, screen)
        self.campaign = current_campaign
        if self.campaign == None:
            w = world.World(Vector(*screen_size))
            self.campaign = campaign.Campaign(player.HumanPlayer(None), [level.Level(w, 10)], store.Store())
            c = components.Chasis(None, 5, None)
            b = components.Body(None, size=7, weight=4, hp=4)
            w = components.Weapon(None, bullet_size=2, bullet_speed=300, bullet_damage=0.05, reload_time=0.1)
            self.campaign.player.addToInventory(c)
            self.campaign.player.addToInventory(b)
            self.campaign.player.addToInventory(w)
            self.campaign.player.assembleBot([c, b, w], Vector(100,100), (0, 0, 0))
            #self.campaign.player.disassembleBot(self.campaign.player.getAssembly()[0])
            #self.campaign.player.assembleBot([c, b, w], Vector(100,100), (0, 0, 0))

        layout = pgui.Container(width=screen_size[0], height=screen_size[1])
        store_button = pgui.Button("Store")
        store_button.connect(pgui.CLICK, self.gui.store, self.campaign)
        layout.add(store_button, 20, 40)
        main_menu_button = pgui.Button("Main menu")
        main_menu_button.connect(pgui.CLICK, self.gui.main_menu, None)
        layout.add(main_menu_button, 20, 70)
        new_game_button = pgui.Button("New game")
        new_game_button.connect(pgui.CLICK, self.gui.new_game, self.campaign)
        layout.add(new_game_button, 20, 100)
        self.init(layout)

class StoreState(State):
    def __init__(self, gui, screen, screen_size, campaign):
        super().__init__(gui, screen)
        self.campaign = campaign

        layout = pgui.Container(width=screen_size[0], height=screen_size[1])
        buy_chasis_button = pgui.Button("Buy Chasis")
        buy_chasis_button.connect(pgui.CLICK, self.campaign.store.buy, self.campaign.player, components.Chasis(None, 5, None))
        layout.add(buy_chasis_button, 20, 100)
        buy_body_button = pgui.Button("Buy Body")
        buy_body_button.connect(pgui.CLICK, self.campaign.store.buy, self.campaign.player, components.Body(None, 17, 10, 10))
        layout.add(buy_body_button, 150, 100)

        back_button = pgui.Button("Go back")
        back_button.connect(pgui.CLICK, self.gui.plan_screen, self.campaign)
        layout.add(back_button, 20, 40)
        self.init(layout)

class GUI:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen_state = MainState(self, self.screen, self.screen_size)

    def update(self, dt):
        self.screen_state.update(dt)

    def display(self):
        self.screen_state.display()

    def event(self, e):
        self.screen_state.event(e)

    def plan_screen(self, campaign):
        self.screen_state = PlanningState(self, self.screen, self.screen_size, campaign)

    def store(self, campaign):
        self.screen_state = StoreState(self, self.screen, self.screen_size, campaign)

    def main_menu(self, *args):
        self.screen_state = MainState(self, self.screen, self.screen_size)

    def new_game(self, campaign):
        self.screen_state = PlayingState(self, self.screen, self.screen_size, campaign)

