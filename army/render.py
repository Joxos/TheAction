from events import OnUpdate, EventsManager
from utils import grid_to_central_coordinate
from config import ANIME_DURATION, SPEED_PRECISION


def update_armies(game, event: OnUpdate, em: EventsManager):
    for army in game.army_list:
        if army.waypoints and army.move_interval_counter <= 0:
            # Move the army to the next waypoint
            army.position = army.waypoints.popleft()
            factor = 1
            if army.waypoints:
                factor = game.map.calculate_3d_distance(
                    army.position, army.waypoints[0]
                )
            army.move_interval_counter = army.move_interval * factor
        else:
            px, py = grid_to_central_coordinate(army.position[0], army.position[1])
            if army.sprite.center_x != px or army.sprite.center_y != py:
                dx, dy = px - army.sprite.center_x, py - army.sprite.center_y
                army.sprite.center_x += dx / ANIME_DURATION
                army.sprite.center_y += dy / ANIME_DURATION
            army.move_interval_counter -= SPEED_PRECISION


subscriptions = {OnUpdate: update_armies}
