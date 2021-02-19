class Cell:
    def __init__(self, i):
        self.champion=None
        self.connect=[]
        self.id= i
    
    def __repr__(self):
        return "%d: %s " %(self.id, self.champion)
        

WIDTH = 7
HEIGHT = 8
MAP = [[Cell(j+1+((i+1)*10)) for j in range(WIDTH)] for i in range(HEIGHT)]

for i in range(HEIGHT):
    for j in range(WIDTH-1):
        MAP[i][j].connect.append(MAP[i][j+1])
        MAP[i][j+1].connect.append(MAP[i][j])
    
for i in range(HEIGHT-1):
    for j in range(WIDTH):
        MAP[i][j].connect.append(MAP[i+1][j])
        MAP[i+1][j].connect.append(MAP[i][j])
    chk = (i+1)%2
    chk2 = i%2
    for j in range(WIDTH-chk2-1, 1+chk, -1):
        MAP[i][j].connect.append(MAP[i+1][j-1])
        MAP[i+1][j-1].connect.append(MAP[i][j])
