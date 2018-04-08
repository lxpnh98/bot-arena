import sys
import random
import pygame

#from pgu import text, gui as pgui

from vector import Vector

import gui
import campaign
import level
import world
import bot
import components
import player

pygame.init()

class Main:
    def __init__(self, screen_size=(640,480)):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0.0
        self.gui = gui.GUI(screen_size)

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.gui.update(self.dt)
            self.gui.display()
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

    def tick(self):
        pygame.display.update()
        self.dt = self.clock.tick(self.fps) / 1000.
        pygame.display.set_caption("FPS: %i" % (1 / self.dt))

    def exit(self, return_value):
        pygame.quit()
        sys.exit(return_value)

if __name__ == "__main__":
    Main().run()
