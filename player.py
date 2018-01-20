import bot
import components

class MultipleChasisException(Exception): pass

class MultipleBodiesException(Exception): pass

class WrongPartsException(Exception): pass

class NoChasisException(Exception): pass

class NoBodyException(Exception): pass

class NotInInventoryException(Exception): pass

class Player:
    def __init__(self, name):
        self.name = name
        self.bots = []

    def addBot(self, bot):
        bot.player = self
        self.bots.append(bot)

class HumanPlayer(Player):
    def __init__(self, name, init_cash=0):
        self.cash = init_cash
        self._inventory = []
        self._assembly = []
        super().__init__(name)

    def getAssembly(self):
        return self._assembly

    def getInventory(self):
        return self._inventory

    def addToInventory(self, c):
        if c not in self._inventory:
            self._inventory.append(c)

    def assembleBot(self, parts, pos, color):
        chasis = None
        body = None
        weapons = []
        for c in parts:
            if c not in self._inventory:
                raise NotInInventoryException(c)
            if isinstance(c, components.Chasis):
                if chasis == None:
                    chasis = c
                else:
                    raise MultipleChasisException()
            elif isinstance(c, components.Body):
                if body == None:
                    body = c
                else:
                    raise MultipleBodiesException()
            elif isinstance(c, components.Weapon):
                weapons.append(c)
            else:
                raise WrongPartsException()
        if chasis == None:
            raise NoChasisException()
        if body == None:
            raise NoBodyException()
        self._inventory.remove(chasis)
        self._inventory.remove(body)
        b = bot.Bot(pos, chasis, color)
        b.chasis.addBody(body)
        for w in weapons:
            self._inventory.remove(w)
            b.chasis.body.addWeapon(w)
        self._assembly.append(b)

    def disassembleBot(self, bot):
        pass

