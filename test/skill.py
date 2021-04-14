import simpy

from battle.construct import Field, Champion, Team
from battle.skill.javelin_toss import JavelinToss

champ_data = {
    "name": "Dummy",
    "championId": "Dummy",
    "level": 1,
    "traits": ["Duelist"],
    "uuid": "test",
    "skill": "",
    "max_hp": 1000,
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
    "dodge_chance": 0,
    "damage_reduce": 0,
    "damage_increase": 0
}


def test_projectile():
    env = simpy.Environment()
    field = Field(env)
    team_1 = Team()
    team_2 = Team()
    a = Champion(champ_data, team_1)
    b = Champion(champ_data, team_2)
    c = Champion(champ_data, team_2)

    a.name = "a"
    b.name = "b"
    c.name = "c"

    field.assign(a, [0, 1])
    field.assign(b, [7, 0])

    a.target = b

    skill = JavelinToss(field)
    field.env.process(skill.cast(a))
    field.env.run(until=10)


test_projectile()
