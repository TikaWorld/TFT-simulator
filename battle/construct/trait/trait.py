from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from battle.action.state import StateManager
from battle.construct.enum import TraitType

if TYPE_CHECKING:
    from battle.construct import Champion, Field


class Trait(ABC):
    def __init__(self, trait_type: TraitType, field: 'Field', state_manager: StateManager):
        self.type = trait_type
        self.state_manager = state_manager
        self.field = field
        self.active_list = []

    @abstractmethod
    def activate(self, champions: List['Champion']):
        return NotImplemented

    def add_active_key(self, champion):
        if champion.id in self.active_list:
            return
        self.active_list.append(champion.id)

    def get_active_count(self) -> int:
        return len(self.active_list)

    def get_trait_champions(self, champions: List['Champion']) -> List['Champion']:
        result = []
        for c in champions:
            if self.type in c.traits:
                result.append(c)
        return result

