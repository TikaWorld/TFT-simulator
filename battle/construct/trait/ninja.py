from typing import List, TYPE_CHECKING

from ..enum import Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class NinjaBuff(Buff):
    def __init__(self, attack_damage, spell_power):
        super().__init__(is_absolute=True)
        self.attack_damage = attack_damage
        self.spell_power = spell_power

    def result(self, buff_type: Stat):
        if buff_type == Stat.ATTACK:
            return self.attack_damage
        if buff_type == Stat.SPELL:
            return self.spell_power


class Ninja(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.NINJA, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 1 == count:
            return NinjaBuff(50, 50)
        elif 4 == count:
            return NinjaBuff(150, 150)
        return None

    def activate(self, champions: List['Champion']):
        for champion in self.get_trait_champions(champions):
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.MAGIC_RESISTANCE, buff)
