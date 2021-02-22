from action.champion import ChampionAction
from app import field, champion
import simpy

env = simpy.Environment()
f = field.Field()
action = ChampionAction(env, f)
a = champion.Champion("a")
b = champion.Champion("b")

f.assign(a,[0,0])
f.assign(b,[7,6])

a.action = action.search
b.action = action.search

env.process(a.action(a))
env.process(b.action(b))

b.attack_speed=2
a.action = action.attack
b.action = action.attack
env.process(a.action(a))
env.process(b.action(b))

env.run(until=5)
