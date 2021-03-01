from app.champion.state import State
from enum import Enum, auto


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


class Champion(object):
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
        self.armor = 40
        self.spell_power = 100
        self.magic_resistance = 40
        self.critical = 25
        self.attack_speed = 1
        self.range = 1
        self.action = None
        self.target = None
        self.pos = None

    def get_damage(self, attack_damage, magic=False):
        resist_value = self.armor if not magic else self.magic_resistance
        damage_multiplier = 100 / (100 + resist_value)
        reduced_damage = attack_damage * damage_multiplier
        self.hp = max(self.hp - reduced_damage, 0)
        if not self.hp:
            try:
                self.action.interrupt()
            except RuntimeError:
                print("Action Already terminated")
            self.state = [State.DEATH]
        print("%s: Get Damage %d" % (self.name, reduced_damage))

        return reduced_damage

    def __repr__(self):
        return "%s" % self.name
