import simpy
from action.champion import ChampionAction
from action.state import StateManager
from construct.state import State
from app.construct import field

champ_data = {
    "name": "Dummy",
    "max_hp": 100,
    "max_mp": 100,
    "mp": 0,
    "heist": 550,
    "attack_damage": 100,
    "spell_power": 100,
    "critical_strike_chance": 25,
    "critical_strike_damage": 150,
    "range": 1,
    "armor": 100,
    "magic_resistance": 100,
    "attack_speed": 1,
    "dodge_chance": 0
}

env = simpy.Environment()
f = field.Field()
f_action = StateManager(env, f)
c_action = ChampionAction(env, f)
team_1 = f.get_team(f.create_team())
team_2 = f.get_team(f.create_team())
a = team_1.create_champion(champ_data)
b = team_2.create_champion(champ_data)
a.name = "a"
b.name = "b"

f.assign(a, [0, 0])
f.assign(b, [1, 0])
f_action.put_state(a, State.STUN, 1)
env.process(c_action.action(a))
env.process(c_action.action(b))

env.run(until=5)
