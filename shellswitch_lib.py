import random
import pygame

LEVELS = [(6, 4, 1), (6, 3, 2), (7, 5, 1), (7, 2, 3), (7, 4, 2), (8, 1, 4), (8, 3, 3), (8, 2, 4), (9, 4, 3), (10, 3, 4)]

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __str__(self):
        return self.__repr__()

    def get_tuple(self):
        return (self.x, self.y)


class ShellSwitchGameTile:
    def __init__(self, x, y, mult, size):
        self.pos = Coord(x, y)
        self.mult = mult
        self.sprite = None
        self.area = pygame.Rect(x, y, size, size)
        self.is_clicked = False

    def __str__(self):
        return str(self.mult)


class Grid:
    def __init__(self, default, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = rows * cols
        self.grid = [[default for i in range(cols)] for j in range(rows)]

    def __repr__(self):
        s = ""
        for row in self.grid:
            for cell in row:
                s += str(cell) + " "
            s.strip()
            s += '\n'
        return s

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        for row in self.grid:
            for cell in row:
                yield cell

    def set_cell(self, row, col, value):
        self.grid[row][col] = value

    def get_cell(self, row, col):
        return self.grid[row][col]

    def get_row(self, row):
        return self.grid[row]

    def get_col(self, col):
        return [row[col] for row in self.grid]


class ShellSwitchGameGrid(Grid):
    def __init__(self):
        super().__init__(None, 5, 5)
        self.tile_size = 44
        self.gap_x = 20
        self.gap_y = 20
        self.pos = Coord(138, 10)

    def gen_grid(self, level):
        pos = Coord(self.pos.x, self.pos.y)
        l_data = LEVELS[level]
        grid_data = [0]*l_data[0] + [2]*l_data[1] + [3]*l_data[2] + [1]*(self.cells - sum(l_data))
        random.shuffle(grid_data)

        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                tile = ShellSwitchGameTile(pos.x, pos.y, grid_data[i], self.tile_size)
                self.set_cell(row, col, tile)
                pos.x += self.tile_size + self.gap_x
                i += 1
            pos.y += self. tile_size + self.gap_y
            pos.x = self.pos.x

    def bombs_in_row(self, row):
        count = 0
        for tile in self.get_row(row):
            if tile.mult == 0:
                count += 1
        return count

    def bombs_in_col(self, col):
        count = 0
        for tile in self.get_col(col):
            if tile.mult == 0:
                count += 1
        return count

    def points_in_row(self, row):
        return sum(x.mult for x in self.get_row(row))

    def points_in_col(self, col):
        return sum(x.mult for x in self.get_col(col))

    def max_score(self):
        score = 1
        for row in self.grid:
            for cell in row:
                if cell.mult != 0:
                    score *= cell.mult
        return score


if __name__ == "__main__":
    x = ShellSwitchGameGrid()
    x.gen_grid(0)
    print(x)