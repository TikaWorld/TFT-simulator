import math
import numpy

from battle.hex import hex_to_pixel, pixel_to_hex


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
        caster_pos = hex_to_pixel(c_pos[0], c_pos[1])
        target_pos = hex_to_pixel(t_pos[0], t_pos[1])

        self.heist = heist
        self.slope = [target_pos[0] - caster_pos[0], target_pos[1] - caster_pos[1]]
        self.accel = self.get_accel(self.slope)
        self.start_pos = caster_pos
        self.displacement = [0, 0]
        self.alive = True

    @staticmethod
    def get_accel(slope):
        distance = math.sqrt(pow(slope[0], 2) + pow(slope[1], 2))
        p = distance
        return slope[0] / p, slope[1] / p

    def get_pos(self):
        converted_pos = pixel_to_hex(self.displacement[0]+self.start_pos[0], self.displacement[1]+self.start_pos[1])
        return converted_pos

    def tick(self, second):
        r = []
        for _ in numpy.arange(0, (self.heist / 180) * second, second):
            self.displacement[0] += self.accel[0] * second
            self.displacement[1] += self.accel[1] * second
            collided_pos = self.get_pos()
            if collided_pos not in r:
                r.append(collided_pos)
        print(r)
        return r

    def collide(self, champion, target):
        return NotImplemented

    def kill(self):
        self.alive = False
