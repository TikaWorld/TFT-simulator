from typing import List, Union

from app.construct.enum import EventType, Stat, State
import random


class Champion:
    def __init__(self, champ_data, team: int):
        self.name = champ_data["name"]
        self.team: int = team
        self.state: List[State] = []
        self.buff = {s: [] for s in Stat}
        self.event = {e: [] for e in EventType}
        self.stat = {s: champ_data[s] for s in Stat}
        self.hp = self.stat[Stat.MAX_HP]
        self.mp = self.stat[Stat.MP]
        self.action = None
        self.target: Union[Champion, None] = None

    def get_stat(self, stat_type) -> Union[int, float]:
        origin = self.stat[stat_type]
        buff = 0
        for b in self.buff[stat_type]:
            if b.is_absolute:
                origin += b.result()
                continue
            buff += b.result()

        return origin + (origin * buff)

    def cause_event(self, event_type, **kwargs):
        for e in self.event[event_type]:
            e.get(**kwargs)

    def set_death(self):
        try:
            if self.action is not None:
                self.action.interrupt()
                self.action = None
        except RuntimeError:
            print("Action Already terminated")
        self.state = [State.DEATH]

    def generate_mana(self, mana):
        self.mp = min(self.mp + mana, self.stat[Stat.MAX_MP])

    def get_damage(self, damage) -> Union[int, float]:
        damage.set_armor(self.stat[Stat.ARMOR])
        damage.set_magic_resistance(self.stat[Stat.MAGIC_RESISTANCE])
        reduced_damage = damage.calc()
        self.cause_event(EventType.GET_DAMAGE, damage=reduced_damage)
        self.generate_mana(damage.get_pre_mitigated() * 0.06)

        if reduced_damage is None:
            print("%s: Avoid damage" % self.name)
            return None
        self.hp = max(self.hp - reduced_damage, 0)
        if not self.hp:
            self.set_death()
        print("%s: Get Damage %d" % (self.name, reduced_damage))

        return reduced_damage

    def is_critical(self) -> bool:
        chance = min(100, self.stat[Stat.CRITICAL_CHANCE])
        result = random.choices([True, False], weights=[chance, 100 - chance])

        return result[0]

    def is_dodge(self) -> bool:
        chance = min(100, self.stat[Stat.DODGE_CHANCE])
        result = random.choices([True, False], weights=[chance, 100 - chance])

        return result[0]

    def is_dead(self) -> bool:
        if State.DEATH in self.state:
            return True
        return False

    def __repr__(self):
        return "%s" % self.name
