from action.champion import Champion
import simpy

env = simpy.Environment()
a = Champion(env)
b = Champion(env)
a.target=b
b.target=a
b.attack_speed=2
env.process(a.action())
env.process(b.action())

env.run(until=5)