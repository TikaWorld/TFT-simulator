from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from app.construct.enum import TraitType

if TYPE_CHECKING:
    from app.construct import Champion


class Trait(ABC):
    def __init__(self, trait_type: TraitType):
        self.type = trait_type

    @abstractmethod
    def activate(self, champions: List["Champion"]):
        return NotImplemented

    def get_trait_champions(self, champions: List["Champion"]) -> List["Champion"]:
        result = []
        for c in champions:
            if self.type in c.trait:
                result.append(c)
        return result

