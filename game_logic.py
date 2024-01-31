import arcade
from events import OnDraw, OnGameInit, EventsManager


def on_draw(game, event: OnDraw, em: EventsManager):
    game.clear()

    for sprite in game.draw_list:
        sprite.draw()


def on_game_init(game, event, em: EventsManager):
    game.center_window()

    # we use a draw list to avoid problems
    # when multiple modules want to draw and clear the screen after previous module has drawn up
    game.draw_list = []


subscriptions = {
    OnDraw: on_draw,
    OnGameInit: on_game_init,
}
