class Cell:
    def __init__(self, i):
        self.champion=None
        self.connect=[]
        self.id= i
    
    def __repr__(self):
        return "%d: %s " %(self.id, self.champion)
        
def create_field(width=7, heigth=8):
    i=0
    field = [[Cell(j+((i)*7)) for j in range(width)] for i in range(heigth)]

    for i in range(heigth):
        for j in range(width-1):
            field[i][j].connect.append(field[i][j+1])
            field[i][j+1].connect.append(field[i][j])
        
    for i in range(heigth-1):
        chk = (i+1)%2
        chk2 = i%2
        if chk2:
            field[i][0].connect.append(field[i+1][0])
            field[i+1][0].connect.append(field[i][0])
        for j in range(width-1, 0, -1):
            field[i][j].connect.append(field[i+1][j-chk])
            field[i+1][j-chk].connect.append(field[i][j])
        for j in range(width-chk2):
            field[i][j].connect.append(field[i+1][j+chk2])
            field[i+1][j+chk2].connect.append(field[i][j])
    
    return field

