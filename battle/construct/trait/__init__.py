from battle.construct.enum import TraitType
from battle.construct.trait.divine import Divine
from battle.construct.trait.duelist import Duelist
from battle.construct.trait.exile import Exile

TRAIT = {
    TraitType.DUELIST: Duelist,
    TraitType.DIVINE: Divine,
    TraitType.EXILE: Exile
}