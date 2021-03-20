from enum import Enum, auto


class TraitType(str, Enum):
    ADEPT = "Set4_Adept"
    ASSASSIN = "Set4_Assassin"
    BOSS = "Boss"
    BLACKSMITH = "Set4_Blacksmith"
    BRAWLER = "Set4_Brawler"
    CULTIST = "Cultist"
    DAREDEVIL = "Set4_Daredevil"
    DIVINE = "Divine"
    DRAGONSOUL = "Set4_Dragonsoul"
    DUELIST = "Duelist"
    ELDERWOOD = "Set4_Elderwood"
    EMPEROR = "Emperor"
    ENLIGHTENED = "Set4_Enlightened"
    EXILE = "Set4_Exile"
    EXECUTIONER = "Set4_Executioner"
    FABLED = "Set4_Fabled"
    FORTUNE = "Fortune"
    KEEPER = "Keeper"
    MAGE = "Set4_Mage"
    MYSTIC = "Set4_Mystic"
    NINJA = "Set4_Ninja"
    SHARPSHOOTER = "Sharpshooter"
    SPIRIT = "Set4_Spirit"
    SLAYER = "Set4_Slayer"
    SYPHONER = "Set4_Syphoner"
    VANGUARD = "Set4_Vanguard"
    WARLORD = "Warlord"


    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
