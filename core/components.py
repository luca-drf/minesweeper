from __future__ import annotations
from string import ascii_uppercase
from itertools import product
import random
from typing import List


extended_ascii = ' ' + ascii_uppercase


class Cell:
    def __init__(self, row: int, col: int, cleared: bool = False, mine: bool = False, flagged: bool = False):
        self._cleared = cleared
        self.mine = mine
        self._flagged = flagged
        self._counter = 0
        self.row = row
        self.col = col

    @property
    def coords_str(self):
        return f'{ascii_uppercase[self.row]}:{self.col + 1}'

    @property
    def cleared(self) -> bool:
        return self._cleared

    def clear(self):
        if self._flagged:
            raise RuntimeError(f'Cell [{self.coords_str}] is flagged! Cannot be cleared.',
                               f'{repr(self)}')
        elif self._cleared:
            raise RuntimeError(f'Cell [{self.coords_str}] is clear! Cannot be cleared.',
                               f'{repr(self)}')
        else:
            self._cleared = True

    @property
    def counter(self) -> int:
        return self._counter

    @counter.setter
    def counter(self, val):
        if val < 0 or 8 < val:
            raise ValueError(f'Cell [{self.coords_str}] Counter out of range: [{val}]',
                             f'{repr(self)}')
        self._counter = val

    @property
    def flagged(self) -> bool:
        return self._flagged

    def flag(self):
        if self._cleared:
            raise RuntimeError(f'Cell [{self.coords_str}] is cleared and cannot be flagged.',
                               f'{repr(self)}')
        self._flagged = True

    def unflag(self):
        if not self._flagged:
            raise RuntimeError(f'Cell [{self.coords_str}] is not flagged.',
                               f'{repr(self)}')
        self._flagged = False

    def __str__(self):
        if self._flagged:
            return 'F'
        elif not self._cleared:
            return '-'
        elif self.mine:
            return 'M'
        elif self._counter > 0:
            return str(self.counter)
        else:
            return '.'

    def __repr__(self):
        flagged = 'F' if self._flagged else '-'
        mine = 'B' if self.mine else '-'
        counter = str(self.counter)
        cleared = 'C' if self._cleared else '-'
        return f"[{self.coords_str}]{str(self)}|{mine}{counter}{flagged}{cleared}]"


class Grid:
    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        self._mines = 0
        self._cleared_cells = 0
        self._cells = [[Cell(row, col) for col in range(cols)] for row in range(rows)]

    def __iter__(self):
        for row in self._cells:
            for cell in row:
                yield cell

    def __len__(self):
        return self._rows * self._cols

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def mines(self) -> int:
        return self._mines

    def is_clear(self) -> bool:
        return (self._mines + self._cleared_cells) == len(self)

    def cell_at(self, row: str, col: str) -> Cell:
        if not (row and col):
            raise ValueError(f'Invalid coordinates: [{row}:{col}]')
        try:
            row_i = label_to_i(row.upper()) - 1
            col_i = int(col) - 1
        except ValueError as e:
            raise ValueError(f'Invalid coordinates: [{row}:{col}]') from e
        if (0 <= row_i < self._rows) and (0 <= col_i < self._cols):
            try:
                return self._cells[row_i][col_i]
            except IndexError as e:
                raise IndexError(f'Invalid coordinates: [{row}:{col}]') from e
        else:
            raise IndexError(f'Invalid coordinates: [{row}:{col}]')

    def cell_at_pos(self, pos: int) -> Cell:
        row = pos // self._cols
        col = pos % self._cols
        if row >= self._rows:
            raise IndexError(f'Position is out of range: ({pos})')
        return self._cells[row][col]

    def place_mines(self, mines: int, positions: List[int] = None) -> Grid:
        if self._mines > 0:
            raise RuntimeError(f'Mines are already down! ({self._mines})')
        if positions:
            mine_positions = positions[0:mines]
        else:
            mine_positions = random.sample(range(len(self)), mines)
        for pos in mine_positions:
            cell = self.cell_at_pos(pos)
            cell.mine = True
            for neighbour_cell in self._cell_neighbours(cell.row, cell.col):
                neighbour_cell.counter += 1
        self._mines = mines
        return self

    def reveal_cell(self, row: str, col: str) -> bool:
        cell = self.cell_at(row, col)
        if cell.mine:
            self.reveal_mines()
            return False
        self._clear_field(cell.row, cell.col)
        return True

    def reveal_mines(self):
        for cell in self:
            if cell.mine:
                cell.clear()

    def flag_cell(self, row: str, col: str) -> Cell:
        cell = self.cell_at(row, col)
        cell.flag()
        return cell

    def unflag_cell(self, row: str, col: str) -> Cell:
        cell = self.cell_at(row, col)
        cell.unflag()
        return cell

    def to_string(self, debug: bool = False) -> str:
        elems = []
        col_width = 2 if not debug else 13
        col_func = lambda n: str(n).ljust(col_width, ' ')
        row_func = str if not debug else repr
        elems.append(f"   {' '.join(map(col_func, range(1, self._cols + 1)))}\n")
        rows = [f"{row_label} {'  '.join(map(row_func, row))}\n"
                for row_label, row in zip(map(''.join, product(extended_ascii, ascii_uppercase)), self._cells)]
        elems.extend(rows)
        return ''.join(elems)

    def _cell_neighbours(self, row: int, col: int):
        for row_of in (-1, 0, 1):
            for col_of in (-1, 0, 1):
                neighbour_row = row + row_of
                neighbour_col = col + col_of
                if not (neighbour_col == col and neighbour_row == row):
                    if 0 <= neighbour_row < self._rows and 0 <= neighbour_col < self._cols:
                        yield self._cells[neighbour_row][neighbour_col]

    def _clear_field(self, row: int, col: int):
        to_clear = set((self._cells[row][col],))
        while len(to_clear) > 0:
            cell = to_clear.pop()
            cell.clear()
            self._cleared_cells += 1
            if cell.counter == 0:
                for neighbour in self._cell_neighbours(cell.row, cell.col):
                    if not neighbour.cleared:
                        to_clear.add(neighbour)


def label_to_i(label: str) -> int:
    res = 0
    for c in label:
        res *= 26
        res += ord(c) - ord('A') + 1
    return res

