from typing import List, TYPE_CHECKING

from ..enum import Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ...action.state import StateManager

if TYPE_CHECKING:
    from battle.construct import Champion


class BrawlerBuff(Buff):
    def __init__(self, hp, attack_damage):
        super().__init__(is_absolute=True)
        self.hp = hp
        self.attack_damage = attack_damage

    def result(self, buff_type: Stat):
        if buff_type == Stat.MAX_HP:
            return self.hp
        if buff_type == Stat.ATTACK:
            return self.attack_damage


class Brawler(Trait):
    def __init__(self, field, state_manager: StateManager):
        super().__init__(TraitType.BRAWLER, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 3:
            return BrawlerBuff(400, 10)
        elif 4 <= count < 5:
            return BrawlerBuff(700, 20)
        elif 6 <= count < 7:
            return BrawlerBuff(1000, 40)
        elif 8 <= count:
            return BrawlerBuff(1400, 80)
        return None

    def activate(self, champions: List['Champion']):
        for champion in self.get_trait_champions(champions):
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.MAX_HP, buff)
                self.state_manager.put_buff(champion, Stat.ATTACK, buff)
