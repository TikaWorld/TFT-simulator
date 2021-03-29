from typing import List, TYPE_CHECKING

from ..enum import EventType, Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ..event import Event
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class SpiritBuff(Buff, Event):
    def __init__(self, value):
        super().__init__(is_absolute=False)
        self.value = value
        self.skill_use = []

    def get(self, event_type, **kwargs):
        if event_type in [EventType.CASTING_SKILL, EventType.BASIC_ATTACK_TYPE_SKILL]:
            champion = kwargs["champion"]
            if champion not in self.skill_use:
                self.skill_use.append(champion)

    def result(self, buff_type: Stat):
        if buff_type == Stat.ATTACK_SPEED:
            return self.value * len(self.skill_use)


class Spirit(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.SPIRIT, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 3:
            return SpiritBuff(0.2)
        elif 4 <= count:
            return SpiritBuff(0.35)
        return None

    def activate(self, champions: List['Champion']):
        buff = self.get_buff()
        if not buff:
            return
        for champion in champions:
            self.state_manager.put_buff(champion, Stat.ATTACK_SPEED, buff)
        for champion in self.get_trait_champions(champions):
            self.state_manager.put_event(champion, EventType.CASTING_SKILL, buff)
