from typing import Dict, List

from app.action.champion import ChampionAction
from app.construct import Field, Team, Champion
from app.construct.trait import TRAIT
from app.construct.trait.trait import Trait


class Game:
    def __init__(self):
        self.field = Field()
        self.champion: Dict[Team, List[Champion]] = {}
        self.trait: Dict[Team, List[Trait]] = {}
        self.action = ChampionAction(self.field)

    def create_team(self) -> Team:
        t = Team()
        self.champion[t] = []
        return t

    def create_champion(self, team: Team, champ_data):
        c = Champion(champ_data, team)
        self.champion[team].append(c)
        for t in champ_data["trait"]:
            self.trait[team][t] = TRAIT[t]()

        return c

    def batch_champion(self, champion: Champion, loc: list[int]):
        self.field.assign(champion, loc)

    def init(self):
        for team_trait, team_champion in (self.trait.values(), self.champion.values()):
            for t in team_trait:
                t.activate(team_champion)

    def start(self):
        self.init()
        champions = []
        for c in self.champion.values():
            champions.extend(c)
        for c in champions:
            self.field.env.process(self.action.action(c))
        self.field.env.run(until=5)
