from typing import List, TYPE_CHECKING, Union

from ..enum import EventType, Stat, TraitType, DamageType
from ..buff import Buff
from .trait import Trait
from ..event import Event
from battle.construct import Damage

if TYPE_CHECKING:
    from battle.construct import Champion
    from ...action.state import StateManager
    from battle.construct import Field


class DivineBuff(Buff, Event):
    def __init__(self, env, value):
        super().__init__(is_absolute=True)
        self.count = 0
        self.value = value
        self.activate = False
        self.is_activated = False
        self.env = env

    def get(self, event_type, **kwargs):
        if self.is_activated:
            if event_type == EventType.BASIC_ATTACK:
                self.divine_attack(kwargs['champion'], kwargs['targets'], kwargs['damage'])
        if event_type == EventType.BASIC_ATTACK:
            self.count += 1
            if self.count >= 6:
                self.is_activated = True
        if event_type == EventType.GET_DAMAGE:
            max_hp = kwargs['max_hp']
            hp = kwargs['hp']
            if (hp / max_hp) <= 0.5:
                self.is_activated = True
        if self.is_activated:
            self.env.process(self.activate_divine())

    def divine_attack(self, champion: 'Champion', targets: List['Champion'], dmg: Union[int, float]):
        for target in targets:
            target.get_damage(Damage(champion, dmg*self.value, damage_type=DamageType.TRUE))

    def activate_divine(self):
        self.activate = True
        yield self.env.timeout(5)
        self.activate = False

    def result(self, buff_type):
        if self.activate:
            if buff_type == Stat.DAMAGE_REDUCE:
                return self.value
        return 0


class Divine(Trait):
    def __init__(self, field: 'Field', state_manager: 'StateManager'):
        super().__init__(TraitType.DIVINE, field, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 2 <= count < 4:
            return DivineBuff(self.state_manager.env, 0.25)
        elif 4 <= count < 6:
            return DivineBuff(self.state_manager.env, 0.40)
        elif 6 <= count < 8:
            return DivineBuff(self.state_manager.env, 0.55)
        elif 8 <= count:
            return DivineBuff(self.state_manager.env, 0.70)
        return None

    def activate(self, champions: List['Champion']):
        trait_champs = self.get_trait_champions(champions)
        for champion in trait_champs:
            buff = self.get_buff()
            if buff:
                self.state_manager.put_buff(champion, Stat.DAMAGE_REDUCE, buff)
                self.state_manager.put_event(champion, EventType.BASIC_ATTACK, buff)
                self.state_manager.put_event(champion, EventType.BASIC_ATTACK_TYPE_SKILL, buff)
                self.state_manager.put_event(champion, EventType.CASTING_SKILL, buff)
                self.state_manager.put_event(champion, EventType.GET_DAMAGE, buff)
