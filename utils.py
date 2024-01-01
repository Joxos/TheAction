from config import (
    WIDTH,
    HEIGHT,
    BOARDER,
)


def mix_color(a, b):
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2, (a[2] + b[2] // 2))


def grid_to_central_coordinate(row, column):
    x = column * (WIDTH + BOARDER) + (WIDTH / 2 + BOARDER)
    y = row * (HEIGHT + BOARDER) + (HEIGHT / 2 + BOARDER)
    return [x, y]


def coordinate_to_grid(x, y):
    column = int(x // (WIDTH + BOARDER))
    row = int(y // (HEIGHT + BOARDER))
    return [row, column]
