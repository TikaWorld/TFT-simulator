from typing import Union, TYPE_CHECKING

from battle.construct.enum import DamageType

if TYPE_CHECKING:
    from battle.construct import Champion


class Damage:
    def __init__(self, champion: 'Champion', damage: Union[int, float], damage_type: DamageType, **kwargs):
        self.champion = champion
        self.damage: Union[int, float] = damage
        self.type: DamageType = damage_type
        self.critical_damage: Union[int, None] = None
        self.is_miss: bool = False
        self.ignore_miss: bool = False
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

    def set_armor(self, armor: Union[int, float]):
        self.resist[DamageType.PHYSICAL] = armor

    def set_magic_resistance(self, magic_resistance: Union[int, float]):
        self.resist[DamageType.MAGIC] = magic_resistance

    def set_critical(self, critical_damage: int):
        self.critical_damage = critical_damage

    def set_miss(self, is_miss: bool):
        self.is_miss = is_miss

    def set_ignore_miss(self, ignore_miss: bool):
        self.critical_damage = ignore_miss

    def get_pre_mitigated(self):
        if self.is_miss and not self.ignore_miss:
            return 0
        result = self.damage
        if self.critical_damage:
            result *= (self.critical_damage / 100)
        return result

    def calc(self) -> Union[int, float, None]:
        if self.is_miss and not self.ignore_miss:
            return None
        result = self.damage * (100 / (100 + self.resist[self.type]))
        if self.critical_damage:
            result *= (self.critical_damage / 100)
        return result
