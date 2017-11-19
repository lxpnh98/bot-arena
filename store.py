class Store:
    def __init__(self):
        self.stock = []

    def add_component(self, component):
        self.stock.append(component)

    def buy(self, player, component):
        if player.cash >= component.buy_price:
            player.cash -= component.buy_price
            player.inventory.append(component)
        print(player.cash)
        print(player.inventory)

    def sell(self, player, component):
        pass
