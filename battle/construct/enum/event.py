from enum import Enum


class EventType(str, Enum):
    BATTLE_START = "battle_start"
    BASIC_ATTACK = "basic_attack"
    GET_DAMAGE = "get_damage"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
