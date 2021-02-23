class Champion(object):
    def __init__(self, name="Dummy"):
        self.name=name
        self.max_hp=100
        self.max_mp=0
        self.hp=self.max_hp
        self.mp=0
        self.heist=550
        self.attack_damage=10
        self.armor=40
        self.spell_power=100
        self.magic_resistance=40
        self.critical=25
        self.attack_speed=1
        self.range=1
        self.action=None
        self.target=None
        self.pos=None
    
    def __repr__(self):
        return "%s" %(self.name)
