from enum import Enum, auto


class TraitType(str, Enum):
    DUELIST = "Duelist"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name