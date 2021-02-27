from enum import Enum, auto


class StrEnum(str, Enum):

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class State(StrEnum):
    STUN = auto()
    AIRBORNE = auto()
    DISARM = auto()
    ROOT = auto()
    TAUNT = auto()
    BANISHES = auto()
