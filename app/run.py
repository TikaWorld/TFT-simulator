from action.champion import ChampionAction
import field, champion
import simpy

env = simpy.Environment()
f = field.Field()
action = ChampionAction(env, f)
a = champion.Champion("a")
b = champion.Champion("b") 
b.heist = 560

f.assign(a,[0,0])
f.assign(b,[5,5])

a.action = action.action
b.action = action.action
env.process(a.action(a))
env.process(b.action(b))

env.run(until=5)
