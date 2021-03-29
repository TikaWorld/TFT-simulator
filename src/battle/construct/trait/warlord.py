from typing import List, TYPE_CHECKING

from ..enum import Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class WarlordBuff(Buff):
    def __init__(self, health, spell_power):
        super().__init__(is_absolute=True)
        self.health = health
        self.spell_power = spell_power

    def result(self, buff_type: Stat):
        if buff_type == Stat.MAX_HP:
            return self.health
        if buff_type == Stat.SPELL:
            return self.spell_power


class Warlord(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.WARLORD, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 3 <= count < 5:
            return WarlordBuff(250, 25)
        elif 6 <= count < 8:
            return WarlordBuff(400, 40)
        elif 9 <= count:
            return WarlordBuff(700, 70)
        return None

    def activate(self, champions: List['Champion']):
        trait_champs = self.get_trait_champions(champions)
        for champion in trait_champs:
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.MAX_HP, buff)
                self.state_manager.put_buff(champion, Stat.SPELL, buff)
