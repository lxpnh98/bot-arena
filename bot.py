import pygame

from vector import *
from components import *
from bullet import *

class Bot:
    def __init__(self, pos, chasis=None, body=None, size=20):
        self.pos = pos
        self.chasis = (chasis if chasis != None else Chasis(self, 0, 5))
        self.body = (body if body != None else Body(self, 2))
        self.size = size
        self.velocity = Vector(0.0, 0.0)

    def update(self, dt, bot_list, world_size, world_distances):
        self.body.update(dt)

        # Decision making

        sum_world_dist = sum(world_distances)
        if (sum_world_dist > 0):
            desired_pos = ((world_size * (world_distances[1] - (self.pos - world_size).dist2()) + 
                           (world_size * (1/2.) * (world_distances[2] - (self.pos - (world_size * (1/2.))).dist2())) + 
                           (world_size.widthVector() * (world_distances[3] - (self.pos - world_size.widthVector()).dist2())) + 
                           (world_size.heightVector() * (world_distances[4] - (self.pos - world_size.heightVector()).dist2())) + 
                           ((world_size.widthVector() * (1/2.)) * (world_distances[5] - (self.pos - (world_size.widthVector() * (1/2.))).dist2())) + 
                           ((world_size.heightVector()* (1/2.)) * (world_distances[6] - (self.pos - (world_size.heightVector() * (1/2.))).dist2())) + 
                           ((world_size.widthVector() * (1/2.) + world_size.heightVector()) * (world_distances[7] - (self.pos - (world_size.widthVector() * (1/2.) + world_size.heightVector())).dist2())) + 
                           ((world_size.heightVector() * (1/2.) + world_size.widthVector()) * (world_distances[8] - (self.pos - (world_size.heightVector() * (1/2.) + world_size.widthVector())).dist2()))) * (1. / sum_world_dist))
            #print(1. / sum_world_dist, desired_pos)
            self.setVelocity(desired_pos - self.pos)
                                            
        min_length_bot = None
        min_length = None
        for b in bot_list:
            if b is not self:
                b_dist = (b.pos - self.pos).length()
                if min_length_bot == None or min_length > b_dist:
                    min_length_bot = b
                    min_length = b_dist
        
        self.pos += self.velocity * dt
        if min_length_bot != None:
            shoot_direction = min_length_bot.pos - self.pos
            self.body.weapon.turn(shoot_direction.angle())
            return self.shoot()
        else:
            return None

    def display(self, screen, pos):
        pygame.draw.circle(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), self.size, 0)
        weapon_pos = (self.pos + pos) + self.body.weapon.getDirection() * (self.size + 4)
        pygame.draw.line(screen, pygame.color.Color("black"), (self.pos + pos).toInt().toTuple(), weapon_pos.toInt().toTuple(), 3)

    def setVelocity(self, velocity):
        if type(velocity) == Vector:
            self.velocity = velocity
        else:
            self.velocity = Vector(*velocity)
        if self.velocity.length() > self.getMaxSpeed():
            self.velocity *= self.getMaxSpeed() / self.velocity.length()

    def getPos(self):
        return self.pos

    def getHP(self):
        return self.chasis.hp

    def getMaxSpeed(self):
        return 100. / self.body.getWeight()

    def accelerate(self, acceleration):
        if type(acceleration) == Vector:
            self.velocity += acceleration
        else:
            self.velocity += Vector(*acceleration)

    def shoot(self):
        return self.body.weapon.shoot()

    def collidesWith(self, bot):
        if (bot.pos - self.pos).dist2() <= (bot.size + self.size)**2:
            return True
        else:
            return False
