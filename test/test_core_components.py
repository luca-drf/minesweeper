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


def test_cell_clear_default():
    cell = Cell(1, 2)
    cell.clear()
    assert cell.cleared


def test_cell_clear_cleared():
    cell = Cell(1, 2, cleared=True)
    with pytest.raises(RuntimeError):
        cell.clear()
    assert cell.cleared


def test_cell_clear_flagged():
    cell = Cell(1, 2, flagged=True)
    with pytest.raises(RuntimeError):
        cell.clear()
    assert not cell.cleared


def test_cell_counter_default():
    cell = Cell(1, 2)
    assert cell.counter == 0


def test_cell_counter_error():
    cell = Cell(1, 2)
    with pytest.raises(ValueError):
        cell.counter = 9
    with pytest.raises(ValueError):
        cell.counter = -1


def test_cell_flag_default():
    cell = Cell(1, 2)
    assert not cell.flagged
    cell.flag()
    assert cell.flagged


def test_cell_flag_error():
    cell = Cell(1, 2, cleared=True)
    with pytest.raises(RuntimeError):
        cell.flag()


def test_cell_unflag():
    cell = Cell(1, 2, flagged=True)
    assert cell.flagged
    cell.unflag()
    assert not cell.flagged


def test_cell_unflag_error():
    cell = Cell(1, 2)
    with pytest.raises(RuntimeError):
        cell.unflag()


@pytest.fixture
def default_grid():
    return Grid(6, 7)


def test_grid_cell_coord(default_grid):
    pass


def test_grid_cell_place_bombs(default_grid):
    pass
