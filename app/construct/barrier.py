from typing import Union


class Barrier:
    def __init__(self, value):
        self.value = value

    def calc(self, dmg: Union[int, float]) -> Union[int, float]:
        self.value -= dmg
        if self.value <= 0:
            residual = abs(self.value)
            self.value = 0
            return residual
        return 0
