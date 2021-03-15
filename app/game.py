from typing import Dict, List

from app.action.champion import ChampionAction
from app.action.state import StateManager
from app.construct import Field, Team, Champion
from app.construct.trait import TRAIT
from app.construct.trait.trait import Trait


class Game:
    def __init__(self):
        self.field = Field()
        self.champion: Dict[Team, List[Champion]] = {}
        self.trait: Dict[Team, Dict[Trait]] = {}
        self.action = ChampionAction(self.field)
        self.state_manager = StateManager(self.field.env)

    def create_team(self) -> Team:
        t = Team()
        self.champion[t] = []
        self.trait[t] = {}

        return t

    def create_champion(self, team: Team, champ_data):
        c = Champion(champ_data, team)
        self.champion[team].append(c)
        for t in champ_data["trait"]:
            if t not in self.trait[team]:
                self.trait[team][t] = TRAIT[t](self.state_manager)
            self.trait[team][t].add_active_key(c)

        return c

    def batch_champion(self, champion: Champion, loc: list[int]):
        self.field.assign(champion, loc)

    def init(self):
        for team_trait, team_champion in zip(self.trait.values(), self.champion.values()):
            for t in team_trait.values():
                t.activate(team_champion)

    def start(self):
        self.init()
        champions = []
        for c in self.champion.values():
            champions.extend(c)
        for c in champions:
            self.field.env.process(self.action.action(c))
        self.field.env.run(until=5)
