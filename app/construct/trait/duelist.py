from ..enum.event import Event
from ..enum.stat import Stat
from ..enum.trait import TraitType
from ..buff import Buff
from .trait import Trait


class DuelistBuff(Buff):
    def __init__(self, value):
        super().__init__(is_absolute=False)
        self.count = 0
        self.value = value

    def get(self, **kwargs):
        self.count = min(self.count+1, 5)

    def result(self):
        return self.value * self.count


class Duelist(Trait):
    def __init__(self):
        super().__init__(TraitType.Duelist)
        self.active_count = 0

    def activate(self, champion):
        buff = DuelistBuff(0.8)
        champion.buff[Stat.ATTACK_SPEED].append(buff)
        champion.event[Event.BASIC_ATTACK].append(buff)
