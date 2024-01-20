from config import CELL_WIDTH, CELL_HEIGHT, BOARDER_WIDTH, SIDEBAR_WIDTH


def mix_color(a, b):
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2, (a[2] + b[2] // 2))


def grid_to_central_coordinate(row, column):
    x = column * (CELL_WIDTH + BOARDER_WIDTH) + (CELL_WIDTH / 2 + BOARDER_WIDTH)
    y = row * (CELL_HEIGHT + BOARDER_WIDTH) + (CELL_HEIGHT / 2 + BOARDER_WIDTH)
    return [x, y]


def coordinate_to_grid(x, y):
    column = int(x // (CELL_WIDTH + BOARDER_WIDTH))
    row = int(y // (CELL_HEIGHT + BOARDER_WIDTH))
    return [row, column]
