class SkillManager:
    def __init__(self, field):
        self.field = field

    def casting(self, champion, skill):
        s = skill(self.field)
        self.field.env.process(s.cast(champion))
