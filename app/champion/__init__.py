class Champion(object):
    def __init__(self, name="Dummy"):
        self.name = name
        self.hp=100
        self.mp=0
        self.max_hp=100
        self.max_mp=0
        self.heist=550
        self.attack_damage=10
        self.critical=25
        self.attack_speed=1
        self.action=None
        self.target=None
        self.pos=None
    
    def __repr__(self):
        return "%s" %(self.name)
