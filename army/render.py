# render.py
from utils import grid_to_central_coordinate
from config import ANIME_DURATION, SPEED_PRECISION
from events import OnUpdate


def is_mouse_over(sprite, mouse_x, mouse_y):
    """Check if the mouse is over the sprite."""
    return sprite.collides_with_point((mouse_x, mouse_y))


def set_transparency(game):
    """
    Waypoints transparency is 255 for game.army_selected and army hovered over. Otherwise, it's 128.
    """
    for army in game.army_list:
        if (
            is_mouse_over(army.sprite, game.mouse_x, game.mouse_y)
            or army == game.army_selected
        ):
            army.sprite.alpha = 255
            army.path_line_sprites.alpha = 255
        else:
            army.sprite.alpha = 128
            army.path_line_sprites.alpha = 128


def move_army(army, px, py):
    """Moves the army's sprite towards the given pixel coordinates."""
    dx, dy = px - army.sprite.center_x, py - army.sprite.center_y
    if dx != 0 or dy != 0:
        army.sprite.center_x += dx / ANIME_DURATION
        army.sprite.center_y += dy / ANIME_DURATION


def process_army_movement(army, game):
    """Processes the movement of an army based on its waypoints."""
    if army.waypoints:
        if army.move_interval_counter <= 0:
            next_position = army.pop_waypoint()  # Pops the next waypoint
            if next_position:
                army.update_position(next_position)
                army.popleft_path_line_sprite()
                if army.has_waypoints():
                    # Calculate the factor based on 3D distance to next waypoint
                    factor = game.map.calculate_3d_distance(
                        army.position, army.waypoints[0]
                    )
                    army.move_interval_counter = army.move_interval * factor
        else:
            army.move_interval_counter -= SPEED_PRECISION


def update_armies(game, event, em):
    """Update function called for each army on every frame."""
    for army in game.army_list:
        process_army_movement(army, game)
        set_transparency(game)

        # Update the sprite's position to reflect the army's new position
        px, py = grid_to_central_coordinate(*army.position)
        move_army(army, px, py)


subscriptions = {OnUpdate: update_armies}
