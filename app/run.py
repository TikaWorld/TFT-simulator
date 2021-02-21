from action.champion import Champion
from app import field
import simpy

env = simpy.Environment()
f = field.create_field()
a = Champion(env,f)
b = Champion(env,f)
f[0][0].champion = a
f[7][6].champion = b
a.pos = [0,0]
b.pos = [7,6]
env.process(a.search())
env.process(b.search())
b.attack_speed=2
env.process(a.action())
env.process(b.action())

env.run(until=5)
