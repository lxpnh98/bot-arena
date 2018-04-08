class Store:
    def __init__(self):
        self.stock = []

    def add_component(self, component):
        self.stock.append(component)

    def buy(self, player, component):
        if player.cash >= component.buy_price:
            player.cash -= component.buy_price
            player.addToInventory(component)
        print(player)
        print(player.cash)
        print(player.getInventory())

    def sell(self, player, component):
        pass
