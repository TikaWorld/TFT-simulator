from typing import List

from .. import Champion
from ..enum import EventType, Stat, TraitType
from ..buff import Buff
from .trait import Trait


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
        super().__init__(TraitType.Duelist)
        self.active_count = 0

    def activate(self, champions: List[Champion]):
        for champion in champions:
            buff = DuelistBuff(0.15)
            champion.buff[Stat.ATTACK_SPEED].append(buff)
            champion.event[EventType.BASIC_ATTACK].append(buff)
