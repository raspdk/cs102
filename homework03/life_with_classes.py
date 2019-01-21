import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_cell_list(self, clist: list) -> None:
        for Cell in self.clist:
            x = Cell.col * self.cell_size + 1
            y = Cell.row * self.cell_size + 1
            a = self.cell_size - 1
            b = self.cell_size - 1
            if Cell.is_alive():
                pygame.draw.rect(self.screen, pygame.Color('red'), (x, y, a, b))
            else:
                pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))
        pass

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        self.clist = CellList(self.cell_height, self.cell_width, True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            # Отрисовка списка клеток
            self.draw_cell_list(self.clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.clist = self.clist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.clist = []
        for i in range(nrows):
            if randomize:
                self.clist.append([Cell(i, j, random.randint(0, 1)) for j in range(ncols)])
            else:
                self.clist.append([Cell(i, j, 0) for j in range(ncols)])

    def get_neighbours(self, cell):
        neighbours = []
        x = cell.row
        y = cell.col
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i != x) or (j != y):
                    if (0 <= i <= self.nrows - 1) and (0 <= j <= self.ncols - 1):
                        neighbours.append(self.clist[i][j])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.clist)
        for cell in self:
            num = self.get_neighbours(cell)
            count_n = sum(i.is_alive() for i in num)
            if (cell.is_alive()) and (1 < count_n < 4):
                new_clist[cell.row][cell.col].state = True
            elif (not cell.is_alive()) and (count_n == 3):
                new_clist[cell.row][cell.col].state = True
            else:
                new_clist[cell.row][cell.col].state = False
        self.clist = new_clist
        return self

    def __iter__(self):
        self.i = 0
        self.j = 0
        return self

    def __next__(self):
        if self.i == self.nrows:
            raise StopIteration
        cell = self.clist[self.i][self.j]
        self.j += 1
        if self.j == self.ncols:
            self.i += 1
            self.j = 0
        return cell

    def __str__(self):
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.clist[i][j].state:
                    str += '1 '
                else:
                    str += '0 '
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename):
        new_grid = []
        with open(filename) as f:
            line = f.readline()
            row = 0
            while line:
                new_grid.append([])
                col = 0
                for pos in line:
                    if pos in '01':
                        new_grid[row].append(Cell(row, col, int(pos)))
                        col += 1
                line = f.readline()
                row += 1
        clist = cls(len(new_grid), len(new_grid[0]))
        clist.clist = new_grid
        return clist

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()