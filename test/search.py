import simpy
from app.construct import field, champion


def test_champion_search():
    from app.action import search

    f = field.Field()
    env = simpy.Environment()
    a = champion.Champion("a")
    b = champion.Champion("b")
    c = champion.Champion("c")
    d = champion.Champion("d")
    block_1 = champion.Champion("block1")
    block_2 = champion.Champion("block2")
    block_3 = champion.Champion("block3")

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
