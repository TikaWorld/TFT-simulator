import simpy

class Cell:
    def __init__(self, i):
        self.champion=None
        self.connect=[]
        self.id=i
    
    def __repr__(self):
        return "%d: %s " %(self.id, self.champion)

class Field:
    def __init__(self, width=7, height=8):
        self.env = simpy.Environment()
        self.width=width
        self.height=height
        self.cell = [[Cell(j+((i)*7)) for j in range(self.width)] for i in range(self.height)]
        self.champion_location = {}

        for i in range(self.height):
            for j in range(width-1):
                self.cell[i][j].connect.append(self.cell[i][j+1])
                self.cell[i][j+1].connect.append(self.cell[i][j])
            
        for i in range(self.height-1):
            chk = (i+1)%2
            chk2 = i%2
            if chk2:
                self.cell[i][0].connect.append(self.cell[i+1][0])
                self.cell[i+1][0].connect.append(self.cell[i][0])
            for j in range(width-1, 0, -1):
                self.cell[i][j].connect.append(self.cell[i+1][j-chk])
                self.cell[i+1][j-chk].connect.append(self.cell[i][j])
            for j in range(width-chk2):
                self.cell[i][j].connect.append(self.cell[i+1][j+chk2])
                self.cell[i+1][j+chk2].connect.append(self.cell[i][j])
    
    def assign(self, champ, loc):
        if self.cell[loc[0]][loc[1]].champion is not None:
            raise Exception
        self.cell[loc[0]][loc[1]].champion = champ
        self.champion_location[champ] = self.cell[loc[0]][loc[1]]

    
    def release(self, champ):
        if not champ in self.champion_location:
            raise Exception
        if self.champion_location[champ].champion is not champ:
            raise Exception
        self.champion_location[champ].champion = None
        del self.champion_location[champ]

    def get_location(self, champ):
        if not champ in self.champion_location:
            raise Exception
        if self.champion_location[champ].champion is not champ:
            raise Exception
        
        return self.champion_location[champ]


    def __repr__(self):
        result = ""
        for line in self.cell:
            result+=str(line)+"\n"
        return result