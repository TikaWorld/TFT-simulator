import simpy
from app import field

def test_champion_search():
    from app.action import search
    from app.action.champion import Champion

    f = field.create_field()
    env = simpy.Environment()
    a = Champion(env, f)
    b = Champion(env, f)
    c = Champion(env, f)
    d = Champion(env, f)
    f[0][0].champion = a
    f[7][6].champion = b
    f[3][3].champion = c
    f[2][4].champion = d
    distance, result = search.find_proximate([0,0], f)
    print(distance, result)

test_champion_search()