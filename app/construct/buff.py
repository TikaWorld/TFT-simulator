from abc import ABC, abstractmethod


class Buff(ABC):
    def __init__(self, is_absolute: bool):
        self.is_absolute = is_absolute

    @abstractmethod
    def result(self):
        return NotImplemented
