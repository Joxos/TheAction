from events import OnDraw, OnGameInit, EventsManager, OnMouseMotion


def on_mouse_motion(game, event: OnMouseMotion, em: EventsManager):
    game.mouse_x = event.x
    game.mouse_y = event.y


def on_draw(game, event: OnDraw, em: EventsManager):
    game.clear()

    for sprite in game.draw_list:
        sprite.draw()


def on_game_init(game, event, em: EventsManager):
    game.center_window()

    # we use a draw list to avoid problems
    # when multiple modules want to draw and clear the screen after previous module has drawn up
    game.draw_list = []

    game.mouse_x = 0
    game.mouse_y = 0


subscriptions = {
    OnDraw: on_draw,
    OnGameInit: on_game_init,
    OnMouseMotion: on_mouse_motion,
}
