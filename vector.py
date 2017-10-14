import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def dot(self, other):
        return Vector(self.x * other.x, self.y * other.y)

    def length(self):
        return math.sqrt(self.dist2())

    def dist2(self):
        return self.x ** 2 + self.y ** 2
        
    def normalize(self):
        l = self.length()
        if l != 0.0:
            return Vector(self.x, self.y) * (1 / self.length())
        return Vector(0.0, 0.0)

    def angle(self):
        return math.atan2(self.x, self.y)

    def toInt(self):
        return Vector(int(self.x), int(self.y))

    def toTuple(self):
        return (self.x, self.y)

    def widthVector(self):
        return Vector(self.x, 0)

    def heightVector(self):
        return Vector(0, self.y)
