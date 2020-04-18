import pytest
from core.components import Cell, Grid, label_to_i


# TODO: Add more corner-case tests


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


def test_grid_cell_position(default_grid):
    assert default_grid._cells[5][6].row == 5
    assert default_grid._cells[5][6].col == 6


def test_grid_cell_at_pos(default_grid):
    cell = default_grid.cell_at_pos(41)
    assert (cell.row, cell.col) == (5, 6)


def test_grid_cell_at_pos_error(default_grid):
    with pytest.raises(IndexError):
        default_grid.cell_at_pos(42)


def test_grid_cell_at(default_grid):
    assert default_grid.cell_at('A', '1') is default_grid._cells[0][0]
    assert default_grid.cell_at('F', '7') is default_grid._cells[5][6]


def test_grid_cell_at_error(default_grid):
    with pytest.raises(ValueError):
        default_grid.cell_at('A', '')
    with pytest.raises(ValueError):
        default_grid.cell_at('', '1')
    with pytest.raises(ValueError):
        default_grid.cell_at('A', 'B')
    with pytest.raises(IndexError):
        default_grid.cell_at('A', '-1')
    with pytest.raises(IndexError):
        default_grid.cell_at('AA', '1')
    with pytest.raises(IndexError):
        default_grid.cell_at('A', '42')


def test_grid_cell_place_bombs(default_grid):
    assert default_grid._bombs == 0
    assert sum(map(lambda cell: cell.bomb, default_grid)) == 0
    default_grid.place_bombs(6)
    assert default_grid._bombs == 6
    assert sum(map(lambda cell: cell.bomb, default_grid)) == 6
    with pytest.raises(RuntimeError):
        default_grid.place_bombs(1)


def test_grid_reveal_bombs(default_grid):
    default_grid.place_bombs(4)
    default_grid.reveal_bombs()
    for cell in default_grid:
        if cell.bomb:
            assert cell.cleared


def test_grid_cell_neighbours_corner(default_grid):
    cell = default_grid._cells[0][0]
    expected_neighbours = [
        default_grid._cells[0][1],
        default_grid._cells[1][0],
        default_grid._cells[1][1]
    ]
    actual_neighbours = default_grid._cell_neighbours(cell.row, cell.col)
    iterations = 0
    for expected_neighbour, actual_neighbour in zip(expected_neighbours, actual_neighbours):
        assert expected_neighbour is actual_neighbour
        iterations += 1
    assert iterations == len(expected_neighbours)


def test_grid_cell_neighbours_center(default_grid):
    cell = default_grid._cells[1][1]
    expected_neighbours = [
        default_grid._cells[0][0],
        default_grid._cells[0][1],
        default_grid._cells[0][2],
        default_grid._cells[1][0],
        default_grid._cells[1][2],
        default_grid._cells[2][0],
        default_grid._cells[2][1],
        default_grid._cells[2][2]
    ]
    actual_neighbours = default_grid._cell_neighbours(cell.row, cell.col)
    iterations = 0
    for expected_neighbour, actual_neighbour in zip(expected_neighbours, actual_neighbours):
        assert expected_neighbour is actual_neighbour
        iterations += 1
    assert iterations == len(expected_neighbours)


def test_grid_clear_field(default_grid):
    bombs_positions = [0, 16]
    expected_counters = [
            0, 1, 0, 0, 0, 0, 0,
            1, 2, 1, 1, 0, 0, 0,
            0, 1, 0, 1, 0, 0, 0,
            0, 1, 1, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0
    ]
    default_grid.place_bombs(2, positions=bombs_positions)
    default_grid._clear_field(5, 6)
    assert not default_grid._cells[0][0].cleared
    assert not default_grid._cells[2][2].cleared
    assert default_grid._cleared_cells == 40
    for cell, exp_count in zip(default_grid, expected_counters):
        assert cell.counter == exp_count


def test_grid_is_clear(default_grid):
    bombs_positions = [0, 0]
    default_grid.place_bombs(1, positions=bombs_positions)
    default_grid._clear_field(0, 1)
    assert not default_grid.is_clear()
    default_grid._clear_field(0, 2)
    assert default_grid.is_clear()


def test_label_to_i():
    assert label_to_i('A') == 1
    assert label_to_i('AA') == 27
    assert label_to_i('BAA') == 1379
    assert label_to_i('AP') == 42
    assert label_to_i('') == 0
