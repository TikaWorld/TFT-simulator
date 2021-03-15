from typing import List, TYPE_CHECKING

from ..enum import EventType, Stat, TraitType
from ..buff import Buff
from .trait import Trait
from ..event import Event
from ...action.state import StateManager

if TYPE_CHECKING:
    from app.construct import Champion


class DivineBuff(Buff, Event):
    def __init__(self, env, value):
        super().__init__(is_absolute=False)
        self.count = 0
        self.value = value
        self.activate = False
        self.is_activated = False
        self.env = env

    def get(self, event_type, **kwargs):
        if self.is_activated:
            return
        if event_type == EventType.BASIC_ATTACK:
            self.count += 1
            if self.count >= 6:
                self.is_activated = True
        if event_type == EventType.GET_DAMAGE:
            max_hp = kwargs['max_hp']
            hp = kwargs['hp']
            if (hp/max_hp) <= 0.5:
                self.is_activated = True
        if self.is_activated:
            self.env.process(self.activate_divine())

    def activate_divine(self):
        self.activate = True
        yield self.env.timeout(5)
        self.activate = False

    def result(self):
        if self.activate:
            return self.value
        return 0


class Divine(Trait):
    def __init__(self, state_manager: StateManager):
        super().__init__(TraitType.DUELIST, state_manager)

    def get_buff(self):
        count = self.get_active_count()
        if 1 <= count < 4:
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
                self.state_manager.put_buff(champion, Stat.ATTACK_SPEED, buff)
                self.state_manager.put_event(champion, EventType.BASIC_ATTACK, buff)
                self.state_manager.put_event(champion, EventType.GET_DAMAGE, buff)
