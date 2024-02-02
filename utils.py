from config import (
    CELL_WIDTH,
    CELL_HEIGHT,
    BOARDER_WIDTH,
    SIDEBAR_WIDTH,
    BOTTOM_SIDEBAR_HEIGHT,
    COLUMN_COUNT,
    ROW_COUNT,
)
from layout import layout_manager, LAYOUTS


def mix_color(a, b):
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2, (a[2] + b[2] // 2))


def grid_to_central_coordinate(row, column):
    x = (
        column * (CELL_WIDTH + BOARDER_WIDTH)  # column starts from 0
        + CELL_WIDTH / 2
        + BOARDER_WIDTH
        + SIDEBAR_WIDTH
    )
    y = (
        row * (CELL_HEIGHT + BOARDER_WIDTH)  # row starts from 0
        + CELL_HEIGHT / 2
        + BOARDER_WIDTH
        + BOTTOM_SIDEBAR_HEIGHT
    )
    return [x, y]


def coordinate_to_grid(x, y):
    if layout_manager.on_layout(LAYOUTS.GRID, x, y):
        column = (x - SIDEBAR_WIDTH) // (CELL_WIDTH + BOARDER_WIDTH)
        row = (y - BOTTOM_SIDEBAR_HEIGHT) // (CELL_HEIGHT + BOARDER_WIDTH)
        if column < COLUMN_COUNT and row < ROW_COUNT:
            return [row, column]
        else:
            return [row - 1, column - 1]
