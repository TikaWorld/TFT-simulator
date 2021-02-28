import simpy
from action.champion import ChampionAction
from action.state import StateManager
from champion.champion import Champion
from champion.state import State
import field

env = simpy.Environment()
f = field.Field()
f_action = StateManager(env, f)
c_action = ChampionAction(env, f)
a = Champion("a", "a")
b = Champion("b", "b")

f.assign(a, [0, 0])
f.assign(b, [1, 0])
f_action.put_state(a, State.STUN, 1)
env.process(c_action.action(a))
env.process(c_action.action(b))

env.run(until=5)
