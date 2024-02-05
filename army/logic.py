# logic.py
import arcade
from army.army import Army
from utils import grid_to_central_coordinate, coordinate_to_grid
from layout import layout_manager, LAYOUTS
from events import OnGameInit, OnGameSetup, OnLeftMousePress, OnRightMousePress


def army_init(game, event, em):
    game.army_list = []
    game.army_selected = None


def generate_army(game, army_info):
    """Helper function to create and add an army to the game."""
    army_sprite = arcade.SpriteCircle(5, army_info.color)
    army_sprite.center_x, army_sprite.center_y = grid_to_central_coordinate(
        *army_info.position
    )  # star to unpackage tuple
    army_info.sprite = army_sprite
    game.draw_list.append(army_sprite)
    game.army_list.append(army_info)


def army_setup(game, event, em):
    generate_army(
        game, Army(id=1, position=(0, 0), color=arcade.color.GO_GREEN, move_interval=10)
    )


def get_army_by_position(game, position):
    """Returns the army at the given grid position, if any."""
    position = tuple(position)
    return next((army for army in game.army_list if army.position == position), None)


def set_destination(game, event_x, event_y):
    """Sets the destination for the selected army."""
    waypoints = game.map.get_minimum_waypoints(
        game.army_selected.position, coordinate_to_grid(event_x, event_y)
    )
    if waypoints:
        game.army_selected.waypoints = waypoints


def append_destination(game, event_x, event_y):
    """Appends a new destination to the army's waypoints."""
    if game.army_selected.waypoints:
        new_waypoints = game.map.get_minimum_waypoints(
            game.army_selected.waypoints[-1], coordinate_to_grid(event_x, event_y)
        )
        if new_waypoints:
            game.army_selected.waypoints.extend(new_waypoints)
    else:
        set_destination(game, event_x, event_y)


def army_set_destination(game, event, em):
    if (
        game.army_selected
        and layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y)
        and not event.key_modifiers & arcade.key.MOD_SHIFT
    ):
        set_destination(game, event.x, event.y)


def army_append_destination(game, event, em):
    if (
        game.army_selected
        and layout_manager.on_layout(LAYOUTS.GRID, event.x, event.y)
        and event.key_modifiers & arcade.key.MOD_SHIFT
    ):
        append_destination(game, event.x, event.y)


def select_army(game, event, em):
    """Selects an army when the left mouse button is pressed."""
    army = get_army_by_position(game, coordinate_to_grid(event.x, event.y))
    if army:
        game.army_selected = army


subscriptions = {
    OnGameInit: army_init,
    OnGameSetup: army_setup,
    OnRightMousePress: [army_set_destination, army_append_destination],
    OnLeftMousePress: select_army,
}
