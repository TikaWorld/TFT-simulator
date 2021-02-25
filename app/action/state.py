class StateAction:
    def __init__(self, env, field):
        self.env = env
        self.field = field

    def put_state(self, champion, state, time):
        self.env.process(self._put_state(champion, state, time))

    def _put_state(self, champion, state, time):
        champion.action.interrupt()
        champion.state.append(state)
        yield self.env.timeout(time)
        champion.state.remove(state)
