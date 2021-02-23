import simpy
from . import search

class ChampionAction:
    def __init__(self, env, field):
        self.env=env
        self.field=field

    def action(self, champion):
        while True:
            if champion.target:
                distance = search.get_distance(self.field.get_location(champion), champion.target)
                if distance is None:
                    champion.target = None
                elif distance <= champion.range:
                    yield self.env.process(self.attack(champion))
                else:
                    yield self.env.process(self.search(champion))
                    yield self.env.process(self.move(champion))
            else:
                yield self.env.process(self.search(champion))

    def attack(self, champion):
        try:
            yield self.env.timeout(champion.attack_speed)
            print("%s: Attack %s at %f" % (champion, champion.target, self.env.now))
            yield self.env.process(self.guard(champion.target, champion.attack_damage))
        except simpy.Interrupt:
            print('Was interrupted.')
        
    def guard(self, champion, attack_damage):
        print("%s: Get Damage %d at %f" % (champion, attack_damage, self.env.now))
        yield self.env.timeout(0)
    
    def move(self, champion):
        path = search.get_path(self.field.get_location(champion), champion.target)
        if not path:
            raise Exception
        yield self.env.timeout(250/champion.heist)
        try:
            self.field.transfer(champion, path[0])
            print("%s: Move to %s at %f" %(champion, path[0], self.env.now))
        except Exception: #Need Define AlreadyArrived Error:
            print("%s: Move action is canceled by already arrived champion at %f" %(champion, self.env.now))
        


    def search(self, champion):
        distance, result = search.find_proximate(self.field.get_location(champion))
        if result:
            champion.target = result[0].champion
            yield self.env.timeout(0)
        else:
            yield self.env.timeout(0.01)
