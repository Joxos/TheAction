from events import (
    OnGameInit,
    OnGameSetup,
    EventsManager,
    OnRightMousePress,
    OnLeftMousePress,
)
import arcade
from army.army import Army
from utils import grid_to_central_coordinate, coordinate_to_grid
from layout import layout_manager, LAYOUTS


def army_init(game, event: OnGameInit, em: EventsManager):
    game.army_list = []
    game.army_selected = None


def generate_army(game, army_info: Army):
    army_sprite = arcade.SpriteCircle(5, army_info.color)
    army_sprite.center_x, army_sprite.center_y = grid_to_central_coordinate(
        army_info.position[0], army_info.position[1]
    )
    army_info.sprite = army_sprite
    game.draw_list.append(army_sprite)
    game.army_list.append(army_info)


def army_setup(game, event: OnGameSetup, em: EventsManager):
    generate_army(
        game, Army(id=1, position=(0, 0), color=arcade.color.RED, move_interval=30)
    )


def get_army(game, position):
    for army in game.army_list:
        if army.position == position:
            return army
    return None


def army_set_destination(game, event: OnRightMousePress, em: EventsManager):
    if (
        game.army_selected
        and layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y)
        and not event.key_modifiers & arcade.key.MOD_SHIFT
    ):
        game.army_selected.waypoints = game.map.get_minimum_waypoints(
            game.army_selected.position, coordinate_to_grid(event.x, event.y)
        )


def army_append_destination(game, event: OnRightMousePress, em: EventsManager):
    if (
        game.army_selected
        and layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y)
        and event.key_modifiers & arcade.key.MOD_SHIFT
    ):
        if game.army_selected.waypoints:
            game.army_selected.waypoints.extend(
                game.map.get_minimum_waypoints(
                    game.army_selected.waypoints[-1],
                    coordinate_to_grid(event.x, event.y),
                )
            )
        else:
            game.army_selected.waypoints = game.map.get_minimum_waypoints(
                game.army_selected.position, coordinate_to_grid(event.x, event.y)
            )


def select_army(game, event: OnLeftMousePress, em: EventsManager):
    for army in game.army_list:
        if layout_manager.on_layout(
            LAYOUTS.GRID, event.x, event.y
        ) and coordinate_to_grid(event.x, event.y) == list(army.position):
            game.army_selected = army
            break


subscriptions = {
    OnGameInit: army_init,
    OnGameSetup: army_setup,
    OnRightMousePress: [army_set_destination, army_append_destination],
    OnLeftMousePress: select_army,
}
