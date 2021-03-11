from .skill import Skill, Projectile


class JavelinToss(Skill):
    def __init__(self, field):
        super().__init__()
        self.field = field

    def cast(self, champion):
        second = 0.01
        current_pos = self.field.champion_location[champion].pos
        target_pos = self.field.champion_location[champion.target].pos
        javelin = Javelin(current_pos, target_pos)
        javelin.set_ignore(champion)
        while javelin.alive:
            yield self.field.env.timeout(second)
            for pos in javelin.tick(second):
                target = self.field.cell[pos[0]][pos[1]].champion
                if target and target not in javelin.ignore:
                    javelin.collide(target)
                    print("%s: Attack %s with javelin toss at %f" % (champion, target, self.field.env.now))
                    break


class Javelin(Projectile):
    def __init__(self, pos, slope):
        super().__init__(pos, slope, heist=1300)
        self.ignore = []

    def set_ignore(self, champion):
        self.ignore.append(champion)

    def collide(self, target):
        self.set_ignore(target)
        print(target)
        self.alive = False
