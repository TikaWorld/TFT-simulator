import simpy
from app import field, champion

def test_champion_search():
    from app.action import search

    f = field.Field()
    env = simpy.Environment()
    a = champion.Champion("a")
    b = champion.Champion("b")
    c = champion.Champion("c")
    d = champion.Champion("d")
    f.cell[0][0].champion = a
    f.cell[7][6].champion = b
    f.cell[3][3].champion = c
    f.cell[2][4].champion = d
    distance, result = search.find_proximate(f.cell[0][0])
    print(distance, result)

test_champion_search()