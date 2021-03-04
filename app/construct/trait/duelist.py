from ..champion import Stat, Event


class DuelistBuff:
    def __init__(self, value):
        self.count = 0
        self.value = value
        self.is_absolute = False

    def get(self, **kwargs):
        self.count = min(self.count+1, 5)

    def result(self):
        return self.value * self.count


class Duelist:
    def __init__(self):
        self.active_count = 0

    def activate(self, champion):
        buff = DuelistBuff(0.8)
        champion.buff[Stat.ATTACK_SPEED].append(buff)
        champion.event[Event.BASIC_ATTACK].append(buff)
