import simpy
from app.champion.state import State
from app.action import search
from functools import wraps


def set_break_status(break_status):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            action_cls = args[0]
            champion = args[1]
            for s in break_status:
                if s in champion.state:
                    return action_cls.env.timeout(0.01)
            result = func(*args, **kwargs)
            return result

        return decorator

    return wrapper


class ChampionAction:
    def __init__(self, env, field):
        self.env = env
        self.field = field

    def action(self, champion):
        while True:
            while State.STUN in champion.state:
                yield self.env.timeout(0.01)
            if champion.target:
                distance = search.get_distance(self.field.get_location(champion), champion.target)
                if distance is None:
                    champion.target = None
                elif distance <= champion.range:
                    champion.action = self.env.process(self.attack(champion))
                    yield champion.action
                else:
                    yield self.env.process(self.search(champion))
                    champion.action = self.env.process(self.move(champion))
                    yield champion.action
            else:
                champion.action = self.env.process(self.search(champion))
                yield champion.action

    @set_break_status([State.DISARM, State.STUN, State.AIRBORNE, State.BANISHES])
    def attack(self, champion):
        try:
            yield self.env.timeout(champion.attack_speed)
            print("%s: Attack %s at %f" % (champion, champion.target, self.env.now))
            yield self.env.process(self.resist(champion.target, champion.attack_damage))
        except simpy.Interrupt:
            print('%s: Was interrupted.' % champion)

    def resist(self, champion, attack_damage, magic=False):
        resist_value = champion.armor if not magic else champion.magic_resistance
        damage_multiplier = 100 / (100 + resist_value)
        reduced_damage = attack_damage * damage_multiplier
        champion.hp -= reduced_damage
        print("%s: Get Damage %d at %f" % (champion, reduced_damage, self.env.now))
        yield self.env.timeout(0)

    @set_break_status([State.STUN, State.AIRBORNE, State.BANISHES, State.ROOT])
    def move(self, champion):
        if State.ROOT in champion.state:
            return self.env.timeout(0.01)
        path = search.get_path(self.field.get_location(champion), champion.target)
        if not path:
            raise Exception
        yield self.env.timeout(250 / champion.heist)
        try:
            self.field.transfer(champion, path[0])
            print("%s: Move to %s at %f" % (champion, path[0], self.env.now))
        except Exception:  # Need Define AlreadyArrived Error:
            print("%s: Move action is canceled by already arrived champion at %f" % (champion, self.env.now))

    def search(self, champion):
        distance, result = search.find_proximate(self.field.get_location(champion))
        if result:
            champion.target = result[0].champion
            yield self.env.timeout(0)
        else:
            yield self.env.timeout(0.01)
