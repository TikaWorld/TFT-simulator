from typing import List, TYPE_CHECKING

from ..barrier import Barrier
from ..enum import EventType, Stat, TraitType
from .trait import Trait
from ..event import Event

if TYPE_CHECKING:
    from battle.construct import Champion
    from ...action.state import StateManager
    from battle.construct import Field
    from ..field import Cell


class KeeperBarrier(Barrier):
    def __init__(self, value: int):
        super().__init__(value)


class KeeperStartEvent(Event):
    def __init__(self, champion_cell: 'Cell', state_manager: 'StateManager', count: int):
        self.champion_cell = champion_cell
        self.state_manager = state_manager
        self.count = count
        self.team = champion_cell.champion.team

    def input_around(self):
        self.input_barrier(self.champion_cell.champion)
        for c in self.champion_cell.connect:
            if c.champion and c.champion.team is self.team:
                self.input_barrier(c.champion)

    def input_barrier(self, champion):
        barrier_performance = 2 if TraitType.KEEPER in champion.traits else 1
        if 2 <= self.count < 3:
            self.state_manager.put_barrier(champion, KeeperBarrier(150*barrier_performance), time=8)
        elif 4 <= self.count < 5:
            self.state_manager.put_barrier(champion, KeeperBarrier(200*barrier_performance), time=10)
        elif 6 <= self.count:
            self.state_manager.put_barrier(champion, KeeperBarrier(250*barrier_performance), time=12)

    def get(self, event_type, **kwargs):
        if event_type == EventType.BATTLE_START:
            self.input_around()


class Keeper(Trait):
    def __init__(self, field: 'Field', state_manager: 'StateManager'):
        super().__init__(TraitType.EXILE, field, state_manager)

    def activate(self, champions: List['Champion']):
        trait_champs = self.get_trait_champions(champions)
        for champion in trait_champs:
            champion_cell = self.field.get_location(champion)
            self.state_manager.put_event(champion, EventType.BATTLE_START,
                                         KeeperStartEvent(champion_cell, self.state_manager, self.get_active_count()))
