import copy

from app.game import Game

champ_data = {
    "name": "Dummy",
    "id": "TFT4_Yasuo",
    "trait": ["Duelist", "Divine", "Exile"],
    "skill": "javelin_toss",
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
    "damage_reduce": 0
}
champ_data2 = copy.copy(champ_data)
champ_data2["id"] = "TFT4_Yasuo2"

game = Game()

team_1 = game.create_team()
team_2 = game.create_team()
a = game.create_champion(team_1, champ_data)
b = game.create_champion(team_2, champ_data)
c = game.create_champion(team_2, champ_data2)
a.name = "a"
b.name = "b"
c.name = "c"


game.batch_champion(a, [0, 0])
game.batch_champion(b, [6, 6])
game.batch_champion(c, [1, 1])

game.start()
