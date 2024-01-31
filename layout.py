from enum import Enum, auto
from config import SIDEBAR_WIDTH, GRID_WIDTH, BOARDER_WIDTH


class Layouts(Enum):
    GRID = auto()
    LEFT_SIDEBAR = auto()
    RIGHT_SIDEBAR = auto()


def on_grid(x, y):
    if x < SIDEBAR_WIDTH or x > SIDEBAR_WIDTH + GRID_WIDTH - BOARDER_WIDTH:
        return False
    return True


def on_left_sidebar(x, y):
    if x < SIDEBAR_WIDTH:
        return True
    return False


def on_right_sidebar(x, y):
    if x > SIDEBAR_WIDTH + GRID_WIDTH - BOARDER_WIDTH:
        return True
    return False


def get_layout(x, y):
    if on_grid(x, y):
        return Layouts.GRID
    elif on_left_sidebar(x, y):
        return Layouts.LEFT_SIDEBAR
    elif on_right_sidebar(x, y):
        return Layouts.RIGHT_SIDEBAR
    else:
        return None
