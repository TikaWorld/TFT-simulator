from typing import Union

from app.construct.enum.state import State
from app.construct import Field, Champion

import simpy


class StateManager:
    def __init__(self, env: simpy.Environment, field: Field):
        self.env: simpy.Environment = env
        self.field: Field = field

    def put_state(self, champion: Champion, state: State, time: Union[int, float]):
        interrupt = False
        if state == State.STUN:
            interrupt = True
        self.env.process(self._put_state(champion, state, time, interrupt))

    def _put_state(self, champion: Champion, state: State,
                   time: Union[int, float], interrupt: bool) -> simpy.events.ProcessGenerator:
        if interrupt and champion.action:
            champion.action.interrupt()
        champion.state.append(state)
        yield self.env.timeout(time)
        try:
            champion.state.remove(state)
        except ValueError:
            print("<%s> State is already removed" % state)
