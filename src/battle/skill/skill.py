import math
import numpy

from battle.construct.field import pos_convert, pivot_convert


class Skill:

    def cast(self, champion):
        return NotImplemented

    @staticmethod
    def chk_condition(champion):
        target = champion.target
        if target and not target.is_dead() and champion.is_mp_full():
            return True
        return False


class Projectile:
    def __init__(self, c_pos, t_pos, heist):
        caster_pos = pivot_convert(c_pos)
        target_pos = pivot_convert(t_pos)

        self.heist = heist
        self.slope = [target_pos[0] - caster_pos[0], target_pos[1] - caster_pos[1]]
        self.accel = self.get_accel(self.slope)
        self.start_pos = c_pos
        self.displacement = [0, 0]
        self.alive = True

    @staticmethod
    def get_accel(slope):
        distance = math.sqrt(pow(slope[0], 2) + pow(slope[1], 2))
        p = distance
        return slope[0] / p, slope[1] / p

    def get_pos(self):
        converted_pos = pos_convert([self.displacement[0]+self.start_pos[0], self.displacement[1]+self.start_pos[1]],
                                    self.start_pos)
        return [int(converted_pos[0]), int(converted_pos[1])]

    def tick(self, second):
        r = []
        for _ in numpy.arange(0, (self.heist / 180) * second, second):
            self.displacement[0] += self.accel[0] * second
            self.displacement[1] += self.accel[1] * second
            collided_pos = self.get_pos()
            if collided_pos not in r:
                r.append(collided_pos)
        return r

    def collide(self, champion, target):
        return NotImplemented

    def kill(self):
        self.alive = False
