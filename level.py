class Level:
    def __init__(self, world, cash_reward):
        self.world = world
        self.cash_reward = cash_reward

    def update(self, dt):
        return self.world.update(dt)

    def display(self, screen, pos):
        self.world.display(screen, pos)
