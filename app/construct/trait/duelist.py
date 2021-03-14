from typing import List, TYPE_CHECKING

from ..enum import EventType, Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ...action.state import StateManager

if TYPE_CHECKING:
    from app.construct import Champion


class DuelistBuff(Buff):
    def __init__(self, value):
        super().__init__(is_absolute=False)
        self.count = 0
        self.value = value

    def get(self, **kwargs):
        self.count = min(self.count+1, 8)

    def result(self):
        return self.value * self.count


class Duelist(Trait):
    def __init__(self, state_manager: StateManager):
        super().__init__(TraitType.DUELIST, state_manager)
        self.active_count = 0

    def activate(self, champions: List['Champion']):
        trait_champs = self.get_trait_champions(champions)
        for champion in trait_champs:
            buff = DuelistBuff(0.15)
            self.state_manager.put_buff(champion, Stat.ATTACK_SPEED, buff)
            self.state_manager.put_event(champion, EventType.BASIC_ATTACK, buff)
