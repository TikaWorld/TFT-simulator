import battle


game = battle.Battle()

team_1 = game.create_team()
team_2 = game.create_team()
a = game.create_champion(team_1, "TFT4_Yasuo", 1)
b = game.create_champion(team_2, "TFT4_Yasuo", 1)
c = game.create_champion(team_2, "TFT4_Yasuo", 1)
a.name = "a"
b.name = "b"
c.name = "c"

game.batch_champion(a, [1, 1])
game.batch_champion(b, [1, 2])
game.batch_champion(c, [2, 2])

game.start()
