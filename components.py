import math
from bullet import *

class Chasis:
    def __init__(self, bot, capacity, body=None):
        self.bot = bot
        self.capacity = capacity
        self.body = None

    def update(self, dt):
        if self.body:
            self.body.update(dt)

    def addBody(self, body):
        body.bot = self.bot
        self.body = body

class Body:
    def __init__(self, bot, size, weight, hp):
        self.bot = bot
        self.size = size
        self.weight = weight
        self.cameras = []
        self.weapons = []
        self.motors = []
        self.hp = hp

    def update(self, dt):
        for w in self.weapons:
            w.update(dt)
        for m in self.motors:
            m.update(dt)
        for c in self.cameras:
            c.update(dt)

    def getWeight(self):
        return self.weight

    def addCamera(self, camera):
        camera.bot = self.bot
        self.cameras.append(camera)
        return self

    def addWeapon(self, weapon):
        weapon.bot = self.bot
        self.weapons.append(weapon)
        return self

    def addMotor(self, motor):
        motor.bot = self.bot
        self.motors.append(motor)
        return self

class Weapon:
    def __init__(self, bot, angle = 0, turn_speed = math.pi, bullet_size = 3, bullet_speed = 100, bullet_damage=1, reload_time=1):
        self.bot = bot
        self.angle = angle
        self.turn_speed = turn_speed
        self.bullet_size = bullet_size
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        self._target_angle = angle
        self._reload_time = reload_time
        self._time_till_reload = None

    def update(self, dt):
        #velocity_diff = self.bot.getAngleDiff()
        #self.angle -= velocity_diff

        if abs(self._target_angle - self.angle) < abs(self._target_angle - (self.angle + 2*math.pi)):
            angle_diff = self._target_angle - self.angle
        else:
            angle_diff = self._target_angle - (self.angle + 2*math.pi)
        angle_direction = (1 if angle_diff > 0 else -1)
        if (angle_direction * self.turn_speed * dt) > abs(angle_diff):
            self.angle += angle_direction * abs(angle_diff) * dt
        else:
            self.angle += angle_direction * self.turn_speed * dt

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
            return Bullet(self.bot, self.bot.pos, direction * self.bullet_speed, self.bullet_damage, self.bullet_size)

    def getDirection(self):
        return Vector(math.cos((self.angle + self.bot.getAngle()) - math.pi / 2), math.sin((self.angle + self.bot.getAngle()) + math.pi / 2))
        #return Vector(math.cos(self.angle - math.pi / 2), math.sin(self.angle + math.pi / 2))
        

class Motor:
    def __init__(self, bot, torque=1):
        self.bot = bot
        self.torque = torque

    def update(self, dt):
        pass

class Camera:
    def __init__(self, bot):
        pass

    def update(self, dt):
        pass
