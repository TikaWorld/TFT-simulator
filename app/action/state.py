from app.construct.state import State


class StateManager:
    def __init__(self, env, field):
        self.env = env
        self.field = field

    def put_state(self, champion, state, time):
        interrupt = False
        if state == State.STUN:
            interrupt = True
        self.env.process(self._put_state(champion, state, time, interrupt))

    def _put_state(self, champion, state, time, interrupt):
        if interrupt and champion.action:
            champion.action.interrupt()
        champion.state.append(state)
        yield self.env.timeout(time)
        try:
            champion.state.remove(state)
        except ValueError:
            print("<%s> State is already removed" % state)
