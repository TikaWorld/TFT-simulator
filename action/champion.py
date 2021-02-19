import simpy

class Champion:
    def __init__(self, env):
        self.env=env
        self.hp=100
        self.mp=0
        self.heist=550
        self.attack_damage=10
        self.critical=25
        self.attack_speed=1
        self.action=self.attack
        self.target=None

    def attack(self):
        while True:
            try:
                yield self.env.process(self.target.guard(self.attack_damage))
            except simpy.Interrupt:
                print('Was interrupted.')
            print("Attack %f" % self.env.now)
            yield self.env.timeout(self.attack_speed)

    def guard(self, attack_damage):
        print("Get Damage %d at %f" % (attack_damage,self.env.now))
        yield self.env.timeout(0)