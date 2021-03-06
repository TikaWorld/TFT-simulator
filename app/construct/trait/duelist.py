from typing import List, TYPE_CHECKING

from ..enum import EventType, Stat, TraitType
from ..buff import Buff
from .trait import Trait

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
    def __init__(self):
        super().__init__(TraitType.DUELIST)
        self.active_count = 0

    def activate(self, champions: List["Champion"]):
        trait_champs = self.get_trait_champions(champions)
        for champion in trait_champs:
            buff = DuelistBuff(0.15)
            champion.buff[Stat.ATTACK_SPEED].append(buff)
            champion.event[EventType.BASIC_ATTACK].append(buff)
