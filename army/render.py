# render.py
from utils import grid_to_central_coordinate
from config import ANIME_DURATION, SPEED_PRECISION
from events import OnUpdate


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

        # Update the sprite's position to reflect the army's new position
        px, py = grid_to_central_coordinate(*army.position)
        move_army(army, px, py)


subscriptions = {OnUpdate: update_armies}
