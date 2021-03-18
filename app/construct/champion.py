from typing import List, Union, TYPE_CHECKING

from app.construct.enum import EventType, Stat, State, DamageType
import random

if TYPE_CHECKING:
    from app.construct import Team
    from app.construct.barrier import Barrier


class Champion:
    def __init__(self, champ_data, team: "Team"):
        self.name = champ_data["name"]
        self.id = champ_data["id"]
        self.team: Team = team
        self.trait = champ_data["trait"]
        self.skill = champ_data["skill"]

        self.state: List[State] = []
        self.buff = {s: [] for s in Stat}
        self.event = {e: [] for e in EventType}
        self.stat = {s: champ_data[s] for s in Stat}
        self.hp = self.stat[Stat.MAX_HP]
        self.mp = self.stat[Stat.MP]
        self.barrier: List['Barrier'] = []

        self.action = None
        self.target: Union[Champion, None] = None

    def heal(self, value):
        self.hp = min(self.get_stat(Stat.MAX_HP), self.hp+value)

    def get_stat(self, stat_type) -> Union[int, float]:
        origin = self.stat[stat_type]
        buff = 0
        for b in self.buff[stat_type]:
            if b.is_absolute:
                origin += b.result(stat_type)
                continue
            buff += b.result(stat_type)

        return origin + (origin * buff)

    def use_barrier(self, dmg: Union[int, float]) -> Union[int, float]:
        residual = dmg
        for b in self.barrier:
            residual = b.calc(residual)
            if residual:
                break
        return residual

    def cause_event(self, event_type, **kwargs):
        for e in self.event[event_type]:
            e.get(event_type, **kwargs)

    def generate_mana(self, mana):
        self.mp = min(self.mp + mana, self.get_stat(Stat.MAX_MP))

    def get_damage(self, damage) -> Union[int, float, None]:
        damage.set_armor(self.get_stat(Stat.ARMOR))
        damage.set_magic_resistance(self.get_stat(Stat.MAGIC_RESISTANCE))
        self.stat[Stat.DAMAGE_REDUCE] = damage.calc()
        reduced_damage = self.stat[Stat.DAMAGE_REDUCE] \
            if damage.type == DamageType.TRUE else self.get_stat(Stat.DAMAGE_REDUCE)
        self.generate_mana(damage.get_pre_mitigated() * 0.06)

        if reduced_damage is None:
            print(f'{self.name}: Avoid damage')
            return None
        residual_damage = self.use_barrier(reduced_damage)
        self.hp = max(self.hp - residual_damage, 0)
        self.cause_event(EventType.GET_DAMAGE, damage=reduced_damage, hp=self.hp, max_hp=self.get_stat(Stat.MAX_HP))

        if not self.hp:
            self.set_death()
        print(f'{self.name}: Get Damage {reduced_damage} HP left {self.hp}')

        return reduced_damage

    def is_critical(self) -> bool:
        chance = min(100, self.get_stat(Stat.CRITICAL_CHANCE))
        result = random.choices([True, False], weights=[chance, 100 - chance])

        return result[0]

    def is_dodge(self) -> bool:
        chance = min(100, self.get_stat(Stat.DODGE_CHANCE))
        result = random.choices([True, False], weights=[chance, 100 - chance])

        return result[0]

    def is_dead(self) -> bool:
        if State.DEATH in self.state:
            return True
        return False

    def is_mp_full(self) -> bool:
        if self.mp >= self.get_stat(Stat.MAX_MP):
            return True
        return False

    def set_death(self):
        try:
            if self.action is not None:
                self.action.interrupt()
                self.action = None
        except RuntimeError:
            print('Action Already terminated')
        self.state = [State.DEATH]

    def __repr__(self):
        return f'{self.name}'
