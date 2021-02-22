import simpy
from .search import find_proximate

class ChampionAction:
    def __init__(self, env, field):
        self.env=env
        self.field=field

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
    
    def move(self):
        NotImplemented
    
    def search(self, champion):
        distance, result = find_proximate(self.field.get_location(champion))
        if result:
            champion.target = result[0].champion
        yield self.env.timeout(0)
