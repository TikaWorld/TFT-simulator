import math
import numpy


class Skill:
    def __init__(self):
        self.type = None

    def action(self):
        return NotImplemented

    def hit(self, champion):
        champion.get_damage(0)


class Projectile:
    def __init__(self, pos, slope):
        self.heist = 1300
        self.accel = self.get_accel(slope)
        self.pos = pos

    @staticmethod
    def get_accel(slope):
        distance = math.sqrt(pow(slope[0], 2) + pow(slope[1], 2))
        p = distance * 10
        return slope[0] / p, slope[1] / p

    def __next__(self):
        r = []
        for _ in numpy.arange(0, (self.heist/180)/10, 0.1):
            self.pos[0] += self.accel[0]
            self.pos[1] += self.accel[1]
            if [int(self.pos[0]), int(self.pos[1])] not in r:
                r.append([int(self.pos[0]), int(self.pos[1])])
        return r

    def __iter__(self):
        return self
