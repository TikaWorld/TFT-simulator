import simpy
from action.champion import ChampionAction
from action.state import StateAction
import champion
import field

env = simpy.Environment()
f = field.Field()
f_action = StateAction(env, f)
c_action = ChampionAction(env, f)
a = champion.Champion("a")
b = champion.Champion("b")

f.assign(a, [0, 0])
f.assign(b, [1, 0])

env.process(c_action.action(a))
env.process(c_action.action(b))

env.run(until=5)
