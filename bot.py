import pygame

from vector import *

class Chasis:
    def __init__(self, capacity):
        self.capacity = capacity

class Body:
    def __init__(self, weight):
        self.weight = weight
        self.camera = None
        self.weapon = Weapon()
        self.motor = Motor()

    def update(self, dt):
        self.weapon.update(dt)

class Weapon:
    def __init__(self, power=100, reload_time=1):
        self.power = power
        self._reload_time = reload_time
        self._time_till_reload = None

    def update(self, dt):
        if self._time_till_reload != None:
            self._time_till_reload -= dt
            if self._time_till_reload < 0.0:
                self._time_till_reload = None
        
    def shoot(self, pos, direction):
        if self._time_till_reload == None:
            self._time_till_reload = self._reload_time
            return Bullet(pos, direction.normalize() * self.power)

class Motor:
    def __init__(self, torque=1):
        self.torque = torque

class Bullet:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = (velocity if type(velocity) == Vector else Vector(*velocity))

    def update(self, dt):
        self.pos += self.velocity * dt

    def display(self, screen, pos):
        pygame.draw.circle(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), 3, 0)
        
class Bot:
    def __init__(self, pos, chasis=Chasis(0), body=Body(0)):
        self.pos = pos
        self.chasis = chasis
        self.body = body
        self.velocity = Vector(0.0, 0.0)

    def update(self, dt):
        self.body.update(dt)
        self.pos += self.velocity * dt
        return self.shoot(self.velocity)

    def display(self, screen, pos):
        pygame.draw.circle(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), 10, 0)

    def set_velocity(self, velocity):
        if type(velocity) == Vector:
            self.velocity = velocity
        else:
            self.velocity = Vector(*velocity)

    def accelerate(self, acceleration):
        if type(acceleration) == Vector:
            self.velocity += acceleration
        else:
            self.velocity += Vector(*acceleration)

    def shoot(self, direction):
        return self.body.weapon.shoot(self.pos, direction)

