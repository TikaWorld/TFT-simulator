from enum import Enum, auto


class DamageType(str, Enum):
    MAGIC = auto()
    PHYSICAL = auto()
    TRUE = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name