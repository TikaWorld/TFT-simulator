from typing import List, TYPE_CHECKING

from ..enum import Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class VanguardBuff(Buff):
    def __init__(self, armor, magic_resistance):
        super().__init__(is_absolute=True)
        self.armor = armor
        self.magic_resistance = magic_resistance

    def result(self, buff_type: Stat):
        if buff_type == Stat.ARMOR:
            return self.armor
        if buff_type == Stat.MAGIC_RESISTANCE:
            return self.magic_resistance


class Vanguard(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.VANGUARD, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 3:
            return VanguardBuff(250, 25)
        elif 4 <= count < 5:
            return VanguardBuff(500, 50)
        elif 6 <= count < 7:
            return VanguardBuff(500, 50)
        elif 8 <= count:
            return VanguardBuff(800, 80)
        return None

    def activate(self, champions: List['Champion']):
        for champion in self.get_trait_champions(champions):
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.ARMOR, buff)
                self.state_manager.put_buff(champion, Stat.MAGIC_RESISTANCE, buff)
