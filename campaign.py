class Campaign:
    def __init__(self, player, levels):
        self.player = player
        self.levels = levels
        self.completed_levels = []
        self.current_level = None

    def update(self, dt):
        if self.current_level:
            winner = self.current_level.update(dt)
            if winner != None:
                if  winner == self.player: # Winner
                    self.player.cash += self.current_level.cash_reward
                    self.completed_levels.append(self.current_level)
                    self.current_level = None
                    print(self.player.cash)
                else:
                    self.current_level = None

    def display(self, screen, pos):
        if self.current_level:
            self.current_level.display(screen, pos)

    def play_level(self, level):
        if level in self.levels:
            self.current_level = level
