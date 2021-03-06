from .champion import Champion
from .trait import TRAIT


class Team:
    def __init__(self):
        self.champions = []
        self.trait = {}
        self.items = []

    def create_champion(self, champ_data):
        c = Champion(champ_data, id(self))
        self.champions.append(c)
        for t in champ_data["trait"]:
            self.trait[t] = TRAIT[t]()
        return c

    def init(self):
        for t in self.trait.values():
            t.activate(self.champions)
