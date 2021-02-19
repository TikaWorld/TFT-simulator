class Cell:
    def __init__(self, i):
        self.champion=None
        self.connect=[]
        self.id= i
    
    def __repr__(self):
        return "%d: %s " %(self.id, [n.id for n in self.connect])
        

WIDTH = 7
HEIGHT = 8
i=0
FIELD = [[Cell(j+((i)*7)) for j in range(WIDTH)] for i in range(HEIGHT)]

for i in range(HEIGHT):
    for j in range(WIDTH-1):
        FIELD[i][j].connect.append(FIELD[i][j+1])
        FIELD[i][j+1].connect.append(FIELD[i][j])
    
for i in range(HEIGHT-1):
    chk = (i+1)%2
    chk2 = i%2
    if chk2:
        FIELD[i][0].connect.append(FIELD[i+1][0])
        FIELD[i+1][0].connect.append(FIELD[i][0])
    for j in range(WIDTH-1, 0, -1):
        FIELD[i][j].connect.append(FIELD[i+1][j-chk])
        FIELD[i+1][j-chk].connect.append(FIELD[i][j])
    for j in range(WIDTH-chk2):
        FIELD[i][j].connect.append(FIELD[i+1][j+chk2])
        FIELD[i+1][j+chk2].connect.append(FIELD[i][j])
