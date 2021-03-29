import os
import random
import json
from pathlib import Path
from typing import List, Union, TYPE_CHECKING, Iterable

from battle.construct.enum import EventType, Stat, State

if TYPE_CHECKING:
    from battle.construct import Team
    from battle.construct.barrier import Barrier

PROJECT_DIR = str(Path(os.path.abspath(__file__)).parent.parent.absolute())


def load_champion_data(path):
    result = {}
    with open(path + "/resource/champion.json", "r") as ch_json:
        champion_data = json.load(ch_json)
    list(map(lambda d: result.update({d["championId"]: d}), champion_data))
    return result


CHAMPION_DATA = load_champion_data(PROJECT_DIR)


class Champion:
    def __init__(self, champ_data, team: "Team"):
        self.name = champ_data["name"]
        self.uuid = champ_data["uuid"]
        self.id = champ_data["championId"]
        self.level = champ_data["level"]
        self.team: Team = team
        self.traits = champ_data["traits"]
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
        self.hp = min(self.get_stat(Stat.MAX_HP), self.hp + value)

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

    def generate_mana(self, mana, cause_event=True):
        if cause_event:
            self.cause_event(EventType.GENERATE_MP, mp=mana, champion=self)
        self.mp = min(self.mp + mana, self.get_stat(Stat.MAX_MP))

    def get_damage(self, damage) -> Union[int, float, None]:
        damage.set_armor(self.get_stat(Stat.ARMOR))
        damage.set_magic_resistance(self.get_stat(Stat.MAGIC_RESISTANCE))
        damage.set_damage_reduce(self.get_stat(Stat.DAMAGE_REDUCE))
        reduced_damage = damage.calc()
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

    def __iter__(self) -> Iterable[str]:
        result = [
            ("name", self.name),
            ("uuid", self.uuid),
            ("id", self.id),
            ("level", self.level),
            ("team", str(self.team)),
            ("traits", self.traits),
            ("skill", self.skill),
            ("state", self.state),
            ("hp", self.hp),
            ("mp", self.mp),
        ]
        stat = {}
        barrier = 0
        for s in Stat:
            stat[s] = self.get_stat(s)
        for b in self.barrier:
            barrier += b.value
        result.append(("stat", stat))
        result.append(("barrier", barrier))

        return iter(result)
