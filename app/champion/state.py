from enum import Enum, auto


class State(str, Enum):
    STUN = auto()
    AIRBORNE = auto()
    DISARM = auto()
    ROOT = auto()
    TAUNT = auto()
    BANISHES = auto()
    DEATH = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
