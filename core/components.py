from string import ascii_uppercase
import random


class Cell:
    def __init__(self, row: int, col: int, cleared: bool = False, bomb: bool = False, flagged: bool = False):
        self._cleared = cleared
        self.bomb = bomb
        self._flagged = flagged
        self._counter = 0
        self.row = row
        self.col = col

    @property
    def cleared(self) -> bool:
        return self._cleared

    def clear(self):
        if self._flagged:
            raise RuntimeError(f'Cell {repr(self)} is flagged! Cannot be cleared.')
        elif self._cleared:
            raise RuntimeError(f'Cell {repr(self)} is clear! Cannot be cleared.')
        else:
            self._cleared = True

    @property
    def counter(self) -> int:
        return self._counter

    @counter.setter
    def counter(self, val):
        if val < 0 or 8 < val:
            raise ValueError(f'Cell {repr(self)} Counter out of range: [{val}]')
        self._counter = val

    @property
    def flagged(self) -> bool:
        return self._flagged

    def flag(self):
        if self._cleared:
            raise RuntimeError(f'Cell {repr(self)} is cleared and cannot be flagged.')
        self._flagged = True

    def unflag(self):
        if not self._flagged:
            raise RuntimeError(f'Cell {repr(self)} is not flagged.')
        self._flagged = False

    def __str__(self):
        if self._flagged:
            return 'F'
        elif not self._cleared:
            return '-'
        elif self.bomb:
            return 'B'
        elif self._counter > 0:
            return str(self.counter)
        else:
            return '.'

    def __repr__(self):
        flagged = 'F' if self._flagged else '-'
        bomb = 'B' if self.bomb else '-'
        counter = str(self.counter)
        cleared = 'C' if self._cleared else '-'
        return f"[{ascii_uppercase[self.row]}:{self.col}]{str(self)}|{bomb}{counter}{flagged}{cleared}]"


class Grid:
    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        self._bombs = 0
        self.cells = [[Cell(row, col) for col in range(cols)] for row in range(rows)]

    def cell_coord(self, pos: int) -> tuple:
        row = pos // self._cols
        col = pos % self._cols
        if row >= self._rows:
            raise ValueError(f'Position is out of range: ({pos})')
        return row, col

    def cell_neighbours(self, row: int, col: int):
        for row_of in (-1, 0, 1):
            for col_of in (-1, 0, 1):
                neighbour_row = row + row_of
                neighbour_col = col + col_of
                if not (neighbour_col == col and neighbour_row == row):
                    if 0 <= neighbour_row < self._rows and 0 <= neighbour_col < self._cols:
                        yield self.cells[neighbour_row][neighbour_col]

    def place_bombs(self, bombs: int):
        if self._bombs > 0:
            raise RuntimeError(f'Bombs are already down! ({self._bombs})')
        bomb_positions = random.sample(range(self._rows * self._cols), bombs)
        for pos in bomb_positions:
            row, col = self.cell_coord(pos)
            cell = self.cells[row][col]
            cell.bomb = True
            for neighbour_cell in self.cell_neighbours(row, col):
                neighbour_cell.counter += 1
        self._bombs = bombs

    def reveal_cell(self, row: int, col: int) -> bool:
        try:
            cell = self.cells[row][col]
        except IndexError:
            raise ValueError(f'Coordinates out of range.')
        if cell.bomb:
            self.reveal_bombs()
            return False
        self._clear_field(row, col)
        return True

    def reveal_bombs(self):
        for row in range(self._rows):
            for col in range(self._cols):
                cell = self.cells[row][col]
                if cell.bomb:
                    cell.clear()

    def _clear_field(self, row: int, col: int):
        to_clear = set((self.cells[row][col],))
        while len(to_clear) > 0:
            cell = to_clear.pop()
            cell.clear()
            if cell.counter == 0:
                for neighbour in self.cell_neighbours(cell.row, cell.col):
                    if not neighbour.cleared:
                        to_clear.add(neighbour)

    def print_grid(self, debug=False):
        sep = ' ' if not debug else ' ' * 12
        p_func = str if not debug else repr
        print(f"  {sep.join(map(str, range(1, self._cols + 1)))}")
        for row_label, row in zip(ascii_uppercase, self.cells):
            print(f"{row_label} {' '.join(map(p_func, row))}")

