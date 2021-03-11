from app.construct import Field, Champion, Team
from app.skill.javelin_toss import JavelinToss
from app.skill.skill import Projectile

champ_data = {
    "name": "Dummy",
    "trait": ["Duelist"],
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
    "dodge_chance": 0
}


def test_projectile():
    field = Field()
    team_1 = Team()
    team_2 = Team()
    a = Champion(champ_data, team_1)
    b = Champion(champ_data, team_2)
    c = Champion(champ_data, team_2)

    a.name = "a"
    b.name = "b"
    c.name = "c"

    field.assign(a, [0, 0])
    field.assign(b, [5, 5])
    field.assign(c, [1, 1])

    a.target = b

    skill = JavelinToss(field)
    skill.cast(a)


test_projectile()
