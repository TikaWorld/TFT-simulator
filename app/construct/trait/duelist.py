from typing import List, TYPE_CHECKING

from ..enum import EventType, Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ..event import Event
from ...action.state import StateManager

if TYPE_CHECKING:
    from app.construct import Champion


class DuelistBuff(Buff, Event):
    def __init__(self, value):
        super().__init__(is_absolute=False)
        self.count = 0
        self.value = value

    def get(self, event_type, **kwargs):
        if event_type == EventType.BASIC_ATTACK:
            self.count = min(self.count+1, 8)

    def result(self):
        return self.value * self.count


class DuelistHeistBuff(Buff):
    def __init__(self):
        super().__init__(is_absolute=False)

    def result(self):
        return 0.5


class Duelist(Trait):
    def __init__(self, state_manager: StateManager):
        super().__init__(TraitType.DUELIST, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 4:
            return DuelistBuff(0.15)
        elif 4 <= count < 6:
            return DuelistBuff(0.25)
        elif 6 <= count < 8:
            return DuelistBuff(0.40)
        elif 8 <= count:
            return DuelistBuff(0.60)
        return None

    def activate(self, champions: List['Champion']):
        trait_champs = self.get_trait_champions(champions)
        for champion in trait_champs:
            self.state_manager.put_buff(champion, Stat.HEIST, DuelistHeistBuff())
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.ATTACK_SPEED, buff)
                self.state_manager.put_event(champion, EventType.BASIC_ATTACK, buff)
