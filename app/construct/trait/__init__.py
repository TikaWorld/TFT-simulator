from app.construct.enum import TraitType
from app.construct.trait.divine import Divine
from app.construct.trait.duelist import Duelist
from app.construct.trait.exile import Exile

TRAIT = {
    TraitType.DUELIST: Duelist,
    TraitType.DIVINE: Divine,
    TraitType.EXILE: Exile
}