import copy
import uuid
from typing import Dict, List

import simpy

from battle.action.champion import ChampionAction
from battle.action.state import StateManager
from battle.construct import Field, Team, Champion, CHAMPION_DATA, TRAIT
from battle.construct.enum import EventType

from battle.construct.trait.trait import Trait
from battle.logger import make_battle_logger


def preprocess_champ_data(data, level):
    result = copy.deepcopy(data["stat"][str(level)])
    result["name"] = data["name"]
    result["uuid"] = str(uuid.uuid4())
    result["level"] = level
    result["championId"] = data["championId"]
    result["cost"] = data["cost"]
    result["traits"] = data["traits"]
    result["skill"] = data["skill"]
    result["dodge_chance"] = 0
    result["damage_reduce"] = 0
    result["damage_increase"] = 0
    result["heist"] = 550
    result["critical_strike_chance"] = 25
    result["critical_strike_damage"] = 150

    return result


class Battle:
    def __init__(self):
        self.env = simpy.Environment()
        self.field = Field(self.env)
        self.champion: Dict[Team, List[Champion]] = {}
        self.trait: Dict[Team, Dict[Trait]] = {}
        self.action = ChampionAction(self.field)
        self.state_manager = StateManager(self.env)
        self.log = []
        make_battle_logger(self.env, self.log)

    def create_team(self, team_id=None) -> Team:
        t = Team(team_id)
        self.champion[t] = []
        self.trait[t] = {}

        return t

    def create_champion(self, team: Team, champ_id, level):
        champ_data = preprocess_champ_data(CHAMPION_DATA[champ_id], level)
        c = Champion(champ_data, team)
        self.champion[team].append(c)
        for t in champ_data["traits"]:
            if t not in self.trait[team]:
                if t not in TRAIT.keys():
                    continue
                self.trait[team][t] = TRAIT[t](self.field, self.state_manager)
            self.trait[team][t].add_active_key(c)

        return c

    def batch_champion(self, champion: Champion, loc: list[int]):
        self.field.assign(champion, loc)

    def get_current(self):
        result = {}
        for team in self.champion.keys():
            result[str(team)] = {}
            result[str(team)]['champions'] = {}
            for c in self.champion[team]:
                pos = self.field.get_location(c).id
                result[str(team)]['champions'][pos] = dict(c)
            result[str(team)]['trait'] = team.trait
        return result

    def init(self):
        for team in self.champion.keys():
            for t in self.trait[team].values():
                t.activate(self.champion[team])
                team.trait[t.type.value] = t.get_active_count()
        print(self.get_current())

    def start(self):
        self.init()
        champions = []
        for c in self.champion.values():
            champions.extend(c)
        for c in champions:
            c.cause_event(EventType.BATTLE_START)
            self.env.process(self.action.action(c))
        self.env.run(until=15)
