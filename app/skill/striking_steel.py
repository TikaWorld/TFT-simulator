from typing import List
import random

from .skill import Skill
from ..construct import Damage, Champion
from ..construct.enum import DamageType, Stat, EventType
from ..construct.field import Cell


class StrikingSteel(Skill):
    def __init__(self, field):
        super().__init__()
        self.field = field

    def get_hit_box(self, casting_cell: Cell, target: Champion):
        target_cell = self.field.champion_location[target]
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

    def cast(self, champion: Champion):
        champion_count = lambda l: sum(
            map(lambda x: True if x.champion and x.champion.team != champion.team else False, l[1:]))
        result = None
        target_count = 0
        caster_cell = self.field.champion_location[champion]
        candidate_cells: List[Cell] = self.field.champion_location[champion.target].connect
        if caster_cell in candidate_cells:
            result = self.get_hit_box(caster_cell, champion.target)
            target_count = champion_count(result)
        candidate = []
        for c in candidate_cells:
            if c.champion:
                continue
            hit_box = self.get_hit_box(c, champion.target)
            if champion_count(hit_box) > target_count:
                candidate.append(hit_box)
        result = random.choice(candidate) if candidate else result
        yield self.field.env.timeout(0.1)

        casting_cell = result[0]
        target_cells = result[1:]
        total_damage = 0
        total_target = []
        if casting_cell is not caster_cell:
            self.field.transfer(champion, casting_cell)
        for t in target_cells:
            target = t.champion
            if not target:
                continue
            dmg = Damage(champion, 100, DamageType.PHYSICAL)
            dmg.set_critical(champion.get_stat(Stat.CRITICAL_DAMAGE)) if champion.is_critical() else None
            dmg.set_miss(target.is_dodge())
            total_damage += target.get_damage(dmg)
            total_target.append(target)

        champion.cause_event(EventType.BASIC_ATTACK, damage=total_damage, champion=champion, targets=total_target)
        print(f'{champion}: Casting Striking Steel at {self.field.env.now:f}')
