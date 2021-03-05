import simpy

from app.construct.enum.state import State
from app.construct.enum.event import Event
from app.construct.enum.stat import Stat
from app.construct.damage import Damage
from app.construct.enum.damage import DamageType
from app.action import search
from functools import wraps
import random


def set_break_status(break_status):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            champion = args[1]
            for s in break_status:
                if s in champion.state:
                    return

            result = func(*args, **kwargs)
            return result

        return decorator

    return wrapper


class ChampionAction:
    def __init__(self, env, field):
        self.env = env
        self.field = field

    def action(self, champion):
        yield self.env.timeout(0)
        while True:
            if State.DEATH in champion.state:
                champion.action = self.env.process(self.death(champion))
                yield champion.action
                if State.DEATH in champion.state:
                    return
            try:
                r = self.select_action(champion)
                yield self.env.process(r) if r else self.env.timeout(0.01)
            except simpy.Interrupt:
                print("%s: action was interrupted" % champion)

    @set_break_status([State.STUN, State.AIRBORNE, State.BANISHES, State.DEATH])
    def select_action(self, champion):
        if champion.target:
            distance = search.get_distance(self.field.get_location(champion), champion.target)
            if distance is None:
                champion.target = None
            elif distance <= champion.stat[Stat.RANGE]:
                champion.action = self.env.process(self.attack(champion))
                yield champion.action
            else:
                yield self.env.process(self.search(champion))
                champion.action = self.env.process(self.move(champion))
                yield champion.action
        else:
            champion.action = self.env.process(self.search(champion))
            yield champion.action

    @set_break_status([State.DISARM, State.STUN, State.AIRBORNE, State.BANISHES, State.DEATH])
    def attack(self, champion):
        target = champion.target
        damage_type = DamageType.PHYSICAL
        attack_speed = champion.get_stat(Stat.ATTACK_SPEED)
        yield self.env.timeout(1 / attack_speed)
        if target.is_dead():
            return
        print("%s: Attack %s with speed %.2f at %f" % (champion, target, attack_speed, self.env.now))
        champion.generate_mana(10)

        damage = Damage(champion.get_stat(Stat.ATTACK), damage_type)
        damage.set_critical(champion.get_stat(Stat.CRITICAL_DAMAGE) if champion.is_critical() else None)
        damage.set_miss(target.is_dodge())

        dmg = target.get_damage(damage)
        champion.cause_event(Event.BASIC_ATTACK, damage=dmg)

    @set_break_status([State.STUN, State.AIRBORNE, State.BANISHES, State.ROOT, State.DEATH])
    def move(self, champion):
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
            champion.target = random.choice(result).champion
            yield self.env.timeout(0)
        else:
            yield self.env.timeout(0.01)

    def death(self, champion):
        if "reborn" in champion.buff.keys():
            print(champion.buff)
            return
        print("%s: Champion is dead at %f" % (champion, self.env.now))
        self.field.release(champion)
        yield self.env.timeout(0)
