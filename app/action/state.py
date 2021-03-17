from typing import Union

from app.construct.enum import Stat, EventType
from app.construct.enum.state import State
from app.construct import Champion, Buff

import simpy


class StateManager:
    def __init__(self, env: simpy.Environment):
        self.env: simpy.Environment = env

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
            print(f'<{state}> State is already removed')

    def put_buff(self, champion: Champion, buff_type: Stat, buff: Buff, time=None):
        self.env.process(self._put_buff(champion, buff_type, buff, time))

    def _put_buff(self, champion: Champion, buff_type: Stat, buff: Buff,
                  time: Union[int, float, None]) -> simpy.events.ProcessGenerator:
        champion.buff[buff_type].append(buff)
        if time is None:
            yield self.env.timeout(0)
            return
        yield self.env.timeout(time)
        try:
            champion.buff[buff_type].remove(buff)
        except ValueError:
            print(f'<{buff}> Buff is already removed')

    def put_event(self, champion: Champion, e_type: EventType, e, time=None):
        self.env.process(self._put_event(champion, e_type, e, time))

    def _put_event(self, champion: Champion, e_type: EventType, e,
                   time: Union[int, float, None]) -> simpy.events.ProcessGenerator:
        champion.event[e_type].append(e)
        if time is None:
            yield self.env.timeout(0)
            return
        yield self.env.timeout(time)
        try:
            champion.event[e_type].remove(e)
        except ValueError:
            print(f'<{e}> Event is already removed')

    def put_barrier(self, champion: Champion, barrier, time=None):
        self.env.process(self._put_barrier(champion, barrier, time))

    def _put_barrier(self, champion: Champion, barrier, time: Union[int, float, None]) -> simpy.events.ProcessGenerator:
        champion.barrier.append(barrier)
        if time is None:
            yield self.env.timeout(0)
            return
        yield self.env.timeout(time)
        try:
            champion.barrier.remove(barrier)
        except ValueError:
            print(f'<{barrier}> Barrier is already removed')
