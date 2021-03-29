from typing import List, TYPE_CHECKING

from ..enum import Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class AssassinBuff(Buff):
    def __init__(self, critical_damage, critical_chance):
        super().__init__(is_absolute=True)
        self.critical_damage = critical_damage
        self.critical_chance = critical_chance

    def result(self, buff_type: Stat):
        if buff_type == Stat.CRITICAL_DAMAGE:
            return self.critical_damage
        if buff_type == Stat.CRITICAL_CHANCE:
            return self.critical_chance


class Assassin(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.ASSASSIN, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 3:
            return AssassinBuff(10, 25)
        elif 4 <= count < 5:
            return AssassinBuff(30, 55)
        elif 6 <= count:
            return AssassinBuff(50, 90)
        return None

    def activate(self, champions: List['Champion']):
        for champion in self.get_trait_champions(champions):
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.CRITICAL_DAMAGE, buff)
                self.state_manager.put_buff(champion, Stat.CRITICAL_CHANCE, buff)
