from enum import Enum


class Stat(str, Enum):
    MAX_HP = "max_hp"
    MAX_MP = "max_mp"
    MP = "mp"
    HEIST = "heist"
    ATTACK = "attack_damage"
    SPELL = "spell_power"
    CRITICAL_CHANCE = "critical_strike_chance"
    CRITICAL_DAMAGE = "critical_strike_damage"
    RANGE = "range"
    ARMOR = "armor"
    MAGIC_RESISTANCE = "magic_resistance"
    ATTACK_SPEED = "attack_speed"
    DODGE_CHANCE = "dodge_chance"

    DAMAGE_REDUCE = "damage_reduce"
    DAMAGE_INCREASE = "damage_increase"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
