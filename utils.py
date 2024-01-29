from config import CELL_WIDTH, CELL_HEIGHT, BOARDER_WIDTH, SIDEBAR_WIDTH


def mix_color(a, b):
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2, (a[2] + b[2] // 2))


def grid_to_central_coordinate(row, column):
    x = column * (CELL_WIDTH + BOARDER_WIDTH) + (CELL_WIDTH / 2 + BOARDER_WIDTH)
    y = row * (CELL_HEIGHT + BOARDER_WIDTH) + (CELL_HEIGHT / 2 + BOARDER_WIDTH)
    return [x + SIDEBAR_WIDTH, y]


def coordinate_to_grid(x, y):
    column = (x - SIDEBAR_WIDTH) // (CELL_WIDTH + BOARDER_WIDTH)
    row = y // (CELL_HEIGHT + BOARDER_WIDTH)
    return [row, column]
