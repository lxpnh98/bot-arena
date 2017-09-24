import math
from bullet import *

class Chasis:
    def __init__(self, bot, capacity, hp):
        self.bot = bot
        self.capacity = capacity
        self.hp = hp

class Body:
    def __init__(self, bot, weight):
        self.bot = bot
        self.weight = weight
        self.camera = None
        self.weapon = Weapon(bot)
        self.motor = Motor(bot)

    def update(self, dt):
        self.weapon.update(dt)

    def getWeight(self):
        return self.weight

class Weapon:
    def __init__(self, bot, angle = 0, turn_speed = math.pi, power=100, reload_time=1):
        self.bot = bot
        self.angle = angle
        self.turn_speed = turn_speed
        self.power = power
        self._target_angle = angle
        self._reload_time = reload_time
        self._time_till_reload = None

    def update(self, dt):
        angle_diff = self._target_angle - self.angle
        angle_direction = (1 if angle_diff > 0 else -1)
        self.angle += angle_direction * min(self.turn_speed, abs(angle_diff)) * dt
        if self._time_till_reload != None:
            self._time_till_reload -= dt
            if self._time_till_reload < 0.0:
                self._time_till_reload = None
    
    def turn(self, angle):
        self._target_angle = angle

    def shoot(self):
        if self._time_till_reload == None:
            self._time_till_reload = self._reload_time
            direction = self.getDirection()
            return Bullet(self.bot, self.bot.pos, direction * self.power)

    def getDirection(self):
        return Vector(math.cos(self.angle - math.pi / 2), math.sin(self.angle + math.pi / 2))
        

class Motor:
    def __init__(self, bot, torque=1):
        self.bot = bot
        self.torque = torque

