from enum import Enum, auto


class DamageType(str, Enum):
    MAGIC = auto()
    PHYSICAL = auto()
    TRUE = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Damage:
    def __init__(self, damage, damage_type, **kwargs):
        self.damage = damage
        self.type = damage_type
        self.critical_damage = None
        self.is_miss = False
        self.ignore_miss = False
        self.armor = 0
        self.magic_resistance = 0

        if "critical_damage" in kwargs.keys():
            self.critical_damage = kwargs["critical_damage"]
        if "is_miss" in kwargs.keys():
            self.is_miss = kwargs["is_miss"]
        if "ignore_miss" in kwargs.keys():
            self.ignore_miss = kwargs["ignore_miss"]
        if "armor" in kwargs.keys():
            self.armor = kwargs["armor"]
        if "magic_resistance" in kwargs.keys():
            self.magic_resistance = kwargs["magic_resistance"]

    def _get_resist_value(self):
        resist_value = None
        if self.type == DamageType.PHYSICAL:
            resist_value = self.armor
        elif self.type == DamageType.MAGIC:
            resist_value = self.magic_resistance
        elif self.type == DamageType.TRUE:
            resist_value = 0

        return resist_value

    def set_armor(self, armor):
        self.armor = armor

    def set_magic_resistance(self, magic_resistance):
        self.magic_resistance = magic_resistance

    def set_critical(self, critical_damage):
        self.critical_damage = critical_damage

    def set_miss(self, is_miss):
        self.is_miss = is_miss

    def set_ignore_miss(self, ignore_miss):
        self.critical_damage = ignore_miss

    def calc(self):
        if self.is_miss and not self.ignore_miss:
            return None
        r = self._get_resist_value()
        result = self.damage * (100 / (100 + r))
        if self.critical_damage:
            result *= (self.critical_damage/100)
        return result
