from .state import State
from .damage import DamageType
from enum import Enum
import random


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

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Champion:
    def __init__(self, team, name="Dummy"):
        self.name = name
        self.team = team
        self.state = []
        self.buff = {}
        self.max_hp = 100
        self.max_mp = 0
        self.hp = self.max_hp
        self.mp = 0
        self.heist = 550
        self.attack_damage = 100
        self.armor = 100
        self.spell_power = 100
        self.magic_resistance = 40
        self.critical_chance = 25
        self.critical_damage = 150
        self.dodge_chance = 0
        self.attack_speed = 1
        self.range = 1
        self.action = None
        self.target = None
        self.pos = None

    def _get_resist_value(self, damage_type):
        resist_value = None
        if damage_type == DamageType.PHYSICAL:
            resist_value = self.armor
        elif damage_type == DamageType.MAGIC:
            resist_value = self.magic_resistance
        elif damage_type == DamageType.TRUE:
            resist_value = 0

        return resist_value

    def set_death(self):
        try:
            if self.action is not None:
                self.action.interrupt()
        except RuntimeError:
            print("Action Already terminated")
        self.state = [State.DEATH]

    def get_damage(self, damage):
        damage.set_armor(self.armor)
        damage.set_magic_resistance(self.magic_resistance)
        reduced_damage = damage.calc()

        if not reduced_damage:
            print("%s: Avoid damage" % self.name)
            return None
        self.hp = max(self.hp - reduced_damage, 0)
        if not self.hp:
            self.set_death()
        print("%s: Get Damage %d" % (self.name, reduced_damage))

        return reduced_damage

    def is_critical(self):
        chance = min(100, self.critical_chance)
        result = random.choices([True, False], weights=[chance, 100-chance])

        return result[0]

    def is_dodge(self):
        chance = min(100, self.dodge_chance)
        result = random.choices([True, False], weights=[chance, 100-chance])

        return result[0]

    def is_dead(self):
        if State.DEATH in self.state:
            return True
        return False

    def __repr__(self):
        return "%s" % self.name
