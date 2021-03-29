
class Team:
    def __init__(self, team_id=None):
        self.id = str(id(self))
        if team_id is not None:
            self.id = team_id
        self.trait = {}

    def __repr__(self):
        return self.id

