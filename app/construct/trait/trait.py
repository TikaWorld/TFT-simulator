from abc import ABC, abstractmethod


class Trait(ABC):
    def __init__(self, trait_type):
        self.type = trait_type

    @abstractmethod
    def activate(self, champions):
        return NotImplemented

    def get_trait_champion(self, champions):
        return NotImplemented
