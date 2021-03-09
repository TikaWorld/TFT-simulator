from app.construct import field, champion, team


def test_champion_search():
    from app.action import search

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

    f = field.Field()
    t = team.Team()
    a = champion.Champion(champ_data, t)
    b = champion.Champion(champ_data, t)
    c = champion.Champion(champ_data, t)
    d = champion.Champion(champ_data, t)
    block_1 = champion.Champion(champ_data, t)
    block_2 = champion.Champion(champ_data, t)
    block_3 = champion.Champion(champ_data, t)

    f.cell[0][0].champion = a
    f.cell[7][5].champion = block_1
    f.cell[6][6].champion = block_2
    f.cell[5][5].champion = block_3

    f.cell[7][6].champion = b
    f.cell[3][3].champion = c
    f.cell[2][4].champion = d
    distance, result = search.find_proximate(f.cell[0][0])
    print(search.get_distance(f.cell[0][0], b))
    print(distance, result)


test_champion_search()
