from .champion import Champion


class Team:
    def __init__(self):
        self.champions = []
        self.trait = []
        self.items = []

    def create_champion(self, champ_data):
        c = Champion(champ_data, id(self))
        self.champions.append(c)
        return c
