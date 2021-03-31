from typing import List, Union

import simpy

from battle.construct.enum import State, Stat, DamageType, EventType
from battle.construct import Damage, Champion, Field
from battle.action import search
from functools import wraps
import random

from battle.exception.field import AlreadyExistChampion, StuckChampion
from battle.exception.skill import CancelSkillCasting
from battle.logger import LOGGER, make_battle_record
from battle.skill import SKILL


def get_generator(value):
    yield value


def set_break_status(break_status: List[State]):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            cls = args[0]
            champion: Champion = args[1]
            for s in break_status:
                if s in champion.state:
                    return get_generator(cls.env.timeout(0))

            result = func(*args, **kwargs)
            return result

        return decorator

    return wrapper


class ChampionAction:
    def __init__(self, field: Field):
        self.env: simpy.Environment = field.env
        self.field: Field = field

    def action(self, champion: Champion) -> simpy.events.ProcessGenerator:
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
                print(f'{champion}: action was interrupted')

    @set_break_status([State.STUN, State.AIRBORNE, State.BANISHES, State.DEATH])
    def select_action(self, champion: Champion) -> simpy.events.ProcessGenerator:
        champion.action = self.env.process(self.cast(champion))
        yield champion.action
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
    def attack(self, champion: Champion) -> simpy.events.ProcessGenerator:
        target: Champion = champion.target
        damage_type = DamageType.PHYSICAL
        attack_speed = champion.get_stat(Stat.ATTACK_SPEED)

        LOGGER[self.env].info(make_battle_record(self.env.now, "BASIC_ATTACK", dict(champion),
                                                 target=dict(target), attack_speed=attack_speed))
        yield self.env.timeout(1 / attack_speed)
        if target.is_dead():
            return
        print(f'{champion}: Attack {target} with speed {attack_speed:.2f} at {self.env.now:f}')
        champion.generate_mana(10)

        damage = Damage(champion, champion.get_stat(Stat.ATTACK), damage_type)
        damage.set_critical(champion.get_stat(Stat.CRITICAL_DAMAGE) if champion.is_critical() else None)
        damage.set_miss(target.is_dodge())

        dmg: Union[int, float] = target.get_damage(damage)
        champion.cause_event(EventType.BASIC_ATTACK, damage=dmg, champion=champion, targets=[target])

    @set_break_status([State.STUN, State.AIRBORNE, State.BANISHES, State.ROOT, State.DEATH])
    def move(self, champion: Champion) -> simpy.events.ProcessGenerator:
        yield self.env.timeout(0)
        current_cell = self.field.get_location(champion)
        try:
            path: search.Path = search.get_path(current_cell, champion.target)
        except StuckChampion:
            return
        heist = champion.get_stat(Stat.HEIST)
        LOGGER[self.env].info(make_battle_record(self.env.now, "MOVE", dict(champion),
                                                 start_cell=current_cell.id, target_cell=path[0].id, heist=heist))

        yield self.env.timeout(180 / heist)
        try:
            self.field.transfer(champion, path[0])
            LOGGER[self.env].info(make_battle_record(self.env.now, "ARRIVED", dict(champion),
                                                     start_cell=current_cell.id, target_cell=path[0].id, heist=heist))
            print(f'{champion}: Move to {path[0]} at {self.env.now:f}')
        except AlreadyExistChampion:
            LOGGER[self.env].info(make_battle_record(self.env.now, "MOVE_CANCELED", dict(champion),
                                                     start_cell=current_cell.id, target_cell=path[0].id, heist=heist))
            print(f'{champion}: Move action is canceled by already arrived champion at {self.env.now:f}')

    def search(self, champion: Champion) -> simpy.events.ProcessGenerator:
        distance, result = search.find_proximate(self.field.get_location(champion))
        if result:
            champion.target = random.choice(result).champion
            yield self.env.timeout(0)
        else:
            yield self.env.timeout(0.01)

    def death(self, champion: Champion) -> simpy.events.ProcessGenerator:
        if 'reborn' in champion.buff.keys():
            print(champion.buff)
            return
        LOGGER[self.env].info(make_battle_record(self.env.now, "DEATH", dict(champion)))
        print(f'{champion}: Champion is dead at {self.env.now:f}')
        self.field.release(champion)
        yield self.env.timeout(0)

    def cast(self, champion: Champion) -> simpy.events.ProcessGenerator:
        if champion.skill not in SKILL.keys():
            champion.mp = 0
            return
        skill = SKILL[champion.skill]
        if not skill or not skill.chk_condition(champion):
            yield self.env.timeout(0)
            return
        print(f'{champion}: Champion is cast at {self.env.now:f}')
        try:
            champion.action = self.field.env.process(skill(self.field).cast(champion))
            yield champion.action
        except CancelSkillCasting:
            yield self.env.timeout(0)
            return
        champion.mp = 0
