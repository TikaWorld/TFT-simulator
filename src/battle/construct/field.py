from typing import List, Dict, TYPE_CHECKING, Union

from ..exception.field import AlreadyExistChampion, NotExistChampion

if TYPE_CHECKING:
    from . import Champion


def pos_convert(pos, pivot_pos):
    result = [pos[0], pos[1]+0.5]
    if int(pivot_pos[0]) % 2:
        if not int(pos[0]) % 2:
            result = [result[0], result[1] + 0.5]
    else:
        if int(pos[0]) % 2:
            result = [result[0], result[1] - 0.5]

    return result


def pivot_convert(pos):
    result = pos
    if int(pos[0]) % 2:
        result = [pos[0], pos[1] + 0.5]

    return result


class Cell:
    def __init__(self, i, pos):
        self.champion: Union[Champion, None] = None
        self.connect: List[Cell] = []
        self.id = i
        self.pos = pos

    def __repr__(self):
        return "%d: %s " % (self.id, self.champion)


class Field:
    def __init__(self, env, width=7, height=8):
        self.env = env
        self.width = width
        self.height = height
        self.cell: List[List[Cell]] = \
            [[Cell(j + (i * self.width), [i, j]) for j in range(self.width)] for i in range(self.height)]
        self.champion_location: Dict[Champion, Cell] = {}

        for i in range(self.height):
            for j in range(width - 1):
                self.cell[i][j].connect.append(self.cell[i][j + 1])
                self.cell[i][j + 1].connect.append(self.cell[i][j])

        for i in range(self.height - 1):
            chk = (i + 1) % 2
            chk2 = i % 2
            if chk2:
                self.cell[i][0].connect.append(self.cell[i + 1][0])
                self.cell[i + 1][0].connect.append(self.cell[i][0])
            for j in range(width - 1, 0, -1):
                self.cell[i][j].connect.append(self.cell[i + 1][j - chk])
                self.cell[i + 1][j - chk].connect.append(self.cell[i][j])
            for j in range(width - chk2):
                self.cell[i][j].connect.append(self.cell[i + 1][j + chk2])
                self.cell[i + 1][j + chk2].connect.append(self.cell[i][j])

    def assign(self, champ: "Champion", loc: list[int]):
        if self.cell[loc[0]][loc[1]].champion is not None:
            raise AlreadyExistChampion
        self.cell[loc[0]][loc[1]].champion = champ
        self.champion_location[champ] = self.cell[loc[0]][loc[1]]

    def transfer(self, champ: "Champion", loc_cell: Cell):
        if loc_cell.champion is not None:
            raise AlreadyExistChampion
        if champ not in self.champion_location:
            raise NotExistChampion
        if self.champion_location[champ].champion is not champ:
            raise NotExistChampion
        self.champion_location[champ].champion = None
        loc_cell.champion = champ
        self.champion_location[champ] = loc_cell

    def release(self, champ: "Champion"):
        if champ not in self.champion_location:
            raise NotExistChampion
        if self.champion_location[champ].champion is not champ:
            raise NotExistChampion
        self.champion_location[champ].champion = None
        del self.champion_location[champ]

    def get_location(self, champ: "Champion") -> Cell:
        if champ not in self.champion_location:
            raise NotExistChampion
        if self.champion_location[champ].champion is not champ:
            raise NotExistChampion

        return self.champion_location[champ]

    def get_cell(self, pos: List[int]) -> Union[Cell, None]:
        if pos[0] < 0 or pos[1] < 0:
            return None
        if pos[0] >= self.height or pos[1] >= self.width:
            return None
        return self.cell[pos[0]][pos[1]]

    def __repr__(self):
        result = ""
        for line in self.cell:
            result += str(line) + "\n"
        return result
