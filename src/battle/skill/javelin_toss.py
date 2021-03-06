from .skill import Skill, Projectile
from ..action.search import find_farthest

import random

from ..construct import Damage, Champion
from ..construct.enum import DamageType


class JavelinToss(Skill):
    def __init__(self, field):
        super().__init__()
        self.field = field

    def get_farthest_champion_pos(self, caster):
        caster_cell = self.field.champion_location[caster]
        _, target_cell_list = find_farthest(caster_cell)
        return random.choice(target_cell_list).pos

    def cast(self, champion):
        second = 0.01
        caster_pos = self.field.champion_location[champion].pos
        target_pos = self.get_farthest_champion_pos(champion)
        javelin = Javelin(100, caster_pos, target_pos)
        javelin.set_ignore(champion)
        while javelin.alive:
            yield self.field.env.timeout(second)
            for pos in javelin.tick(second):
                collide_pos = self.field.get_cell(pos)
                if not collide_pos:
                    javelin.kill()
                    break
                collide_target: Champion = collide_pos.champion
                if collide_target and collide_target not in javelin.ignore:
                    javelin.collide(champion, collide_target)
                    print(f'{champion}: Collide {collide_target} with javelin toss at {self.field.env.now:f}')
                    break


class Javelin(Projectile):
    def __init__(self, damage_value, pos, slope):
        super().__init__(pos, slope, heist=1300)
        self.ignore = []
        self.damage_value = damage_value

    def set_ignore(self, champion: Champion):
        self.ignore.append(champion)

    def collide(self, caster: Champion, target: Champion):
        self.set_ignore(target)
        d = Damage(caster, self.damage_value, DamageType.MAGIC)
        target.get_damage(d)
        self.alive = False
