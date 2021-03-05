from app.construct.enum.damage import DamageType


class Damage:
    def __init__(self, damage, damage_type, **kwargs):
        self.damage = damage
        self.type = damage_type
        self.critical_damage = None
        self.is_miss = False
        self.ignore_miss = False
        self.resist = {
            DamageType.PHYSICAL: 0,
            DamageType.MAGIC: 0,
            DamageType.TRUE: 0,
        }

        if "critical_damage" in kwargs.keys():
            self.critical_damage = kwargs["critical_damage"]
        if "is_miss" in kwargs.keys():
            self.is_miss = kwargs["is_miss"]
        if "ignore_miss" in kwargs.keys():
            self.ignore_miss = kwargs["ignore_miss"]
        if "armor" in kwargs.keys():
            self.resist[DamageType.PHYSICAL] = kwargs["armor"]
        if "magic_resistance" in kwargs.keys():
            self.resist[DamageType.MAGIC] = kwargs["magic_resistance"]

    def set_armor(self, armor):
        self.resist[DamageType.PHYSICAL] = armor

    def set_magic_resistance(self, magic_resistance):
        self.resist[DamageType.MAGIC] = magic_resistance

    def set_critical(self, critical_damage):
        self.critical_damage = critical_damage

    def set_miss(self, is_miss):
        self.is_miss = is_miss

    def set_ignore_miss(self, ignore_miss):
        self.critical_damage = ignore_miss

    def get_pre_mitigated(self):
        if self.is_miss and not self.ignore_miss:
            return 0
        result = self.damage
        if self.critical_damage:
            result *= (self.critical_damage / 100)
        return result

    def calc(self):
        if self.is_miss and not self.ignore_miss:
            return None
        result = self.damage * (100 / (100 + self.resist[self.type]))
        if self.critical_damage:
            result *= (self.critical_damage / 100)
        return result
