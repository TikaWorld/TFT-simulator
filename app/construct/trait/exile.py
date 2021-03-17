from typing import List, TYPE_CHECKING

from ..barrier import Barrier
from ..enum import EventType, Stat, TraitType
from .trait import Trait
from ..event import Event

if TYPE_CHECKING:
    from app.construct import Champion
    from ...action.state import StateManager
    from app.construct import Field


class ExileBarrier(Barrier):
    def __init__(self, champion: 'Champion'):
        super().__init__(0)


class ExileEnergyDrain(Event):
    def __init__(self, champion: 'Champion'):
        self.champion = champion

    def get(self, event_type, **kwargs):
        if event_type == EventType.BASIC_ATTACK:
            self.champion.heal(kwargs['damage']*0.8)


class Exile(Trait):
    def __init__(self, field: 'Field', state_manager: 'StateManager'):
        super().__init__(TraitType.EXILE, field, state_manager)

    def input_buff(self, champion):
        count = self.get_active_count()
        if 1 <= count:
            self.state_manager.put_barrier(champion, ExileBarrier(champion))
        if 2 <= count:
            self.state_manager.put_event(champion, EventType.BASIC_ATTACK, ExileEnergyDrain(champion))

    def check_around(self, champion: 'Champion'):
        cell = self.field.get_location(champion)
        for c in cell.connect:
            if not c.champion:
                continue
            if c.champion.team is champion.team:
                return False
        return True

    def activate(self, champions: List['Champion']):
        trait_champs = self.get_trait_champions(champions)
        for champion in trait_champs:
            if self.check_around(champion):
                self.input_buff(champion)
