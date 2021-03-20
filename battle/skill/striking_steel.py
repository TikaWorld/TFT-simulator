import copy
from typing import List
import random

from .skill import Skill
from ..construct import Damage, Champion
from ..construct.enum import DamageType, Stat, EventType
from ..construct.field import Cell


class StrikingSteel(Skill):
    SKILL_FACTOR = [190, 190, 200, 210]

    def __init__(self, field):
        super().__init__()
        self.field = field

    @staticmethod
    def attack_target(damage: Damage, target_cells: List[Cell]):
        total_damage = 0
        total_target = []
        for t in target_cells:
            dmg = copy.copy(damage)
            target = t.champion
            if not target:
                continue
            dmg.set_miss(target.is_dodge())
            total_damage += target.get_damage(dmg)
            total_target.append(target)

        return total_damage, total_target

    def cast(self, champion: Champion):
        caster_cell = self.field.champion_location[champion]
        target_cell = self.field.champion_location[champion.target]
        casting = self.get_casting_pos(caster_cell, target_cell)

        casting_cell = casting[0]
        target_cells = casting[1:]
        if casting_cell is not caster_cell:
            yield self.field.env.timeout(0.1)
            self.field.transfer(champion, casting_cell)

        damage = self.get_damage(champion)
        total_damage, total_target = self.attack_target(damage, target_cells)

        champion.cause_event(EventType.BASIC_ATTACK, damage=total_damage, champion=champion, targets=total_target)
        print(f'{champion}: Casting Striking Steel at {self.field.env.now:f}')

        yield self.field.env.timeout(0.3)

    def get_damage(self, champion: Champion):
        skill_factor = (self.SKILL_FACTOR[champion.level] * 0.01) * (champion.get_stat(Stat.SPELL) * 0.01)

        dmg = Damage(champion, champion.get_stat(Stat.ATTACK) * skill_factor, DamageType.PHYSICAL)
        dmg.set_critical(champion.get_stat(Stat.CRITICAL_DAMAGE)) if champion.is_critical() else None
        dmg.set_damage_increase(champion.get_stat(Stat.DAMAGE_INCREASE))
        return dmg

    def get_hit_box(self, casting_cell: Cell, target_cell: Cell) -> List[Cell]:
        casting_pos = casting_cell.pos
        result = [casting_cell, target_cell]

        target_pos = target_cell.pos
        extra_pos = [None, None]

        if casting_pos[0] == target_pos[0]:
            extra_pos[0] = target_pos[0]
            extra_pos[1] = target_pos[1] + 1 if casting_pos[1] < target_pos[1] else target_pos[0] - 1
        else:
            is_odd = target_pos[0] % 2
            extra_pos[0] = target_pos[0] + 1 if casting_pos[0] < target_pos[0] else target_pos[0] - 1
            extra_pos[1] = casting_pos[1] - 1 if target_pos[1] + is_odd == casting_pos[1] else casting_pos[1] + 1

        extra_cell = self.field.get_cell(extra_pos)
        result.append(extra_cell) if extra_cell else None

        return result

    def get_casting_pos(self, caster_cell, target_cell) -> List[Cell]:
        champion_count = lambda l: sum(
            map(lambda x: True if x.champion and x.champion.team != caster_cell.champion.team else False, l[1:]))
        result = None
        target_count = 0
        candidate_cells: List[Cell] = target_cell.connect
        if caster_cell in candidate_cells:
            result = self.get_hit_box(caster_cell, target_cell)
            target_count = champion_count(result)
        candidate = []
        for c in candidate_cells:
            if c.champion:
                continue
            hit_box = self.get_hit_box(c, target_cell)
            if champion_count(hit_box) > target_count:
                candidate.append(hit_box)
        result = random.choice(candidate) if candidate else result

        return result
