from abc import ABC, abstractmethod

from battle.construct.enum import Stat


class Buff(ABC):
    def __init__(self, is_absolute: bool, debuff=False):
        self.is_absolute = is_absolute
        self.debuff = debuff

    @abstractmethod
    def result(self, buff_type: Stat):
        return NotImplemented
