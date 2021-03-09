from app.game import Game

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

game = Game()

team_1 = game.create_team()
team_2 = game.create_team()
a = game.create_champion(team_1, champ_data)
b = game.create_champion(team_2, champ_data)
a.name = "a"
b.name = "b"

game.batch_champion(a, [0, 0])
game.batch_champion(b, [5, 0])
game.start()
