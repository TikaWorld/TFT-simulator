import simpy
from app import field

def test_champion_search():
    from app.action import search
    from app.action.champion import Champion

    env = simpy.Environment()
    a = Champion(env)
    b = Champion(env)
    field.FIELD[0][0].champion = a
    field.FIELD[3][3].champion = b
    for f in field.FIELD:
        print(f)
    search.find_proximate([0,0])

test_champion_search()