from abc import ABC, abstractmethod

from app.construct.enum import Stat


class Buff(ABC):
    def __init__(self, is_absolute: bool):
        self.is_absolute = is_absolute

    @abstractmethod
    def result(self, buff_type: Stat):
        return NotImplemented
