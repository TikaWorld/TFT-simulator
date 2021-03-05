from enum import Enum


class Event(str, Enum):
    BASIC_ATTACK = "basic_attack"
    GET_DAMAGE = "get_damage"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name