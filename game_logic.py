import arcade
from utils import coordinate_to_grid
from layout import on_grid
from map.map import Map
from events import OnDraw, OnMouseRelease, OnGameInit, OnCellSelected, EventsManager
from config import (
    ROW_COUNT,
    COLUMN_COUNT,
    BIOME_STEP,
)


def on_mouse_release(game, event: OnMouseRelease, em: EventsManager):
    if not on_grid(event.x, event.y):
        return
    row, column = coordinate_to_grid(event.x, event.y)
    if event.button == arcade.MOUSE_BUTTON_LEFT:
        em.new_event(OnCellSelected(row, column))


def on_draw(game, event: OnDraw, em: EventsManager):
    game.clear()

    for sprite in game.draw_list:
        sprite.draw()


def on_game_init(game, event, em: EventsManager):
    game.center_window()
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
