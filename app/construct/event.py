from abc import ABC, abstractmethod


class Event(ABC):
    @abstractmethod
    def get(self, event_type):
        return NotImplemented
