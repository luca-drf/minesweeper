import pytest
from core.components import Cell, Grid


def test_cell_defaults():
    cell = Cell(1, 2)
    assert not cell.cleared
    assert not cell.bomb
    assert not cell.flagged
    assert cell.counter == 0
    assert cell.row == 1
    assert cell.col == 2


