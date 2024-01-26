from utils import coordinate_to_grid
from map import Map
from events import OnDraw, OnMouseRelease, OnGameInit
from config import (
    ROW_COUNT,
    COLUMN_COUNT,
    BIOME_STEP,
    SIDEBAR_WIDTH,
    GRID_WIDTH,
    BOARDER_WIDTH,
)


def on_mouse_release(game, event: OnMouseRelease):
    row, column = coordinate_to_grid(event.x - SIDEBAR_WIDTH, event.y)
    if event.x < SIDEBAR_WIDTH or event.x > SIDEBAR_WIDTH + GRID_WIDTH - BOARDER_WIDTH:
        return

    game.select_cell(row, column)


def on_draw(game, event: OnDraw):
    game.clear()

    for sprite in game.draw_list:
        sprite.draw()


def on_game_init(game, event):
    # actually the color of boarder
    game.grid_selected = None
    game.map = Map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)


subscriptions = {
    OnDraw: on_draw,
    OnMouseRelease: on_mouse_release,
    OnGameInit: on_game_init,
}
