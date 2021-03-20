from battle.construct.enum import TraitType
from battle.construct.trait.assassin import Assassin
from battle.construct.trait.brawler import Brawler
from battle.construct.trait.divine import Divine
from battle.construct.trait.duelist import Duelist
from battle.construct.trait.enlightened import Enlightened
from battle.construct.trait.exile import Exile
from battle.construct.trait.keeper import Keeper
from battle.construct.trait.mystic import Mystic
from battle.construct.trait.ninja import Ninja
from battle.construct.trait.spirit import Spirit
from battle.construct.trait.vanguard import Vanguard
from battle.construct.trait.warlord import Warlord

TRAIT = {
    TraitType.ASSASSIN: Assassin,
    TraitType.BRAWLER: Brawler,
    TraitType.DIVINE: Divine,
    TraitType.DUELIST: Duelist,
    TraitType.ENLIGHTENED: Enlightened,
    TraitType.EXILE: Exile,
    TraitType.KEEPER: Keeper,
    TraitType.MYSTIC: Mystic,
    TraitType.NINJA: Ninja,
    TraitType.SPIRIT: Spirit,
    TraitType.VANGUARD: Vanguard,
    TraitType.WARLORD: Warlord
}