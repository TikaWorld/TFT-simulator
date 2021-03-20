from enum import Enum


class EventType(str, Enum):
    BATTLE_START = "battle_start"
    BASIC_ATTACK = "basic_attack"
    BASIC_ATTACK_TYPE_SKILL = "basic_attack_type_skill"
    CASTING_SKILL = "casting_skill"
    GENERATE_MP = "generate_mp"
    GET_DAMAGE = "get_damage"


    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
