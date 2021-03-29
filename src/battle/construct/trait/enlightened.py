from typing import List, TYPE_CHECKING

from ..enum import TraitType, EventType
from .trait import Trait
from ..event import Event
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class EnlightenedBuff(Event):
    def __init__(self, value):
        self.value = value

    def get(self, event_type, **kwargs):
        if event_type == EventType.GENERATE_MP:
            mp = kwargs["mp"]
            champion: 'Champion' = kwargs["champion"]
            additional_mana = mp + mp*self.value
            champion.generate_mana(additional_mana, cause_event=False)


class Enlightened(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.MYSTIC, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 3:
            return EnlightenedBuff(0.5)
        elif 4 <= count < 5:
            return EnlightenedBuff(1.0)
        elif 6 <= count:
            return EnlightenedBuff(1.5)
        return None

    def activate(self, champions: List['Champion']):
        for champion in self.get_trait_champions(champions):
            buff = self.get_buff()
            if buff:
                self.state_manager.put_event(champion, EventType.GENERATE_MP, buff)
