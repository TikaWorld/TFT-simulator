from .state import State
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
    DODGE_CHANCE = "dodge_chance"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Champion:
    def __init__(self, champ_data, team):
        self.name = champ_data["name"]
        self.team = team
        self.state = []
        self.buff = {}
        self.stat = {s: champ_data[s] for s in Stat}
        self.hp = self.stat[Stat.MAX_HP]
        self.mp = self.stat[Stat.MP]
        self.action = None
        self.target = None
        self.pos = None

    def set_death(self):
        try:
            if self.action is not None:
                self.action.interrupt()
        except RuntimeError:
            print("Action Already terminated")
        self.state = [State.DEATH]

    def generate_mana(self, mana):
        self.mp = max(self.mp+mana, self.stat[Stat.MAX_MP])

    def get_damage(self, damage):
        damage.set_armor(self.stat[Stat.ARMOR])
        damage.set_magic_resistance(self.stat[Stat.MAGIC_RESISTANCE])
        reduced_damage = damage.calc()
        self.generate_mana(damage.get_pre_mitigated() * 0.06)

        if not reduced_damage:
            print("%s: Avoid damage" % self.name)
            return None
        self.hp = max(self.hp - reduced_damage, 0)
        if not self.hp:
            self.set_death()
        print("%s: Get Damage %d" % (self.name, reduced_damage))

        return reduced_damage

    def is_critical(self):
        chance = min(100, self.stat[Stat.CRITICAL_CHANCE])
        result = random.choices([True, False], weights=[chance, 100 - chance])

        return result[0]

    def is_dodge(self):
        chance = min(100, self.stat[Stat.DODGE_CHANCE])
        result = random.choices([True, False], weights=[chance, 100 - chance])

        return result[0]

    def is_dead(self):
        if State.DEATH in self.state:
            return True
        return False

    def __repr__(self):
        return "%s" % self.name
