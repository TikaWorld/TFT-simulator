class SkillManager:
    def __init__(self, field):
        self.field = field

    def casting(self, champion):
        return NotImplemented

    def cast_projectile(self, projectile, second=0.1):
        while projectile.alive:
            for pos in projectile.tick(second):
                projectile.collide()
            self.field.env.timeout(second)
