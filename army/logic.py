# logic.py
import arcade
from army.army import Army
from utils import grid_to_central_coordinate, coordinate_to_grid
from layout import layout_manager, LAYOUTS
from events import (
    OnGameInit,
    OnGameSetup,
    OnLeftMousePress,
    OnRightMousePress,
    OnKeyPress,
)
import math


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
    army_info.path_line_sprites = arcade.SpriteList()
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


def create_path_sprites(points, line_color, line_width, alpha=255):
    path_sprites = arcade.SpriteList()
    # the first element should be empty since the animaion starts from the second element
    path_sprites.append(arcade.Sprite())

    for i in range(len(points) - 1):
        start_x, start_y = points[i]
        end_x, end_y = points[i + 1]

        line_color_with_alpha = (*line_color[:3], alpha)  # 将RGB颜色和alpha值组合为RGBA
        line_texture = arcade.make_soft_square_texture(
            line_width, line_color_with_alpha, outer_alpha=0
        )

        line_sprite = arcade.Sprite()
        line_sprite.texture = line_texture
        line_sprite.center_x = (start_x + end_x) / 2
        line_sprite.center_y = (start_y + end_y) / 2

        angle_rad = math.atan2(end_y - start_y, end_x - start_x)
        line_sprite.angle = math.degrees(angle_rad)
        line_length = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        line_sprite.width = line_length
        line_sprite.alpha = alpha

        path_sprites.append(line_sprite)

    return path_sprites


def army_deselect(game, event, em):
    """
    Deselect with escape key.
    """

    if event.key == arcade.key.ESCAPE:
        game.army_selected = None


def set_destination(game, event_x, event_y):
    """Sets the destination for the selected army."""
    waypoints = game.map.get_minimum_waypoints(
        game.army_selected.position, coordinate_to_grid(event_x, event_y)
    )
    if waypoints:
        game.army_selected.waypoints = waypoints
        # remove old path line sprites
        if game.army_selected.path_line_sprites:
            game.army_selected.path_line_sprites.clear()
        coordinates = [grid_to_central_coordinate(*wp) for wp in waypoints]
        game.army_selected.path_line_sprites = create_path_sprites(
            coordinates, arcade.color.BLUE, 5, alpha=128
        )
        game.draw_list.append(game.army_selected.path_line_sprites)


def append_destination(game, event_x, event_y):
    """Appends a new destination to the army's waypoints."""
    if game.army_selected.waypoints:
        new_waypoints = game.map.get_minimum_waypoints(
            game.army_selected.waypoints[-1], coordinate_to_grid(event_x, event_y)
        )
        print(new_waypoints)
        if new_waypoints:
            game.army_selected.waypoints.extend(new_waypoints)
            new_coordinates = [grid_to_central_coordinate(*wp) for wp in new_waypoints]
            game.army_selected.path_line_sprites.extend(
                create_path_sprites(new_coordinates, arcade.color.BLUE, 5, alpha=128)
            )
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
    OnKeyPress: army_deselect,
}
