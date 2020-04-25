from core.components import Grid, Cell
import sys
import re
from typing import Callable


ACTION_RE = re.compile(r'^(?P<action>[FUR]) (?P<row>\w+):(?P<col>\d+)$', re.IGNORECASE)


def init_grid() -> Grid:
    print('Enter Grid dimension')
    grid = None
    while True:
        dim_raw = input('[S]mall, [M]edium, [L]arge, E[X]tra Large: ').strip()
        if dim_raw.upper() =='S':
            grid = Grid(9, 9).place_mines(10)
            break
        elif dim_raw.upper() == 'M':
            grid = Grid(16, 16).place_mines(32)
            break
        elif dim_raw.upper() == 'L':
            grid = Grid(25, 25).place_mines(77)
            break
        elif dim_raw.upper() == 'X':
            grid = Grid(32, 32).place_mines(126)
            break
        else:
            print('Please enter a valid choice.')
    return grid


def game_loop(grid: Grid) -> None:
    print()
    print(grid.to_string())
    while True:
        if grid.is_clear():
            print('You win!')
            break
        print('Enter action: [F]lag/[U]nflag or [R]eveal followed by cell coordinates (e.g. R A:9) ')
        action_raw = input('Action: ').strip()
        if match := ACTION_RE.match(action_raw):
            action = match.group('action').upper()
            row = match.group('row')
            col = match.group('col')
            try:
                if action == 'F':
                    grid.flag_cell(row, col)
                    print(grid.to_string())
                elif action == 'U':
                    grid.unflag_cell(row, col)
                    print(grid.to_string())
                elif action == 'R':
                    if not grid.reveal_cell(row, col):
                        print(grid.to_string())
                        print('Game over.')
                        break
                    else:
                        print(grid.to_string())
                else:
                    print('Please enter a valid action. (F, U or R)')
            except (ValueError, IndexError, RuntimeError) as e:
                print(e.args[0])
        else:
            print('Please enter a valid action.')


def main():
    print('== Minesweeper ==')
    try:
        grid = init_grid()
        game_loop(grid)
    except KeyboardInterrupt:
        print()
        sys.exit('Exiting...')
