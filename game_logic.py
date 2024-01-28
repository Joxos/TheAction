import arcade
from utils import coordinate_to_grid
from map.map import Map
from events import OnDraw, OnMouseRelease, OnGameInit, OnCellSelected, EventsManager
from config import (
    ROW_COUNT,
    COLUMN_COUNT,
    BIOME_STEP,
    SIDEBAR_WIDTH,
    GRID_WIDTH,
    BOARDER_WIDTH,
)


def on_mouse_release(game, event: OnMouseRelease, em: EventsManager):
    row, column = coordinate_to_grid(event.x - SIDEBAR_WIDTH, event.y)
    if event.x < SIDEBAR_WIDTH or event.x > SIDEBAR_WIDTH + GRID_WIDTH - BOARDER_WIDTH:
        return
    em.new_event(OnCellSelected(row, column))


def on_draw(game, event: OnDraw, em: EventsManager):
    game.clear()

    for sprite in game.draw_list:
        sprite.draw()


def on_game_init(game, event, em: EventsManager):
    game.grid_selected = None
    game.map = Map(ROW_COUNT, COLUMN_COUNT, BIOME_STEP)
    game.background_color = arcade.color.BLACK

    # we use a draw list to avoid problems
    # when multiple modules want to draw and clear the screen after previous module has drawn up
    game.draw_list = []


subscriptions = {
    OnDraw: on_draw,
    OnMouseRelease: on_mouse_release,
    OnGameInit: on_game_init,
}
