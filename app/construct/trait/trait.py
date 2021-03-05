from abc import ABC, abstractmethod
from typing import List

from app.construct import Champion
from app.construct.enum import TraitType


class Trait(ABC):
    def __init__(self, trait_type: TraitType):
        self.type = trait_type

    @abstractmethod
    def activate(self, champions: List[Champion]):
        return NotImplemented

    def get_trait_champion(self, champions):
        return NotImplemented
