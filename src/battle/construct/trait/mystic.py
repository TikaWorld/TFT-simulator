from typing import List, TYPE_CHECKING

from ..enum import Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class MysticBuff(Buff):
    def __init__(self, magic_resistance):
        super().__init__(is_absolute=True)
        self.value = magic_resistance

    def result(self, buff_type: Stat):
        if buff_type == Stat.MAGIC_RESISTANCE:
            return self.value


class Mystic(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.MYSTIC, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 3:
            return MysticBuff(40)
        elif 4 <= count < 5:
            return MysticBuff(120)
        elif 6 <= count:
            return MysticBuff(300)
        return None

    def activate(self, champions: List['Champion']):
        for champion in champions:
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.MAGIC_RESISTANCE, buff)
